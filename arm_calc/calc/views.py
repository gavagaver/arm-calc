from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from calc.models import Element, Rod, RodsCalc
from calc.forms import RodsCalcForm, RodFormSet
from account.models import Folder

User = get_user_model()


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
            rods_calc.element.folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        rods_calc.save()

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('account:list_elements', rods_calc.element.folder.pk)

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


def delete_rod(request, pk):
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


def copy_rod(request, pk):
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


def delete_element(request, pk):
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
            return redirect('account:list_elements', place_folder.pk)
        else:
            return redirect('account:profile', request.user.username)


def copy_element(request, pk):
    try:
        element = Element.objects.get(id=pk)
        place_folder = element.folder
        rods_calcs = RodsCalc.objects.filter(element=element)
    except Element.DoesNotExist:
        messages.error(
            request, 'Такого элемента нет'
        )
        return redirect('account:list_elements', pk=element.folder.pk)
    except RodsCalc.DoesNotExist:
        messages.error(
            request, 'Такого армирования нет'
        )
        return redirect('account:list_elements', pk=element.folder.pk)

    element.pk = None
    element.save()

    for rods_calc in rods_calcs:
        try:
            rods = Rod.objects.filter(rods_calc=rods_calc)
        except Rod.DoesNotExist:
            messages.error(
                request, 'Такого армирования нет'
            )
            return redirect('account:list_elements', pk=element.folder.pk)
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
        return redirect('account:list_elements', place_folder.pk)
    else:
        return redirect('account:profile', request.user.username)
