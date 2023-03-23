from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, \
    DeleteView, DetailView, ListView, FormView

from . import custom_operations
from . import models
from . import forms

User = get_user_model()


class LandingView(TemplateView):
    template_name = 'calc/landing.html'


class ProfileView(ListView):
    template_name = 'calc/profile.html'
    model = models.Site
    context_object_name = 'sites'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(engineer=self.request.user)


class ResultView(DetailView):
    template_name = 'calc/result.html'
    Model = models.Element


# def result(request, pk):
#     element = models.Element.objects.get(pk=pk)
#     rods_calc = models.RodsCalc.objects.get(element=element)
#     rods = models.Rod.objects.filter(rods_calc=rods_calc)
#     arm_classes = sorted(
#         list(set(rods.values_list('arm_class', flat=True).distinct()))
#     )
#     results = {}
#     for clas in arm_classes:
#         diameters = sorted(list(set(
#             rods.filter(arm_class=clas).values_list('diameter',
#                                                     flat=True
#                                                     ).distinct()
#         )))
#         masses = []
#         for diameter in diameters:
#             all_rods_of_diameter = rods.filter(diameter=diameter,
#                                                arm_class=clas)
#             masses_of_diameter = []
#             for rod in all_rods_of_diameter:
#                 mass = rod.mass_of_rods()
#                 masses_of_diameter.append(mass)
#             masses.append(round(sum(masses_of_diameter), 2))
#
#         diameters = list(map(lambda x: '⌀' + str(x), diameters))
#         diameters.append('Итого')
#         masses.append(round(sum(masses), 2))
#
#         dictionary = dict(zip(diameters, masses))
#         results[clas] = dictionary
#
#     masses_of_rods = []
#     for rod in rods:
#         mass_of_rod = rod.mass_of_rods()
#         masses_of_rods.append(mass_of_rod)
#
#     sum_element = round(sum(masses_of_rods), 2)
#     context = {
#         'element': element,
#         'rods': rods,
#         'results': results,
#         'sum_element': sum_element,
#     }
#     return render(request, 'calc/result.html', context)


class SiteDetailView(DetailView):
    template_name = 'calc/site/site_detail.html'
    model = models.Site
    context_object_name = 'site'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_id = self.kwargs.get('pk')
        context['constructions'] = models.Construction.objects.filter(
            site=site_id)
        return context


class SiteCreateView(CreateView):
    template_name = 'calc/site/site_create.html'
    Model = models.Site
    form_class = forms.SiteForm
    context_object_name = 'site'

    def form_valid(self, form):
        engineer = self.request.user
        site = form.save(commit=False)
        site.engineer = engineer
        site.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:site_detail', kwargs={'pk': self.object.pk})


class SiteUpdateView(UpdateView):
    template_name = 'calc/site/site_create.html'
    model = models.Site
    form_class = forms.SiteForm
    context_object_name = 'site'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.__class__.__name__ == 'SiteUpdateView':
            context['view_name'] = 'update'
        return context

    def form_valid(self, form):
        engineer = self.request.user
        site = form.save(commit=False)
        site.engineer = engineer
        site.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:site_detail', kwargs={'pk': self.object.pk})


class SiteDuplicateView(FormView):
    template_name = 'calc/site/site_create.html'
    form_class = forms.SiteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def get_object(self):
        return get_object_or_404(models.Site, pk=self.kwargs['pk'])

    def form_valid(self, form):
        new_object = custom_operations.duplicate_object(form.instance)
        form = self.form_class(self.request.POST, instance=new_object)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:landing')


class SiteDeleteView(DeleteView):
    model = models.Site
    template_name = 'calc/includes/confirm_delete.html'
    success_url = reverse_lazy('calc:landing')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ConstructionDetailView(DetailView):
    template_name = 'calc/construction/construction_detail.html'
    model = models.Construction
    context_object_name = 'construction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        construction_id = self.kwargs.get('pk')
        context['versions'] = models.Version.objects.filter(
            construction=construction_id)
        return context


