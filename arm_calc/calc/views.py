from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, \
    DeleteView, DetailView, ListView, FormView

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


class RodsCalcResultView(DetailView):
    template_name = 'calc/rods_calc/rods_calc_result.html'
    model = models.RodsCalc
    context_object_name = 'rods_calc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rods_calc_id = self.kwargs.get('pk')
        rod_classes = models.RodClass.objects.filter(
            rods_calc=rods_calc_id)
        context['rod_classes'] = rod_classes
        rod_diameters = models.RodDiameter.objects.filter(
            rod_class__in=rod_classes)
        print(rod_diameters)
        context['rod_diameters'] = rod_diameters
        context['rods'] = models.Rod.objects.filter(
            rods_calc=rods_calc_id)
        return context


class SiteDetailView(DetailView):
    template_name = 'calc/site/site_detail.html'
    model = models.Site
    context_object_name = 'site'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_id = self.kwargs.get('pk')
        context['constructions'] = models.Construction.objects.filter(
            site=site_id)
        context['dropdown_actions'] = {
            'Редактировать': reverse('calc:site_update',
                                     args=[self.object.pk]),
            'Удалить': reverse('calc:site_delete', args=[self.object.pk]),
        }
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


def site_duplicate(request, pk):
    site = models.Site.objects.get(pk=pk)
    engineer = site.engineer
    constructions = models.Construction.objects.filter(site=site)

    site.pk = None
    site.save()

    for construction in constructions:
        versions = models.Version.objects.filter(construction=construction)

        construction.pk = None
        construction.site = site
        construction.save()

        for version in versions:
            folders = models.Folder.objects.filter(version=version)

            version.pk = None
            version.construction = construction
            version.save()

            for folder in folders:
                elements = models.Element.objects.filter(folder=folder)

                folder.pk = None
                folder.version = version
                folder.save()

                for element in elements:
                    rods_calcs = models.RodsCalc.objects.filter(
                        element=element)

                    element.pk = None
                    element.folder = folder
                    element.save()

                    for rods_calc in rods_calcs:
                        rods = models.Rod.objects.filter(rods_calc=rods_calc)

                        rods_calc.pk = None
                        rods_calc.element = element
                        rods_calc.save()

                        for rod in rods:
                            rod.pk = None
                            rod.rods_calc = rods_calc
                            rod.save()

    return redirect('calc:profile', username=engineer.username)


def site_delete(request, pk):
    site = models.Site.objects.get(id=pk)
    site.delete()
    return redirect('calc:profile', username=site.engineer.username)


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


def construction_duplicate(request, pk):
    construction = models.Construction.objects.get(pk=pk)
    site = construction.site
    versions = models.Version.objects.filter(construction=construction)

    construction.pk = None
    construction.save()

    for version in versions:
        folders = models.Folder.objects.filter(version=version)

        version.pk = None
        version.construction = construction
        version.save()

        for folder in folders:
            elements = models.Element.objects.filter(folder=folder)

            folder.pk = None
            folder.version = version
            folder.save()

            for element in elements:
                rods_calcs = models.RodsCalc.objects.filter(element=element)

                element.pk = None
                element.folder = folder
                element.save()

                for rods_calc in rods_calcs:
                    rods = models.Rod.objects.filter(rods_calc=rods_calc)

                    rods_calc.pk = None
                    rods_calc.element = element
                    rods_calc.save()

                    for rod in rods:
                        rod.pk = None
                        rod.rods_calc = rods_calc
                        rod.save()

    return redirect('calc:site_detail', site.pk)


def construction_delete(request, pk):
    construction = models.Construction.objects.get(id=pk)
    construction.delete()
    return redirect('calc:site_detail', pk=construction.site.pk)


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
    template_name = 'calc/version/version_create.html'
    model = models.Version
    form_class = forms.VersionForm
    context_object_name = 'version'

    def form_valid(self, form):
        construction = models.Construction.objects.get(
            pk=self.kwargs['construction_pk'],
        )
        construction.save()
        version = form.save(commit=False)
        version.construction = construction
        version.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:version_detail',
                       kwargs={'pk': self.object.pk})


class VersionUpdateView(UpdateView):
    template_name = 'calc/version_update.html'
    Model = models.Version


def version_duplicate(request, pk):
    version = models.Version.objects.get(pk=pk)
    construction = version.construction
    folders = models.Folder.objects.filter(version=version)

    version.pk = None
    version.save()

    for folder in folders:
        elements = models.Element.objects.filter(folder=folder)

        folder.pk = None
        folder.version = version
        folder.save()

        for element in elements:
            rods_calcs = models.RodsCalc.objects.filter(element=element)

            element.pk = None
            element.folder = folder
            element.save()

            for rods_calc in rods_calcs:
                rods = models.Rod.objects.filter(rods_calc=rods_calc)

                rods_calc.pk = None
                rods_calc.element = element
                rods_calc.save()

                for rod in rods:
                    rod.pk = None
                    rod.rods_calc = rods_calc
                    rod.save()

    return redirect('calc:construction_detail', construction.pk)


def version_delete(request, pk):
    version = models.Folder.objects.get(id=pk)
    version.delete()
    return redirect('calc:construction_detail', pk=version.construction.pk)


class FolderDetailView(DetailView):
    template_name = 'calc/folder/folder_detail.html'
    model = models.Folder
    context_object_name = 'folder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder_id = self.kwargs.get('pk')
        context['elements'] = models.Element.objects.filter(
            folder=folder_id)
        return context


