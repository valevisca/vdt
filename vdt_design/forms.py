from django.forms import ModelForm
from .models import Design, Pid

class DesignForm(ModelForm):
    class Meta: 
        model = Design
        fields = ['name', 'customer', 'description', 'inputfile']

class PidForm(ModelForm):
    class Meta: 
        model = Pid
        fields = ['sname', 'pidtype', 'name', 'description', 'cogs', 'gpl', 'discount', 
                    'netprice', 'power_typ', 'power_max', 'mtbf']