class ConstructionCreateView(CreateView):
    template_name = 'calc/construction/construction_create.html'
    model = models.Construction
    form_class = forms.ConstructionForm
    context_object_name = 'construction'

    def form_valid(self, form):
        site = models.Site.objects.get(
            pk=self.kwargs['site_pk'],
        )
        site.engineer = self.request.user
        site.save()
        construction = form.save(commit=False)
        construction.site = site
        construction.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:construction_detail',
                       kwargs={'pk': self.object.pk})


class ConstructionUpdateView(UpdateView):
    template_name = 'calc/construction/construction_create.html'
    model = models.Construction
    form_class = forms.ConstructionForm

    def form_valid(self, form):
        site = self.get_object().site
        construction = form.save(commit=False)
        construction.site = site
        construction.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.__class__.__name__ == 'ConstructionUpdateView':
            context['view_name'] = 'update'
        return context


class ConstructionDuplicateView(View):
    template_name = 'calc/construction_duplicate.html'
    Model = models.Construction


class ConstructionDeleteView(DeleteView):
    Model = models.Construction


class VersionDetailView(DetailView):
    template_name = 'calc/version/version_detail.html'
    model = models.Version
    context_object_name = 'version'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        version_id = self.kwargs.get('pk')
        context['folders'] = models.Folder.objects.filter(
            version=version_id)
        return context


class VersionCreateView(CreateView):
    template_name = 'calc/version_create.html'
    Model = models.Version


class VersionUpdateView(UpdateView):
    template_name = 'calc/version_update.html'
    Model = models.Version


class VersionDuplicateView(View):
    template_name = 'calc/version_duplicate.html'
    Model = models.Version


class VersionDeleteView(DeleteView):
    Model = models.Version


class FolderDetailView(DetailView):
    template_name = 'calc/folder_detail.html'
    Model = models.Folder
    context_object_name = 'folder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder_id = self.kwargs.get('folder_id')
        folder = models.Folder.objects.get(pk=folder_id)
        context['folders'] = models.Folder.objects.filter(folder=folder)
        context['elements'] = folder.elements.all()
        cache.set('folder_id', str(folder.pk))
        return context


class FolderCreateView(CreateView):
    template_name = 'calc/folder_create.html'
    Model = models.Folder
    form_class = forms.FolderForm
    context_object_name = 'folder'

    def form_valid(self, form):
        engineer = self.request.user
        folder = form.save(commit=False)
        folder.engineer = self.request.user
        try:
            folder.folder = models.Folder.objects.get(
                pk=int(cache.get('folder_id')))
            cache.clear()
        except:
            pass
        folder.save()

    def get_success_url(self):
        return reverse('calc:folder_detail', kwargs={'pk': self.object.pk})


class FolderUpdateView(UpdateView):
    template_name = 'calc/folder_update.html'
    Model = models.Folder


class FolderDuplicateView(View):
    template_name = 'calc/folder_duplicate.html'
    Model = models.Folder


class FolderDeleteView(DeleteView):
    Model = models.Folder


# def folder_delete(request, pk):
#     folder = models.Folder.objects.get(pk=pk)
#     place_folder = folder.folder
#     if folder:
#         folder.delete()
#     if place_folder:
#         return redirect('calc:folder', place_folder.pk)
#     else:
#         return redirect('calc:profile', request.user.username)


class ElementDetailView(DetailView):
    template_name = 'calc/element/element_detail.html'
    model = models.Element
    context_object_name = 'element'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        element_id = self.kwargs.get('pk')
        context['rods_calcs'] = models.RodsCalc.objects.filter(
            element=element_id)
        return context


class ElementCreateView(CreateView):
    template_name = 'calc/element_create.html'
    Model = models.Element
    form_class = forms.ElementForm
    context_object_name = 'element'

    def form_valid(self, form):
        engineer = self.request.user
        if cache.get('folder_id'):
            element = models.Folder.objects.get(
                pk=int(cache.get('folder_id'))
            )
            cache.clear()
        element = form.save(commit=False)
        element.engineer = self.request.user
        if cache.get('folder_id'):
            element.folder = models.Folder.objects.get(
                pk=int(cache.get('folder_id')))
            cache.clear()
        element.save()

    def get_success_url(self):
        return reverse('calc:element_create', kwargs={'pk': self.object.pk})


