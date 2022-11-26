from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from calc.models import Element, Rod

User = get_user_model()


def element(request, element_id):
    element = get_object_or_404(Element, pk=element_id)
    rods = Rod.objects.filter(element=element)
    context = {
        'element': element,
        'rods': rods,
    }
    return render(request, 'calc/element.html', context)


def result(request, element_id):
    context = {
        element_id: element_id,
    }
    return render(request, 'calc/result.html', context)
