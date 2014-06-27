#admin.py is where we create 'actions' that users can do to entries
#within this app, changemajor, as well as settings to change how
#we view entries within 'changemajor'

#'admin' - necessary to change view settings when viewing an 'changemajor' object
#'messages' - necessary to change success/fail messages when performing an action to an 'changemajor' object
from django.contrib import admin, messages
from djreggie.changemajor.models import ChangeModel
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
#from Production.models import AaRec, AcadRec, IdRec, ProgramEnrollRec

'''This is an 'action' a user can perform to a 'changemajor' object
def push_to_production(modeladmin, request, queryset):
    push_to_production.short_description = 'Push to production server' #What the user sees
    #SQL Alchemy
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    for row in queryset:
            adv = row.advisor.split(' ')
            sql = "UPDATE prog_enr_rec SET major1 = '%s', major2 = '%s', major3 = '%s', minor1 = '%s', minor2 = '%s', minor3 = '%s', adv_id = {SELECT id FROM id_rec WHERE firstname = '%s' AND lastname = '%s'} WHERE id = %d" % (row.majors[0].txt, row.majors[1].txt, row.majors[2].txt, row.minors[0].txt, row.minors[1].txt, row.minors[2].txt, row.student_id, adv[0], adv[1])
            connection.execute(sql)
    # This is the bulk of moving data from the development to production databases
    #
    # *Understand this first - The data that exists in the form will be moved to separate
    # tables in the production server. Some fields might be moved to table 'A', others to table
    # 'B', and the rest might go to table 'C'. 
    # 
    # Steps to accomplish this:
    # 1) Find all of the tables where your data will be moving when it goes to the production
    # server. 
    #
    # 2) Download MySQLWorkbench and make copies of the tables on your local machine you found in step 1.
    # Be sure to copy the structure of the table exactly as found on the production server (including the name of the table)
    #
    # 3) Run this command and be sure 'newmodels.py' has been created in your project
    # (Run the command while within the 'root' project folder on your local machine. This
    # assumes you have been developing the form on your local machine)
    #       python manage.py inspectdb --database=default2 > newmodels.py
    #
    #   *Note: 'default2' is the name of your database where you have created the tables in
    #   step 2. This database should be a copy of the production database on the server (at the very least a copy of the tables you will need from step 1)
    #   This is found in the project's 'settings.py' file
    #
    # 4) On the top of this page, import the 'newmodels.py' file
    #
    # 5) Look in 'newmodels.py', you will see a bunch of classes. Each class represents a 
    # table. Now look at the fields in each class. For the below sample code, assume you had two classes
    # in 'newmodels.py' named 'table_one' and 'table_two'
    #
    #   'table_one' has these fields:
    #       id, name, tel
    #
    #   'table_two' has these fields:
    #       id, address
    #
    #   Also assume that your form has these fields:
    #       my_id, form, phone_number
    #
    # 6) For each class, use some code like below to save the data to your production database (keep this code in the function this comment is in)
    # *Note: replace 'default2' with the name YOU used for your production database (in 'settings.py')
    # *Note: feel free to un-comment the code below and make changes you need, you can keep these comments for reference
    # *Note: .get_or_create() makes an object if one is not found or updates an existing one if found
    # *Note: 'created' is a boolean that is true if an object was created from .get_or_create()
    # *Note: .save() saves the data to the production server
    # *Note: parameters within .get_or_create() are ... .get_or_create(field_from_newmodels.py=each.field_in_my_form)
    #
    #   for each in queryset: #Loops through all instances of the form object
    #       (obj, created) = table_one.objects.using('default2').get_or_create(id=each.my_id,name=each.name,tel=each.phone_number)
    #       obj.save()
    #       (obj, created) = table_two.objects.using('default2').get_or_create(id=each.my_id,address=each.address)
    #       if not obj.address:
    #           #You can also use 'warning', 'debug', 'info' and 'success' in place of 'error'
    #           messages.error(request, 'Object did not have an address')
    #       obj.save()
    #       messages.success(request, 'Object was moved to production!')


    #for item in queryset:
    #    (obj, created) = IdRec.objects.using('default2').get_or_create(id=item.student_id)
    #    obj.fullname=item.name
    #    obj.save()
    #    (obj, created) = AaRec.objects.using('default2').get_or_create(id=item.student_id)
    #    (obj, created) = AcadRec.objects.using('default2').get_or_create(id=item.student_id)
    #    item_majors = list(item.majors.all())
    #    item_minors = list(item.minors.all())
    #    if len(item_majors) >= 1:
    #        obj.major1=item_majors[0]
    #    if len(item_majors) >= 2:
    #        obj.major2=item_majors[1]
    #    if len(item_majors) >= 3:
    #        obj.major3=item_majors[2]
    #    if len(item_minors) >= 1:
    #        obj.minor1=item_minors[0]
    #    if len(item_minors) >= 2:
    #        obj.minor2=item_minors[1]
    #    if len(item_minors) >= 3:
    #        obj.minor3=item_minors[2]
    #    obj.save()
        
    #    (obj, created) = ProgramEnrollRec.objects.using('default2').get_or_create(id=item.student_id)
    #    if item.advisor != '':
    #        obj.adv_id=1
    #    obj.cl=item.year
    #    obj.save()


#class MajorAdmin(admin.ModelAdmin):
    actions = [push_to_production] #Includes the action we defined earlier in this page

#Include all these models in the admin page
#admin.site.register(ProxyStudent, MajorAdmin)'''

