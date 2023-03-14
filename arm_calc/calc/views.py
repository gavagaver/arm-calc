from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, \
    DeleteView

from calc.models import Folder, Element, Rod, RodsCalc
from calc.forms import FolderForm, ElementForm, RodsCalcForm, RodFormSet

User = get_user_model()


def landing(request):
    context = {}
    return render(request, 'calc/landing.html', context)


def profile(request, username):
    engineer = get_object_or_404(User, username=username)
    folders = engineer.folders.filter(folder=None)
    elements = engineer.elements.filter(folder=None)
    context = {
        'engineer': engineer,
        'folders': folders,
        'elements': elements,
    }
    return render(request, 'calc/profile.html', context)


def result(request, pk):
    element = Element.objects.get(pk=pk)
    rods_calc = RodsCalc.objects.get(element=element)
    rods = Rod.objects.filter(rods_calc=rods_calc)
    arm_classes = sorted(
        list(set(rods.values_list('arm_class', flat=True).distinct()))
    )
    results = {}
    for clas in arm_classes:
        diameters = sorted(list(set(
            rods.filter(arm_class=clas).values_list('diameter',
                                                    flat=True
                                                    ).distinct()
        )))
        masses = []
        for diameter in diameters:
            all_rods_of_diameter = rods.filter(diameter=diameter,
                                               arm_class=clas)
            masses_of_diameter = []
            for rod in all_rods_of_diameter:
                mass = rod.mass_of_rods()
                masses_of_diameter.append(mass)
            masses.append(round(sum(masses_of_diameter), 2))

        diameters = list(map(lambda x: '⌀' + str(x), diameters))
        diameters.append('Итого')
        masses.append(round(sum(masses), 2))

        dictionary = dict(zip(diameters, masses))
        results[clas] = dictionary

    masses_of_rods = []
    for rod in rods:
        mass_of_rod = rod.mass_of_rods()
        masses_of_rods.append(mass_of_rod)

    sum_element = round(sum(masses_of_rods), 2)
    context = {
        'element': element,
        'rods': rods,
        'results': results,
        'sum_element': sum_element,
    }
    return render(request, 'calc/result.html', context)


def site(request, pk):
    pass


def site_create(request):
    pass


def site_update(request, pk):
    pass


def site_duplicate(request, pk):
    pass


def site_delete(request, pk):
    pass


def construction(request, pk):
    pass


def construction_create(request):
    pass


def construction_update(request, pk):
    pass


def construction_duplicate(request, pk):
    pass


def construction_delete(request, pk):
    pass


def version(request, pk):
    pass


def version_create(request):
    pass


def version_update(request, pk):
    pass


def version_duplicate(request, pk):
    pass


def version_delete(request, pk):
    pass


def folder(request, pk):
    folder = Folder.objects.get(pk=pk)
    folders = Folder.objects.filter(folder=folder)
    elements = folder.elements.all()
    context = {
        'folder': folder,
        'folders': folders,
        'elements': elements,
    }
    cache.set('folder_id', str(pk))
    return render(request, 'calc/folder.html', context)


def folder_create(request):
    form = FolderForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        engineer = request.user
        folder = form.save(commit=False)
        folder.engineer = request.user
        try:
            folder.folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        except:
            pass
        folder.save()
        return redirect('calc:folder', folder.pk)
    context = {
        'form': form,
    }
    return render(request, 'calc/create_folder.html', context)


def folder_update(request, pk):
    pass


def folder_duplicate(request, pk):
    pass


def folder_delete(request, pk):
    folder = Folder.objects.get(pk=pk)
    place_folder = folder.folder
    if folder:
        folder.delete()
    if place_folder:
        return redirect('calc:folder', place_folder.pk)
    else:
        return redirect('calc:profile', request.user.username)


def element(request, pk):
    pass


def element_create(request):
    form = ElementForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        engineer = request.user
        if cache.get('folder_id'):
            folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        element = form.save(commit=False)
        element.engineer = request.user
        if cache.get('folder_id'):
            element.folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        else:
            element.save()
            return redirect('calc:profile', request.user.username)
        element.save()
        if folder:
            return redirect('calc:folder', folder.pk)
    context = {
        'form': form,
    }
    return render(request, 'calc/create_element.html', context)


def element_update(request, pk):
    updated_element = get_object_or_404(Element, pk=pk)
    if request.user != updated_element.engineer:
        return redirect('calc:profile', request.user.username)
    form = ElementForm(
        request.POST or None,
        files=request.FILES or None,
        instance=updated_element,
    )
    if form.is_valid():
        form.save()
        return redirect('calc:profile', request.user.username)
    context = {'form': form, }
    return render(request, 'calc/create_element.html', context)


