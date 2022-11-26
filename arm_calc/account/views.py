from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from account.models import Folder
from calc.models import Element

User = get_user_model()


def folder(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    elements = Element.objects.filter(folder=folder)
    context = {
        'folder': folder,
        'elements': elements,
    }
    return render(request, 'account/folder.html', context)
