from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect

from calc.models import Element
from account.models import Folder
from .forms import FolderForm

User = get_user_model()


def landing(request):
    context = {}
    return render(request, 'account/landing.html', context)


def folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    folders = Folder.objects.filter(folder=folder)
    elements = folder.elements.all()
    context = {
        'folder': folder,
        'folders': folders,
        'elements': elements,
    }
    cache.set('folder_id', str(folder_id))
    return render(request, 'account/folder.html', context)


def delete_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    place_folder = folder.folder
    for inner_folder in folder.folders.all():
        if inner_folder:
            inner_folder.delete()
    if folder:
        folder.delete()
    if place_folder:
        return redirect('account:list_elements', place_folder.pk)
    else:
        return redirect('account:profile', request.user.username)


def create_folder(request):
    form = FolderForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        engineer = request.user
        folder = form.save(commit=False)
        folder.engineer = request.user
        if cache.get('folder_id'):
            folder.folder = Folder.objects.get(pk=int(cache.get('folder_id')))
            cache.clear()
        folder.save()
        return redirect('account:list_elements', folder.pk)
    context = {
        'form': form,
    }
    return render(request, 'account/create_folder.html', context)


def profile(request, username):
    engineer = get_object_or_404(User, username=username)
    folders = engineer.folders.filter(folder=None)
    elements = engineer.elements.filter(folder=None)
    context = {
        'engineer': engineer,
        'folders': folders,
        'elements': elements,
    }
    return render(request, 'account/profile.html', context)