# def element_create(request):
#     form = ElementForm(
#         request.POST or None,
#         files=request.FILES or None,
#     )
#     if form.is_valid():
#         engineer = request.user
#         if cache.get('folder_id'):
#             folder = models.Folder.objects.get(
#             pk=int(cache.get('folder_id'))
#             )
#             cache.clear()
#         element = form.save(commit=False)
#         element.engineer = request.user
#         if cache.get('folder_id'):
#             element.folder = models.Folder.objects.get(
#                 pk=int(cache.get('folder_id')))
#             cache.clear()
#         else:
#             element.save()
#             return redirect('calc:profile', request.user.username)
#         element.save()
#         if folder:
#             return redirect('calc:folder', folder.pk)
#     context = {
#         'form': form,
#     }
#     return render(request, 'calc/element_create.html', context)

class ElementUpdateView(UpdateView):
    template_name = 'calc/element_update.html'
    Model = models.Element


# def element_update(request, pk):
#     updated_element = get_object_or_404(models.Element, pk=pk)
#     if request.user != updated_element.engineer:
#         return redirect('calc:profile', request.user.username)
#     form = ElementForm(
#         request.POST or None,
#         files=request.FILES or None,
#         instance=updated_element,
#     )
#     if form.is_valid():
#         form.save()
#         return redirect('calc:profile', request.user.username)
#     context = {'form': form, }
#     return render(request, 'calc/element_create.html', context)

class ElementDuplicateView(View):
    template_name = 'calc/element_duplicate.html'
    Model = models.Element


# def element_duplicate(request, pk):
#     try:
#         element = models.Element.objects.get(id=pk)
#         place_folder = element.folder
#         rods_calcs = models.RodsCalc.objects.filter(element=element)
#     except models.Element.DoesNotExist:
#         messages.error(
#             request, 'Такого элемента нет'
#         )
#         return redirect('calc:folder', pk=element.folder.pk)
#     except models.RodsCalc.DoesNotExist:
#         messages.error(
#             request, 'Такого армирования нет'
#         )
#         return redirect('calc:folder', pk=element.folder.pk)
#
#     element.pk = None
#     element.save()
#
#     for rods_calc in rods_calcs:
#         try:
#             rods = models.Rod.objects.filter(rods_calc=rods_calc)
#         except models.Rod.DoesNotExist:
#             messages.error(
#                 request, 'Такого армирования нет'
#             )
#             return redirect('calc:folder', pk=element.folder.pk)
#         rods_calc.pk = None
#         rods_calc.element = element
#         rods_calc.save()
#
#         for rod in rods:
#             rod.pk = None
#             rod.rods_calc = rods_calc
#             rod.save()
#
#     messages.success(
#         request, 'Элемент успешно скопирован'
#     )
#     if place_folder:
#         return redirect('calc:folder', place_folder.pk)
#     else:
#         return redirect('calc:profile', request.user.username)


class ElementDeleteView(DeleteView):
    Model = models.Element


# def element_delete(request, pk):
#     element = models.Element.objects.get(pk=pk)
#     place_folder = element.folder
#     rods_calcs = models.RodsCalc.objects.filter(element=element)
#     for rods_calc in rods_calcs:
#         rods = models.Rod.objects.filter(rods_calc=rods_calc)
#         if element:
#             element.delete()
#         for rod in rods:
#             if rods:
#                 rod.delete()
#         if place_folder:
#             return redirect('calc:folder', place_folder.pk)
#         else:
#             return redirect('calc:profile', request.user.username)


class RodsCalcDetailView(TemplateView):
    pass


