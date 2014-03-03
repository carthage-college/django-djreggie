#admin.py is where we create 'actions' that users can do to entries
#within this app, consentfam, as well as settings to change how
#we view entries within 'consentfam'

#'admin' - necessary to change view settings when viewing a 'consentfam' object
from django.contrib import admin
from djreggie.consentfam.models import ConsentModel, ParentForm
#from asdf import FinprivRec

#asdf is a a file that used to hold a database table called FinprivRec which was used for the consentfam form because of the unique fields in it.

#This is an 'action' a user can perform to a 'consentfam' object
def push_to_production(modeladmin, request, queryset):
    #for item in queryset:
    #    FinprivRec.objects.using('productiondefault').get_or_create(id=item.Carthage_ID_Number, code_name=item.name)
        
    push_to_production.short_description = "Approve for moving to another database"    #The description that shows up on the page saying what the action does.

class Admin(admin.ModelAdmin):
    list_display = ('Carthage_ID_Number',) #We will only see the following fields as columns in the admin page
    actions = [push_to_production] #Includes the action we defined earlier in this page    
    search_fields = ['Carthage_ID_Number']
    
    
admin.site.register(ConsentModel, Admin) #Always be sure to add the model before adding the admin class
admin.site.register(ParentForm) #Only one model and an admin class can be associated with a call to register. If you have more models, make more calls.
