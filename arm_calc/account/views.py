from django.contrib.auth import get_user_model
from django.shortcuts import render

from calc.models import Element

User = get_user_model()


def folder(request):
    elements = Element.objects.all()
    context = {
        'elements': elements,
    }
    return render(request, 'account/folder.html', context)
