from django.contrib import admin
from djreggie.depstudent.models import Depend, FamInfo, Studwork, Parwork, CS

class Admin(admin.ModelAdmin):
    list_display = ('fname', 'email', 'address',)
    
admin.site.register(Depend, Admin)
admin.site.register(FamInfo)
admin.site.register(Studwork)
admin.site.register(Parwork)
admin.site.register(CS)
#admin.site.register(Sincome)
#admin.site.register(Parincome)
#admin.site.register(Otherinfo)
#admin.site.register(certification)
