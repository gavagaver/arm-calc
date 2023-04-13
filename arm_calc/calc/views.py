from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
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


@login_required
class ProfileView(ListView):
    template_name = 'calc/profile.html'
    model = models.Site
    context_object_name = 'sites'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(engineer=self.request.user)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def site_delete(request, pk):
    site = models.Site.objects.get(id=pk)
    site.delete()
    return redirect('calc:profile', username=site.engineer.username)


@login_required
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


@login_required
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


@login_required
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

    def get_success_url(self):
        site = self.get_object().site
        return reverse('calc:site_detail', args=[site.pk])


@login_required
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


@login_required
def construction_delete(request, pk):
    construction = models.Construction.objects.get(id=pk)
    construction.delete()
    return redirect('calc:site_detail', pk=construction.site.pk)


@login_required
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


@login_required
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


@login_required
class VersionUpdateView(UpdateView):
    template_name = 'calc/version/version_create.html'
    model = models.Version
    form_class = forms.VersionForm

    def form_valid(self, form):
        construction = self.get_object().construction
        version = form.save(commit=False)
        version.construction = construction
        version.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.__class__.__name__ == 'VersionUpdateView':
            context['view_name'] = 'update'
        return context

    def get_success_url(self):
        construction = self.get_object().construction
        return reverse('calc:construction_detail', args=[construction.pk])


@login_required
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


@login_required
def version_delete(request, pk):
    version = models.Version.objects.get(id=pk)
    version.delete()
    return redirect('calc:construction_detail', pk=version.construction.pk)


@login_required
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


@login_required
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


@login_required
class FolderUpdateView(UpdateView):
    template_name = 'calc/folder/folder_create.html'
    model = models.Folder
    form_class = forms.FolderForm

    def form_valid(self, form):
        version = self.get_object().version
        folder = form.save(commit=False)
        folder.version = version
        folder.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.__class__.__name__ == 'FolderUpdateView':
            context['view_name'] = 'update'
        return context

    def get_success_url(self):
        version = self.get_object().version
        return reverse('calc:version_detail', args=[version.pk])


@login_required
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


@login_required
def folder_delete(request, pk):
    folder = models.Folder.objects.get(id=pk)
    folder.delete()
    return redirect('calc:version_detail', pk=folder.version.pk)


@login_required
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


@login_required
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


@login_required
class ElementUpdateView(UpdateView):
    template_name = 'calc/element/element_create.html'
    model = models.Element
    form_class = forms.ElementForm

    def form_valid(self, form):
        folder = self.get_object().folder
        element = form.save(commit=False)
        element.folder = folder
        element.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        folder = self.get_object().folder
        return reverse('calc:folder_detail', args=[folder.pk])


@login_required
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


@login_required
def element_delete(request, pk):
    element = models.Element.objects.get(id=pk)
    element.delete()
    return redirect('calc:folder_detail', pk=element.folder.pk)


@login_required
class RodsCalcInline:
    form_class = forms.RodsCalcForm
    model = models.RodsCalc
    template_name = 'calc/rods_calc/rods_calc_create.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        rods_calc = form.save(commit=False)
        try:
            element_pk = self.kwargs['element_pk']
        except KeyError:
            element_pk = rods_calc.element.pk
        element = models.Element.objects.get(pk=element_pk)
        rods_calc.element = element
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
            try:
                rod_class_object = models.RodClass.objects.get(rods_calc=rods[0].rods_calc, title=rod_class)
                rod_class_object.total_mass = total_mass
                rod_class_object.save()
            except Exception:
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
            diameter, rod_class_title = key
            rod_class = models.RodClass.objects.filter(
                title=rod_class_title,
                rods_calc=rods_calc,
            ).order_by('-create_date').first()

            try:
                rod_diameter_object = models.RodDiameter.objects.get(rod_class=rod_class, title=diameter)
                rod_diameter_object.total_mass = value
                rod_diameter_object.save()
            except Exception:
                models.RodDiameter.objects.create(
                    rod_class=rod_class,
                    title=diameter,
                    total_mass=value
                )

        rod_classes = rods_calc.rod_classes.all()
        rods_calc.total_mass = sum([rc.total_mass for rc in rod_classes])
        rods_calc.save()

        return redirect('calc:rods_calc_update', rods_calc.pk)

    def formset_rods_valid(self, formset):
        rods = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for rod in rods:
            rod.rods_calc = self.object
            rod.save()


@login_required
class RodsCalcCreateView(RodsCalcInline, CreateView):
    def get_context_data(self, **kwargs):
        context = super(RodsCalcCreateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        element_pk = self.kwargs['element_pk']
        context['element'] = models.Element.objects.get(pk=element_pk)
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


@login_required
class RodsCalcUpdateView(RodsCalcInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(RodsCalcUpdateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        rods_calc_pk = self.kwargs['pk']
        rods_calc = models.RodsCalc.objects.get(pk=rods_calc_pk)
        context['rods_calc'] = rods_calc
        context['element'] = rods_calc.element
        if self.__class__.__name__ == 'RodsCalcUpdateView':
            context['view_name'] = 'update'
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


@login_required
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


@login_required
def rods_calc_delete(request, pk):
    rods_calc = models.RodsCalc.objects.get(id=pk)
    rods_calc.delete()
    return redirect('calc:element_detail', pk=rods_calc.element.pk)


@login_required
def rod_duplicate(request, pk):
    rod = models.Rod.objects.get(pk=pk)

    rod.pk = None
    rod.save()

    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)


@login_required
def rod_delete(request, pk):
    rod = models.Rod.objects.get(id=pk)
    rod.delete()
    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)


@login_required
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