class RodsCalcInline:
    form_class = forms.RodsCalcForm
    model = models.RodsCalc
    template_name = 'calc/rods_calc_create.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        rods_calc = form.save(commit=False)
        rods_calc.element.engineer = self.request.user
        if cache.get('folder_id'):
            rods_calc.element.folder = models.Folder.objects.get(
                pk=int(cache.get('folder_id')))
            cache.clear()
        rods_calc.save()

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('calc:folder', rods_calc.element.folder.pk)

    def formset_rods_valid(self, formset):
        rods = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for rod in rods:
            rod.rods_calc = self.object
            rod.save()


class RodsCalcCreateView(RodsCalcInline, CreateView):
    def get_context_data(self, **kwargs):
        context = super(RodsCalcCreateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'rods': forms.RodFormSet(prefix='rods'),
            }
        else:
            return {
                'rods': forms.RodFormSet(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix='rods'
                ),
            }


class RodsCalcUpdateView(RodsCalcInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(RodsCalcUpdateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'rods': forms.RodFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix='rods'
            ),
        }


class RodsCalcDuplicateView(View):
    template_name = 'calc/rods_calc_duplicate.html'
    Model = models.RodsCalc


class RodsCalcDeleteView(RodsCalcInline, DeleteView):
    pass


class RodDuplicateView(View):
    template_name = 'calc/rod_duplicate.html'
    Model = models.Rod


# def rod_duplicate(request, pk):
#     try:
#         rod = models.Rod.objects.get(id=pk)
#     except models.Rod.DoesNotExist:
#         messages.success(
#             request, 'Такого стержня нет'
#         )
#         return redirect('calc:update_element', pk=rod.rods_calc.element.id)
#
#     rod.pk = None
#     rod.save()
#     messages.success(
#         request, 'Стержень успешно скопирован'
#     )
#     return redirect('calc:update_element', pk=rod.rods_calc.element.id)


class RodDeleteView(DeleteView):
    Model = models.Rod


# def rod_delete(request, pk):
#     try:
#         rod = models.Rod.objects.get(id=pk)
#     except models.Rod.DoesNotExist:
#         messages.success(
#             request, 'Такого стержня нет'
#         )
#         return redirect('calc:update_element', pk=rod.rods_calc.element.id)
#
#     rod.delete()
#     messages.success(
#         request, 'Стержень успешно удален'
#     )
#     return redirect('calc:update_element', pk=rod.rods_calc.element.id)


class VolumesCalcDetailView(TemplateView):
    pass


class VolumesCalcCreateView(CreateView):
    pass


class VolumesCalcUpdateView(RodsCalcInline, UpdateView):
    pass


class VolumesCalcDuplicateView(View):
    pass


class VolumesCalcDeleteView(DeleteView):
    pass


class VolumeDuplicateView(View):
    Model = models.Volume


class VolumeDeleteView(DeleteView):
    Model = models.Volume


class SquaresCalcDetailView(TemplateView):
    pass


class SquaresCalcCreateView(CreateView):
    pass


class SquaresCalcUpdateView(UpdateView):
    pass


class SquaresCalcDuplicateView(View):
    Model = models.SquaresCalc


class SquaresCalcDeleteView(DeleteView):
    pass


class SquareDuplicateView(View):
    Model = models.Square


class SquareDeleteView(DeleteView):
    Model = models.Square


class LengthsCalcDetailView(TemplateView):
    pass


class LengthsCalcCreateView(CreateView):
    pass


class LengthsCalcUpdateView(UpdateView):
    pass


class LengthsCalcDuplicateView(View):
    Model = models.LengthsCalc


class LengthsCalcDeleteView(DeleteView):
    pass


class LengthDuplicateView(View):
    Model = models.Length


class LengthDeleteView(DeleteView):
    Model = models.Length


class UnitsCalcDetailView(TemplateView):
    pass


class UnitsCalcCreateView(CreateView):
    pass


class UnitsCalcUpdateView(UpdateView):
    pass


class UnitsCalcDuplicateView(View):
    Model = models.UnitsCalc


class UnitsCalcDeleteView(DeleteView):
    pass


class UnitDuplicateView(View):
    Model = models.Unit


class UnitDeleteView(DeleteView):
    Model = models.Unit
