from django import forms
from django.forms import inlineformset_factory

from . import models, calculation_settings


class SiteForm(forms.ModelForm):
    """
    Form for creating or editing a Site object.
    """

    class Meta:
        model = models.Site
        fields = ['title', ]
        labels = {
            'title': 'Укажите название объекта:',
        }


class ConstructionForm(forms.ModelForm):
    """
    Form for creating or editing a Construction object.
    """

    class Meta:
        model = models.Construction
        fields = ['title', ]
        labels = {
            'title': 'Укажите название сооружения:',
        }


class VersionForm(forms.ModelForm):
    """
    Form for creating or editing a Version object.
    """

    class Meta:
        model = models.Version
        fields = ['title', ]
        labels = {
            'title': 'Укажите название стадии:',
        }


class FolderForm(forms.ModelForm):
    """
    Form for creating or editing a Folder object.
    """

    class Meta:
        model = models.Folder
        fields = ['title', ]
        labels = {
            'title': 'Укажите название папки:',

        }


class ElementForm(forms.ModelForm):
    """
    Form for creating or editing an Element object.
    """

    class Meta:
        model = models.Element
        fields = ['title', ]
        labels = {
            'title': 'Укажите название элемента:',
        }


class RodsCalcForm(forms.ModelForm):
    """
    Form for creating or editing a RodsCalc object.
    """

    class Meta:
        model = models.RodsCalc
        fields = ('title', 'measurement_scale')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'measurement_scale': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class RodForm(forms.ModelForm):
    """
    Form for creating or editing a Rod object.
    """

    class Meta:
        model = models.Rod
        exclude = (
            'length',
            'mass_of_single_rod',
            'mass_of_rods',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'diameter': forms.Select(
                choices=calculation_settings.DIAMETERS,
                attrs={
                    'class': 'form-control'
                }
            ),
            'rod_class': forms.Select(
                choices=calculation_settings.ROD_CLASSES,
                attrs={
                    'class': 'form-control'
                }
            ),
            'length_1': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_1': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'length_2': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_2': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'length_3': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_3': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'length_4': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_4': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class RodFormSet(inlineformset_factory):
    """
    Formset for creating or editing multiple Rod objects in RodsCalc object.
    """
    model = models.RodsCalc
    form = RodForm
    extra = 0
    can_delete = False
    can_delete_extra = True
