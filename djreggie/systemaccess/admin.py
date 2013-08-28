#admin.py is where we create 'actions' that users can do to entries
#within this app, systemaccess, as well as settings to change how
#we view entries within 'systemaccess'

#'admin' - necessary to change view settings when viewing an 'systemaccess' object
#'messages' - necessary to change success/fail messages when performing an action to an 'systemaccess' object
from django.contrib import admin, messages
from djreggie.systemaccess.models import AccessFormModel

#This is an 'action' a user can perform to a 'excavatebore' object
def push_to_production(modeladmin, request, queryset):
    push_to_production.short_description = 'Push to production server' #What the user sees
    
    
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
    
    
    
    
    
    #for each in queryset: #loop through all form fields
    
    #    (obj, created) = CarthageEmpRec.objects.using('default2').get_or_create(id=each.carthage_id, work_phone=each.work_phone, department=each.department, reason_for_change=each.reason_for_change, other_textbox=each.other_textbox, supervisor_name=each.supervisor_name, supervisor_signature=each.supervisor_signature, employee_entered_payroll_system=each.employee_entered_payroll_system, employee_entered_payroll_system_by=each.employee_entered_payroll_system_by, registrar_created_web_access=each.registrar_created_web_access, registrar_created_web_access_by=each.registrar_created_web_access_by, administrative_system_approval=each.administrative_system_approval, administrative_system_approval_date=each.administrative_system_approval_date, administrative_system_created_or_changed_date=each.administrative_system_created_or_changed_date, administrative_system_created_or_changed_date_by=each.administrative_system_created_or_changed_date_by)
    #    obj.save()
    #    
    #    (obj2, created2) = PermRec.objects.using('default2').get_or_create(id=each.carthage_id, email=each.email, novell_file_and_print_access=each.novell_file_and_print_access, eracer=each.eracer, common=each.common, programming=each.programming, admissions=each.admissions, recruiting=each.recruiting, student=each.student, financial=each.financial, student_billing=each.student_billing, management=each.management, student_services=each.student_services, financial_aid=each.financial_aid, registrar=each.registrar, display_registration=each.display_registration, development=each.development, donor_accounting=each.donor_accounting, planned_giving=each.planned_giving, institutional_advancement_grants=each.institutional_advancement_grants, alumni=each.alumni, phonathon=each.phonathon, health=each.health, add_id_records=each.add_id_records, registrar_administration=each.registrar_administration, financial_administration=each.financial_administration, admissions_administration=each.admissions_administration, training=each.training, cisco_vpn_remote_access_to_network=each.cisco_vpn_remote_access_to_network, administrative_access_to_user_machines=each.administrative_access_to_user_machines, network_security_administration=each.network_security_administration, system_administration=each.system_administration, cognos=each.cognos, author=each.author, consumer=each.consumer)
    #    obj2.save()


        
class AccessFormAdmin(admin.ModelAdmin):
    search_fields = ['carthage_id'] #We can search by 'carthage_id'
    list_display = ('carthage_id', 'full_name', 'department') #We will only see the following fields as columns in the admin page
    actions = [push_to_production] #Includes the action we defined earlier in this page
    readonly_fields = ('supervisor_date',) #We cannot change this in the admin page

admin.site.register(AccessFormModel, AccessFormAdmin) #Always be sure to add the model before adding the admin class
