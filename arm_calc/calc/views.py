from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from calc.models import Element, Rod
from calc.forms import ElementForm, RodFormSet
from account.models import Folder

User = get_user_model()


def result(request, pk):
    element = Element.objects.get(pk=pk)
    rods = Rod.objects.filter(element=element)
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


class ElementInline:
    form_class = ElementForm
    model = Element
    template_name = 'calc/element_create_or_update.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        element = form.save(commit=False)
        element.engineer = self.request.user
        if cache.get('folder_id'):
            element.folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        element.save()

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('account:list_elements', element.folder.pk)

    def formset_rods_valid(self, formset):
        rods = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for rod in rods:
            rod.element = self.object
            rod.save()


class ElementCreate(ElementInline, CreateView):
    def get_context_data(self, **kwargs):
        context = super(ElementCreate, self).get_context_data(**kwargs)
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


class ElementUpdate(ElementInline, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(ElementUpdate, self).get_context_data(**kwargs)
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
        return redirect('calc:update_element', pk=rod.element.id)

    rod.delete()
    messages.success(
        request, 'Стержень успешно удален'
    )
    return redirect('calc:update_element', pk=rod.element.id)


def delete_element(request, element_id):
    element = Element.objects.get(pk=element_id)
    place_folder = element.folder
    if element:
        element.delete()
    if place_folder:
        return redirect('account:list_elements', place_folder.pk)
    else:
        return redirect('account:profile', request.user.username)
