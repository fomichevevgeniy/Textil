from django import forms
from .models import ClothProductModel

class DropdownModelForm(forms.ModelForm):

    class Meta:
        model = ClothProductModel
        fields = ('material_taked',)
