from django import forms
from .models import Purchase
from django.contrib.auth.models import User

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

#class CreationForm(forms.ModelForm):
#    class Meta:
#        model = User