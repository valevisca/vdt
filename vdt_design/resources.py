from import_export import resources
from .models import Pid

class PidResource(resources.ModelResource):
    class Meta:
        model = Pid
        fields = ['sname', 'pidtype', 'name', 'description', 'cogs', 'gpl', 'discount', 
                    'netprice', 'power_typ', 'power_max', 'mtbf']