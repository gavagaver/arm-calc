from django import forms
from django.forms import inlineformset_factory

from . import calculation_settings, models


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
        fields = ('title', 'quantity')
        widgets = {
            'title': forms.TextInput(
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


class RodForm(forms.ModelForm):
    """
    Form for creating or editing a Rod object.
    """

    class Meta:
        model = models.Rod
        exclude = (
            'length',
            'quantity',
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
            'quantity_a': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_b': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_c': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


RodFormSet = inlineformset_factory(
    models.RodsCalc, models.Rod, form=RodForm,
    extra=0, can_delete=False,
    can_delete_extra=True
)


class VolumesCalcForm(forms.ModelForm):
    """
    Form for creating or editing a VolumesCalc object.
    """

    class Meta:
        model = models.VolumesCalc
        fields = ('title', 'quantity')
        widgets = {
            'title': forms.TextInput(
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


class VolumeForm(forms.ModelForm):
    """
    Form for creating or editing a Volume object.
    """

    class Meta:
        model = models.Volume
        exclude = (
            'quantity',
            'volume_of_single_volume',
            'volume_of_volumes',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'is_hole': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
            'length': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'width': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'height': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_a': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_b': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'quantity_c': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


VolumeFormSet = inlineformset_factory(
    models.VolumesCalc, models.Volume, form=VolumeForm,
    extra=0, can_delete=False,
    can_delete_extra=True
)
