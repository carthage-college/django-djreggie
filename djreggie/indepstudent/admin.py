from django.contrib import admin
from models import Independ, FamInfo, Sincome, Studwork, Otherinfo, CS, certification

class Admin(admin.ModelAdmin):
    list_display = ('fname', 'email', 'address',)
    
admin.site.register(Independ, Admin)
admin.site.register(FamInfo)
admin.site.register(Studwork)
admin.site.register(CS)
admin.site.register(Sincome)
admin.site.register(Otherinfo)
admin.site.register(certification)
