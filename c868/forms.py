from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models as models
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.CustomUser
        fields = ("email", 'role')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.CustomUser
        fields = ("email", 'role')

class CreatePartForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['name',
        'sku',
        'source',
        'source_id',
        'inventory',
        'price',
        'max_inventory',
        'min_inventory',]

    def clean(self):
        cleaned_data = super().clean()
        max_inventory = cleaned_data.get('max_inventory')
        min_inventory = cleaned_data.get('min_inventory')
        inventory = cleaned_data.get('inventory')
        if max_inventory <= min_inventory:
            raise forms.ValidationError('Max inventory must be greater than min inventory.')
        if inventory > max_inventory:
            raise forms.ValidationError('Inventory is larger than max inventory.')
        if inventory < min_inventory:
            raise forms.ValidationError('Inventory is less than min inventory.')
        return cleaned_data

class CreateSubPartForm(CreatePartForm):
    class Meta:
        model = models.Part
        fields = ['name',
        'sku',
        'source',
        'source_id',
        'inventory',
        'price',
        'max_inventory',
        'min_inventory',]
    
    parent_pk = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, parent_pk, *args, **kwargs):
        kwargs.update(initial={
            'parent_pk': parent_pk
        })
        super().__init__(*args, **kwargs)

class EditPartForm(CreatePartForm):
    pass