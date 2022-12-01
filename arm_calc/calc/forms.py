from django import forms
from django.forms import inlineformset_factory

from calc.models import Element, Rod


class ElementForm(forms.ModelForm):
    class Meta:
        model = Element
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class RodForm(forms.ModelForm):
    class Meta:
        model = Rod
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'diameter': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'arm_class': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'length': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


RodFormSet = inlineformset_factory(
    Element, Rod, form=RodForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
