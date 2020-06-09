from django.contrib import admin

# Register your models here.
# First we have to import the module 'Project' into admin.py
from .models import Design, Pid


# The following class define some readonly fields which are then reported in the
# Admin web page. In particular we are presenting the 'datecreated'
class DesignAdmin(admin.ModelAdmin):
    readonly_fields = ('datecreated',)

# Then we have to register it 
admin.site.register(Design, DesignAdmin)
admin.site.register(Pid)