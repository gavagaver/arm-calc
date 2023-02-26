from django.contrib.auth import get_user_model
from django.shortcuts import render

from calc.models import Element
from account.models import Folder

User = get_user_model()


def landing(request):
    context = {}
    return render(request, 'account/landing.html', context)


def folder(request, pk):
    folder = Folder.objects.get(pk=pk)
    elements = folder.elements.all()
    context = {
        'folder': folder,
        'elements': elements,
    }
    return render(request, 'account/folder.html', context)