def element_duplicate(request, pk):
    try:
        element = Element.objects.get(id=pk)
        place_folder = element.folder
        rods_calcs = RodsCalc.objects.filter(element=element)
    except Element.DoesNotExist:
        messages.error(
            request, 'Такого элемента нет'
        )
        return redirect('calc:folder', pk=element.folder.pk)
    except RodsCalc.DoesNotExist:
        messages.error(
            request, 'Такого армирования нет'
        )
        return redirect('calc:folder', pk=element.folder.pk)

    element.pk = None
    element.save()

    for rods_calc in rods_calcs:
        try:
            rods = Rod.objects.filter(rods_calc=rods_calc)
        except Rod.DoesNotExist:
            messages.error(
                request, 'Такого армирования нет'
            )
            return redirect('calc:folder', pk=element.folder.pk)
        rods_calc.pk = None
        rods_calc.element = element
        rods_calc.save()

        for rod in rods:
            rod.pk = None
            rod.rods_calc = rods_calc
            rod.save()

    messages.success(
        request, 'Элемент успешно скопирован'
    )
    if place_folder:
        return redirect('calc:folder', place_folder.pk)
    else:
        return redirect('calc:profile', request.user.username)


def element_delete(request, pk):
    element = Element.objects.get(pk=pk)
    place_folder = element.folder
    rods_calcs = RodsCalc.objects.filter(element=element)
    for rods_calc in rods_calcs:
        rods = Rod.objects.filter(rods_calc=rods_calc)
        if element:
            element.delete()
        for rod in rods:
            if rods:
                rod.delete()
        if place_folder:
            return redirect('calc:folder', place_folder.pk)
        else:
            return redirect('calc:profile', request.user.username)


class RodsCalcDetail(TemplateView):
    pass


class RodsCalcInline:
    form_class = RodsCalcForm
    model = RodsCalc
    template_name = 'calc/element_create_or_update.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        rods_calc = form.save(commit=False)
        rods_calc.element.engineer = self.request.user
        if cache.get('folder_id'):
            rods_calc.element.folder = Folder.objects.get(
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


class RodsCalcCreate(RodsCalcInline, CreateView):
    def get_context_data(self, **kwargs):
        context = super(RodsCalcCreate, self).get_context_data(**kwargs)
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


class RodsCalcUpdate(RodsCalcInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(RodsCalcUpdate, self).get_context_data(**kwargs)
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


def rods_calc_duplicate(request, pk):
    pass


class RodsCalcDelete(RodsCalcInline, DeleteView):
    pass


def rod_duplicate(request, pk):
    try:
        rod = Rod.objects.get(id=pk)
    except Rod.DoesNotExist:
        messages.success(
            request, 'Такого стержня нет'
        )
        return redirect('calc:update_element', pk=rod.rods_calc.element.id)

    rod.pk = None
    rod.save()
    messages.success(
        request, 'Стержень успешно скопирован'
    )
    return redirect('calc:update_element', pk=rod.rods_calc.element.id)


def rod_delete(request, pk):
    try:
        rod = Rod.objects.get(id=pk)
    except Rod.DoesNotExist:
        messages.success(
            request, 'Такого стержня нет'
        )
        return redirect('calc:update_element', pk=rod.rods_calc.element.id)

    rod.delete()
    messages.success(
        request, 'Стержень успешно удален'
    )
    return redirect('calc:update_element', pk=rod.rods_calc.element.id)


class VolumesCalcDetail(TemplateView):
    pass


class VolumesCalcCreate(CreateView):
    pass


class VolumesCalcUpdate(RodsCalcInline, UpdateView):
    pass


def volumes_calc_duplicate(request, pk):
    pass


class VolumesCalcDelete(DeleteView):
    pass


def volume_duplicate(request, pk):
    pass


def volume_delete(request, pk):
    pass


class SquaresCalcDetail(TemplateView):
    pass


class SquaresCalcCreate(CreateView):
    pass


class SquaresCalcUpdate(UpdateView):
    pass


def squares_calc_duplicate(request, pk):
    pass


class SquaresCalcDelete(DeleteView):
    pass


def square_duplicate(request, pk):
    pass


def square_delete(request, pk):
    pass


class LengthsCalcDetail(TemplateView):
    pass


class LengthsCalcCreate(CreateView):
    pass


class LengthsCalcUpdate(UpdateView):
    pass


def lengths_calc_duplicate(request, pk):
    pass


class LengthsCalcDelete(DeleteView):
    pass


def length_duplicate(request, pk):
    pass


def length_delete(request, pk):
    pass


class UnitsCalcDetail(TemplateView):
    pass


class UnitsCalcCreate(CreateView):
    pass


class UnitsCalcUpdate(UpdateView):
    pass


def units_calc_duplicate(request, pk):
    pass


class UnitsCalcDelete(DeleteView):
    pass


def unit_duplicate(request, pk):
    pass


def unit_delete(request, pk):
    pass
