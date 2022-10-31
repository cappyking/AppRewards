from django import forms
from .models import AppLib, MasterTaskHolder


class appadd(forms.ModelForm):
    class Meta:
        model = AppLib
        fields = ['title', 'point', 'category']


class imageadd(forms.ModelForm):
    class Meta:
        model = MasterTaskHolder
        fields = ['image']
