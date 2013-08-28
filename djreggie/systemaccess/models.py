from django import forms
from django.db import models

# Create your models here.
class AccessFormModel(models.Model):

    #General Information
    full_name = models.CharField(max_length=64)
    carthage_id = models.IntegerField(primary_key=True,max_length=7)
    department = models.CharField(max_length=64)
    date_submitted = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=64)
    work_phone = models.CharField(max_length=16)
    
    #Permissions
    CHOICES = (
        ('a', 'Add'),
        ('d', 'Delete'),
    )
    
    email = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES,default='a')
    novell_file_and_print_access = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES,default='a')
    eracer = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES,default='a')
    common = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES,default='a')
    control = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    programming = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    admissions = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    recruiting = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    student = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    financial = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    student_billing = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    management = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    student_services = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    financial_aid = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    registrar = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    display_registration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    development = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    donor_accounting = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    planned_giving = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    institutional_advancement_grants = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    alumni = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    phonathon = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    health = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    add_id_records = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    registrar_administration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    financial_administration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    admissions_administration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    training = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    cisco_vpn_remote_access_to_network = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    administrative_access_to_user_machines = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    network_security_administration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    system_administration = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    cognos = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    author = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    consumer = models.CharField(max_length=2,blank=True,null=True,choices=CHOICES)
    
    #Permissions (ctd..)
    CHOICES2 = (
        ('NEW', 'New Employee'),
        ('UEM', 'No longer employed at Carthage'),
        ('RCH', 'Responsiblity change'),
        ('OTH', 'Other'),
    )
    
    reason_for_change = models.CharField(max_length=4,choices=CHOICES2)
    other_textbox = models.CharField(max_length=100,blank=True,null=True)
    
    #These fields are commented out because we no longer need them
    
    supervisor_name = models.CharField(max_length=64,blank=True, null=True)
    supervisor_date = models.DateField(blank=True, null=True)
    #supervisor_signature = models.CharField(max_length=64)
    #employee_entered_payroll_system = models.DateField()
    #employee_entered_payroll_system_by = models.CharField(max_length=64)
    #registrar_created_web_access = models.DateField()
    #registrar_created_web_access_by = models.CharField(max_length=64)
    #administrative_system_approval = models.CharField(max_length=64)
    #administrative_system_approval_date = models.DateField()
    #administrative_system_created_or_changed_date = models.DateField()
    #administrative_system_created_or_changed_date_by = models.CharField(max_length=64)
    
    #employee_name = models.CharField(max_length=64)
    #employee_department = models.CharField(max_length=64)
    #signature = models.CharField(max_length=64)
    #date = models.DateField()
    
    #Global options for the model
    class Meta:
        verbose_name = 'Entries' #I want to call it in the django admin page
        verbose_name_plural = 'Entries' #Plural version
    
    #Returns the data as a string for easy emailing
    def as_string(self):
        return """
            Full name: %s
            Carthage ID: %s
            Department: %s
            Date submitted: %s
            Position: %s
            Work phone: %s
            
            PERMISSIONS-->
                Email: %s
                Novell: %s
                eRacer: %s
                Common: %s
                Control: %s
                Programming: %s
                Admissions: %s
                Recruiting: %s
                Student: %s
                Financial: %s
                Student billing: %s
                Management: %s
                Student services: %s
                Financial aid: %s
                Registrar: %s
                Display registration: %s
                Development: %s
                Donor accounting: %s
                Planned giving: %s
                Institutional advancement grants: %s
                Alumni: %s
                Phonathon: %s
                Health: %s
                Add id records: %s
                Registrar administration: %s
                Financial administration: %s
                Admissions administration: %s
                Training: %s
                Cisco vpn: %s
                Administrative access to user machines: %s
                Network security administration: %s
                System administration: %s
                Cognos: %s
                Author: %s
                Consumer: %s
        """ % (full_name,carthage_id,department,date_submitted,position,work_phone,email,novell_file_and_print_access,eracer,common,control,programming,admissions,recruiting,student,financial,student_billing,management,student_services,financial_aid,registrar.display_registration,development,donor_accounting,planned_giving,institutional_advancement_grants,alumni,phonathon,health,add_id_records,registrar_administration,financial_administration,admissions_administration,training,cisco_vpn_remote_access_to_network,administrative_access_to_user_machines,network_security_administration,system_administration,cognos,author,consumer)
