from django import forms
from django.forms import inlineformset_factory

from calc.models import Element, Rod


class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        exclude = ('engineer', 'folder',)
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
    class Meta:
        model = Rod
        fields = '__all__'
        DIAMETERS = (
            ('6', '6'),
            ('8', '8'),
            ('10', '10'),
            ('12', '12'),
            ('14', '14'),
            ('16', '16'),
            ('18', '18'),
            ('20', '20'),
            ('22', '22'),
            ('25', '25'),
            ('28', '28'),
            ('32', '32'),
            ('36', '36'),
            ('40', '40'),
        )
        ARM_CLASSES = (
            ('А240', 'А240'),
            ('А400', 'А400'),
            ('А500', 'А500'),
            ('А600', 'А600'),
            ('А800', 'А800'),
            ('А1000', 'А1000'),
        )
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'diameter': forms.Select(
                choices=DIAMETERS,
                attrs={
                    'class': 'form-control'
                }
            ),
            'arm_class': forms.Select(
                choices=ARM_CLASSES,
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


RodFormSet = inlineformset_factory(
    Element, Rod, form=RodForm,
    extra=1, can_delete=False,
    can_delete_extra=True
)