class FolderCreateView(CreateView):
    template_name = 'calc/folder/folder_create.html'
    model = models.Folder
    form_class = forms.FolderForm
    context_object_name = 'folder'

    def form_valid(self, form):
        version = models.Version.objects.get(
            pk=self.kwargs['version_pk'],
        )
        version.save()
        folder = form.save(commit=False)
        folder.version = version
        folder.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:folder_detail',
                       kwargs={'pk': self.object.pk})


class FolderUpdateView(UpdateView):
    template_name = 'calc/folder_update.html'
    Model = models.Folder


def folder_duplicate(request, pk):
    folder = models.Folder.objects.get(pk=pk)
    version = folder.version
    elements = models.Element.objects.filter(folder=folder)

    folder.pk = None
    folder.save()

    for element in elements:
        rods_calcs = models.RodsCalc.objects.filter(element=element)

        element.pk = None
        element.folder = folder
        element.save()

        for rods_calc in rods_calcs:
            rods = models.Rod.objects.filter(rods_calc=rods_calc)

            rods_calc.pk = None
            rods_calc.element = element
            rods_calc.save()

            for rod in rods:
                rod.pk = None
                rod.rods_calc = rods_calc
                rod.save()

    return redirect('calc:version_detail', version.pk)


def folder_delete(request, pk):
    folder = models.Folder.objects.get(id=pk)
    folder.delete()
    return redirect('calc:version_detail', pk=folder.version.pk)


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
    template_name = 'calc/element/element_create.html'
    model = models.Element
    form_class = forms.ElementForm
    context_object_name = 'element'

    def form_valid(self, form):
        folder = models.Folder.objects.get(
            pk=self.kwargs['folder_pk'],
        )
        engineer = self.request.user
        folder.save()
        element = form.save(commit=False)
        element.folder = folder
        element.engineer = engineer
        element.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('calc:element_detail',
                       kwargs={'pk': self.object.pk})


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

# class ElementDuplicateView(View):
#     template_name = 'calc/element_duplicate.html'
#     Model = models.Element


def element_duplicate(request, pk):
    element = models.Element.objects.get(id=pk)
    place_folder = element.folder
    rods_calcs = models.RodsCalc.objects.filter(element=element)

    element.pk = None
    element.save()

    for rods_calc in rods_calcs:
        rods = models.Rod.objects.filter(rods_calc=rods_calc)

        rods_calc.pk = None
        rods_calc.element = element
        rods_calc.save()

        for rod in rods:
            rod.pk = None
            rod.rods_calc = rods_calc
            rod.save()

    return redirect('calc:folder_detail', place_folder.pk)


def element_delete(request, pk):
    element = models.Element.objects.get(id=pk)
    element.delete()
    return redirect('calc:folder_detail', pk=element.folder.pk)


class RodsCalcInline:
    form_class = forms.RodsCalcForm
    model = models.RodsCalc
    template_name = 'calc/rods_calc/rods_calc_create.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        rods_calc = form.save(commit=False)
        rods_calc.element.engineer = self.request.user

        rods_calc.save()

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        rods = models.Rod.objects.filter(rods_calc=rods_calc)

        class_mass_dict = {}

        for rod in rods:
            rod_class = rod.rod_class
            mass_of_rods = rod.mass_of_rods

            if rod_class not in class_mass_dict:
                class_mass_dict[rod_class] = mass_of_rods
            else:
                class_mass_dict[rod_class] += mass_of_rods

        for rod_class, total_mass in class_mass_dict.items():
            models.RodClass.objects.create(rods_calc=rods[0].rods_calc,
                                           title=rod_class,
                                           total_mass=total_mass)

        diameter_class_mass_dict = {}

        for rod in rods:
            diameter = rod.diameter
            rod_class = rod.rod_class
            mass_of_rods = rod.mass_of_rods

            if (diameter, rod_class) not in diameter_class_mass_dict:
                diameter_class_mass_dict[(diameter, rod_class)] = mass_of_rods

            else:
                diameter_class_mass_dict[(diameter, rod_class)] += mass_of_rods

        for key, value in diameter_class_mass_dict.items():
            diameter, rod_class = key
            models.RodDiameter.objects.create(
                rod_class=models.RodClass.objects.get(
                    title=rod_class,
                    rods_calc=rods_calc,
                ),
                title=diameter, total_mass=value)

        rod_classes = rods_calc.rod_classes.all()
        rods_calc.total_mass = sum([rc.total_mass for rc in rod_classes])
        rods_calc.save()

        return redirect('calc:landing')

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


def rods_calc_duplicate(request, pk):
    rods_calc = models.RodsCalc.objects.get(pk=pk)
    element = rods_calc.element
    rods = models.Rod.objects.filter(rods_calc=rods_calc)

    rods_calc.pk = None
    rods_calc.save()

    for rod in rods:
        rod.pk = None
        rod.rods_calc = rods_calc
        rod.save()

    return redirect('calc:element_detail', element.pk)


def rods_calc_delete(request, pk):
    rods_calc = models.RodsCalc.objects.get(id=pk)
    rods_calc.delete()
    return redirect('calc:element_detail', pk=rods_calc.element.pk)


def rod_duplicate(request, pk):
    rod = models.Rod.objects.get(pk=pk)

    rod.pk = None
    rod.save()

    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)


def rod_delete(request, pk):
    rod = models.Rod.objects.get(id=pk)
    rod.delete()
    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)


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
