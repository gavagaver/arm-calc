from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from calc.models import Element, Rod
from calc.forms import ElementForm, RodFormSet

User = get_user_model()


def result(request, pk):
    element = Element.objects.get(pk=pk)
    rods = Rod.objects.filter(element=element)
    """arm_classes = sorted(
        list(set(rods.values_list('arm_class', flat=True).distinct()))
    )"""
    results = {
        'А240': {'Ø16': 71.5, 'Ø12': 340.9, 'Ø8': 227.5, 'Итого': 500},
        'А500С': {'Ø12': 77.3, 'Ø10': 320.4, 'Ø8': 257.3, 'Итого': 1500},
    }
    sum_element = 2000.0
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

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('account:list_elements')

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
            request, 'Object Does not exit'
        )
        return redirect('calc:update_element', pk=rod.element.id)

    rod.delete()
    messages.success(
        request, 'Rod deleted successfully'
    )
    return redirect('calc:update_element', pk=rod.element.id)
