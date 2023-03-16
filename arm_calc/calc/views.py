from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, \
    DeleteView, DetailView, ListView

from calc import models
from calc.forms import FolderForm, ElementForm, RodsCalcForm, RodFormSet

User = get_user_model()


class LandingView(TemplateView):
    template_name = 'calc/landing.html'


class ProfileView(DetailView):
    template_name = 'calc/profile.html'
    Model = get_user_model()
    context_object_name = 'user'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        engineer = get_object_or_404(User, username=username)
        context['folders'] = engineer.folders.filter(folder=None)
        context['elements'] = engineer.elements.filter(folder=None)
        return context


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
    template_name = 'calc/site_detail.html'
    Model = models.Site


class SiteCreateView(CreateView):
    template_name = 'calc/site_create.html'
    Model = models.Site


class SiteUpdateView(UpdateView):
    template_name = 'calc/site_update.html'
    Model = models.Site


class SiteDuplicateView(View):
    template_name = 'calc/site_duplicate.html'
    Model = models.Site


class SiteDeleteView(DeleteView):
    Model = models.Site


class ConstructionDetailView(DetailView):
    template_name = 'calc/construction_detail.html'
    Model = models.Construction


class ConstructionCreateView(CreateView):
    template_name = 'calc/construction_create.html'
    Model = models.Construction


class ConstructionUpdateView(UpdateView):
    template_name = 'calc/construction_update.html'
    Model = models.Construction


class ConstructionDuplicateView(View):
    template_name = 'calc/construction_duplicate.html'
    Model = models.Construction


class ConstructionDeleteView(DeleteView):
    Model = models.Construction


class VersionDetailView(DetailView):
    template_name = 'calc/version_detail.html'
    Model = models.Version


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

    def form_valid(self, form):
        pass


# def folder_create(request):
#     form = FolderForm(
#         request.POST or None,
#         files=request.FILES or None,
#     )
#     if form.is_valid():
#         engineer = request.user
#         folder = form.save(commit=False)
#         folder.engineer = request.user
#         try:
#             folder.folder = models.Folder.objects.get(
#                 pk=int(cache.get('folder_id')))
#             cache.clear()
#         except:
#             pass
#         folder.save()
#         return redirect('calc:folder', folder.pk)
#     context = {
#         'form': form,
#     }
#     return render(request, 'calc/folder_create.html', context)


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
    template_name = 'calc/element_detail.html'
    Model = models.Element


class ElementCreateView(CreateView):
    template_name = 'calc/element_create.html'
    Model = models.Element

    def form_valid(self, form):
        pass


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
    form_class = RodsCalcForm
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
                'rods': RodFormSet(prefix='rods'),
            }
        else:
            return {
                'rods': RodFormSet(
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
            'rods': RodFormSet(
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
    template_name = 'calc/volumes_calc_duplicate.html'
    Model = models.VolumesCalc


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
    template_name = 'calc/squares_calc_duplicate.html'
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
    template_name = 'calc/lengths_calc_duplicate.html'
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
    template_name = 'calc/units_calc_duplicate.html'
    Model = models.UnitsCalc


class UnitsCalcDeleteView(DeleteView):
    pass


class UnitDuplicateView(View):
    Model = models.Unit


class UnitDeleteView(DeleteView):
    Model = models.Unit
