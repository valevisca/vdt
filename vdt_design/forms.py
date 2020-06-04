from django.forms import ModelForm
from .models import Design

class DesignForm(ModelForm):
    class Meta: 
        model = Design
        fields = ['name', 'customer', 'description', 'inputfile']

