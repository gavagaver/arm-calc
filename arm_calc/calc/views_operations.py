from django.shortcuts import redirect

from . import models

# Site operations


def site_duplicate(request, pk):
    """
    Duplicate a site object and all of its related constructions,
    versions, folders, elements, rods_calcs, and rods.
    """
    site = models.Site.objects.get(pk=pk)
    engineer = site.engineer
    constructions = models.Construction.objects.filter(site=site)

    site.pk = None
    site.save()

    for construction in constructions:
        versions = models.Version.objects.filter(construction=construction)

        construction.pk = None
        construction.site = site
        construction.save()

        for version in versions:
            folders = models.Folder.objects.filter(version=version)

            version.pk = None
            version.construction = construction
            version.save()

            for folder in folders:
                elements = models.Element.objects.filter(folder=folder)

                folder.pk = None
                folder.version = version
                folder.save()

                for element in elements:
                    rods_calcs = models.RodsCalc.objects.filter(
                        element=element)

                    element.pk = None
                    element.folder = folder
                    element.save()

                    for rods_calc in rods_calcs:
                        rods = models.Rod.objects.filter(rods_calc=rods_calc)

                        rods_calc.pk = None
                        rods_calc.element = element
                        rods_calc.save()

                        for rod in rods:
                            rod.pk = None
                            rod.rods_calc = rods_calc
                            rod.save()

    return redirect('calc:profile', username=engineer.username)


def site_delete(request, pk):
    """
    Delete a site object with the given pk.
    """
    site = models.Site.objects.get(id=pk)
    site.delete()
    return redirect('calc:profile', username=site.engineer.username)


# Construction operations

def construction_duplicate(request, pk):
    """
    Duplicate a construction object and all of its related
    versions, folders, elements, rods_calcs, and rods.
    """
    construction = models.Construction.objects.get(pk=pk)
    site = construction.site
    versions = models.Version.objects.filter(construction=construction)

    construction.pk = None
    construction.save()

    for version in versions:
        folders = models.Folder.objects.filter(version=version)

        version.pk = None
        version.construction = construction
        version.save()

        for folder in folders:
            elements = models.Element.objects.filter(folder=folder)

            folder.pk = None
            folder.version = version
            folder.save()

            for element in elements:
                rods_calcs = models.RodsCalc.objects.filter(element=element)

                element.pk = None
                element.folder = folder
                element.save()

                for rods_calc in rods_calcs:
                    rods = models.Rod.objects.filter(rods_calc=rods_calc)

                    rods_calc.pk = None
                    rods_calc.element = element
                    rods_calc.save()

                    for rod in rods:
                        rod.pk = None
                        rod.rods_calc = rods_calc
                        rod.save()

    return redirect('calc:site_detail', site.pk)


def construction_delete(request, pk):
    """
    Delete a construction object with the given pk.
    """
    construction = models.Construction.objects.get(id=pk)
    construction.delete()
    return redirect('calc:site_detail', pk=construction.site.pk)


# Version operations

def version_duplicate(request, pk):
    """
    Duplicate a version object and all of its related
    folders, elements, rods_calcs, and rods.
    """
    version = models.Version.objects.get(pk=pk)
    construction = version.construction
    folders = models.Folder.objects.filter(version=version)

    version.pk = None
    version.save()

    for folder in folders:
        elements = models.Element.objects.filter(folder=folder)

        folder.pk = None
        folder.version = version
        folder.save()

        for element in elements:
            rods_calcs = models.RodsCalc.objects.filter(element=element)

            element.pk = None
            element.folder = folder
            element.save()

            for rods_calc in rods_calcs:
                rods = models.Rod.objects.filter(rods_calc=rods_calc)

                rods_calc.pk = None
                rods_calc.element = element
                rods_calc.save()

                for rod in rods:
                    rod.pk = None
                    rod.rods_calc = rods_calc
                    rod.save()

    return redirect('calc:construction_detail', construction.pk)


def version_delete(request, pk):
    """
    Delete a version object with the given pk.
    """
    version = models.Version.objects.get(id=pk)
    version.delete()
    return redirect('calc:construction_detail', pk=version.construction.pk)


# Folder operations

def folder_duplicate(request, pk):
    """
    Duplicate a folder object and all of its related
    elements, rods_calcs, and rods.
    """
    folder = models.Folder.objects.get(pk=pk)
    version = folder.version
    elements = models.Element.objects.filter(folder=folder)

    folder.pk = None
    folder.save()

    for element in elements:
        rods_calcs = models.RodsCalc.objects.filter(element=element)

        element.pk = None
        element.folder = folder
        element.save()

        for rods_calc in rods_calcs:
            rods = models.Rod.objects.filter(rods_calc=rods_calc)

            rods_calc.pk = None
            rods_calc.element = element
            rods_calc.save()

            for rod in rods:
                rod.pk = None
                rod.rods_calc = rods_calc
                rod.save()

    return redirect('calc:version_detail', version.pk)


def folder_delete(request, pk):
    """
    Delete a folder object with the given pk.
    """
    folder = models.Folder.objects.get(id=pk)
    folder.delete()
    return redirect('calc:version_detail', pk=folder.version.pk)


# Element operations

def element_duplicate(request, pk):
    """
    Duplicate an element object and all of its related
    rods_calcs, and rods.
    """
    element = models.Element.objects.get(id=pk)
    place_folder = element.folder
    rods_calcs = models.RodsCalc.objects.filter(element=element)

    element.pk = None
    element.save()

    for rods_calc in rods_calcs:
        rods = models.Rod.objects.filter(rods_calc=rods_calc)

        rods_calc.pk = None
        rods_calc.element = element
        rods_calc.save()

        for rod in rods:
            rod.pk = None
            rod.rods_calc = rods_calc
            rod.save()

    return redirect('calc:folder_detail', place_folder.pk)


def element_delete(request, pk):
    """
    Delete a element object with the given pk.
    """
    element = models.Element.objects.get(id=pk)
    element.delete()
    return redirect('calc:folder_detail', pk=element.folder.pk)


# Rods Calc operations

def rods_calc_duplicate(request, pk):
    """
    Duplicate a rods_calc object and all of its related rods.
    """
    rods_calc = models.RodsCalc.objects.get(pk=pk)
    element = rods_calc.element
    rods = models.Rod.objects.filter(rods_calc=rods_calc)

    rods_calc.pk = None
    rods_calc.save()

    for rod in rods:
        rod.pk = None
        rod.rods_calc = rods_calc
        rod.save()

    return redirect('calc:element_detail', element.pk)


def rods_calc_delete(request, pk):
    """
    Delete a rods_calc object with the given pk.
    """
    rods_calc = models.RodsCalc.objects.get(id=pk)
    rods_calc.delete()
    return redirect('calc:element_detail', pk=rods_calc.element.pk)


# Rod operations

def rod_duplicate(request, pk):
    """
    Duplicate a rod object.
    """
    rod = models.Rod.objects.get(pk=pk)

    rod.pk = None
    rod.save()

    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)


def rod_delete(request, pk):
    """
    Delete a rod object with the given pk.
    """
    rod = models.Rod.objects.get(id=pk)
    rod.delete()
    return redirect('calc:rods_calc_update', pk=rod.rods_calc.pk)
