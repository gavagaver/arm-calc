from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)

from . import calculation_settings, forms, models

User = get_user_model()


class LandingView(TemplateView):
    """
    A view that renders the landing page template.
    """
    template_name = 'calc/landing.html'


class ProfileView(ListView):
    """
    A view that renders the profile page template and displays a list of sites
    associated with the logged-in engineer.
    """
    template_name = 'calc/profile.html'
    model = models.Site
    context_object_name = 'sites'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(engineer=self.request.user)


class SiteDetailView(DetailView):
    """
    A view that renders the site detail page template and displays information
    about a specific site.
    """
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
    """
    A view that renders the site create page template
    and handles the creation of a new site.
    """
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
    """
    A view that renders the site update page template
    and handles the updating of an existing site.
    """
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


class ConstructionDetailView(DetailView):
    """
    A view that renders the construction detail page template
    and displays information about a specific construction.
    """
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
    """
    A view that renders the construction create page template
    and handles the creation of a new construction.
    """
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
    """
    A view that renders the construction update page template
    and handles the updating of an existing construction.
    """
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


class VersionDetailView(DetailView):
    """
    A view that renders the version detail page template and displays
    information about a specific version.
    """
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
    """
    A view that renders the version create page template
    and handles the creation of a new version.
    """
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
    """
    A view that renders the version update page template
    and handles the updating of an existing version.
    """
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


class FolderDetailView(DetailView):
    """
    A view that renders the folder detail page template and displays
    information about a specific folder.
    """
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
    """
    A view that renders the folder create page template
    and handles the creation of a new folder.
    """
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
    """
    A view that renders the folder update page template
    and handles the updating of an existing folder.
    """
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


class ElementDetailView(DetailView):
    """
    A view that renders the element detail page template and displays
    information about a specific element.
    """
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
    """
    A view that renders the element create page template
    and handles the creation of a new element.
    """
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
    """
    A view that renders the element update page template
    and handles the updating of an existing element.
    """
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
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        folder = self.get_object().folder
        return reverse('calc:folder_detail', args=[folder.pk])


class RodsCalcInline:
    form_class = forms.RodsCalcForm
    model = models.RodsCalc
    template_name = 'calc/rods_calc/rods_calc_create.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        # formset validation. If not successful, then render the formset again
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        # set rods_calc to which element it belongs
        rods_calc = form.save(commit=False)
        try:
            element_pk = self.kwargs['element_pk']
        except KeyError:
            element_pk = rods_calc.element.pk
        element = models.Element.objects.get(pk=element_pk)
        rods_calc.element = element
        rods_calc.save()
        self.object = form.save()

        # find specific save function for every formset or save
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        # calculate the rods_calc
        rods = models.Rod.objects.filter(rods_calc=rods_calc)

        # calculate the mass of the reinforcement of each class
        class_mass_dict = {}

        for rod in rods:
            rod_class = rod.rod_class
            mass_of_rods = rod.mass_of_rods

            if rod_class not in class_mass_dict:
                class_mass_dict[rod_class] = mass_of_rods
            else:
                class_mass_dict[rod_class] += mass_of_rods

        # save the mass of the reinforcement of each class in database
        for rod_class, total_mass in class_mass_dict.items():
            try:
                rod_class_object = models.RodClass.objects.get(
                    rods_calc=rods[0].rods_calc,
                    title=rod_class
                )
                rod_class_object.total_mass = total_mass
                rod_class_object.save()
            except Exception:
                models.RodClass.objects.create(
                    rods_calc=rods[0].rods_calc,
                    title=rod_class,
                    total_mass=total_mass,
                )

        # calculate the mass of the reinforcement of each diameter and class
        diameter_class_mass_dict = {}

        for rod in rods:
            diameter = rod.diameter
            rod_class = rod.rod_class
            mass_of_rods = rod.mass_of_rods

            if (diameter, rod_class) not in diameter_class_mass_dict:
                diameter_class_mass_dict[(diameter, rod_class)] = mass_of_rods

            else:
                diameter_class_mass_dict[(diameter, rod_class)] += mass_of_rods

        # save the mass of the reinforcement of each class in database
        for key, value in diameter_class_mass_dict.items():
            diameter, rod_class_title = key
            rod_class = models.RodClass.objects.filter(
                title=rod_class_title,
                rods_calc=rods_calc,
            ).order_by('-create_date').first()

            try:
                rod_diameter_object = models.RodDiameter.objects.get(
                    rod_class=rod_class,
                    title=diameter
                )
                rod_diameter_object.total_mass = value
                rod_diameter_object.save()
            except Exception:
                models.RodDiameter.objects.create(
                    rod_class=rod_class,
                    title=diameter,
                    total_mass=value
                )

        # calculate total mass of rods_calc and save
        rod_classes = rods_calc.rod_classes.all()
        rods_calc.total_mass = round(
            sum([rc.total_mass for rc in rod_classes]),
            calculation_settings.NUM_OF_DECIMALS,
        )
        rods_calc.save()

        return redirect('calc:rods_calc_update', rods_calc.pk)

    def formset_rods_valid(self, formset):
        rods = formset.save(commit=False)
        for rod in rods:
            rod.rods_calc = self.object
            rod.save()


class RodsCalcCreateView(RodsCalcInline, CreateView):
    """
    A view that renders the rods_calc create page template
    and handles the creation of a new rods_calc.
    """
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
        return {
            'rods': forms.RodFormSet(
                self.request.POST or None,
                self.request.FILES or None,
                prefix='rods'
            ),
        }


class RodsCalcUpdateView(RodsCalcInline, UpdateView):
    """
    A view that renders the rods_calc update page template
    and handles the updating of an existing rods_calc.
    """
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


class RodsCalcResultView(DetailView):
    """
    A view that renders the results page of rods_calc.
    """
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
        context['rod_diameters'] = rod_diameters
        context['rods'] = models.Rod.objects.filter(
            rods_calc=rods_calc_id)
        return context
