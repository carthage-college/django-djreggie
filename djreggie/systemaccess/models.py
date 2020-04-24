from django import forms
from django.db import models

# Create your models here.
class AccessFormModel(models.Model):

    #General Information
    full_name = models.CharField(max_length=64)
    carthage_id = models.IntegerField(primary_key=True)
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
        
    supervisor_name = models.CharField(max_length=64,blank=True, null=True)
    supervisor_date = models.DateField(blank=True, null=True)

    
    #Global options for the model
    class Meta:
        verbose_name = 'Entries' #I want to call it in the django admin page
        verbose_name_plural = 'Entries' #Plural version
    
    #Returns the data as a string for easy emailing
    def as_string(self):
        return """
            Full name: %(full_name)s
            Carthage ID: %(carthage_id)s
            Department: %(department)s
            Date submitted: %(date_submitted)s
            Position: %(position)s
            Work phone: %(work_phone)s
            
            PERMISSIONS-->
                Email: %(email)s
                Novell: %(novell_file_and_print_access)s
                eRacer: %(eracer)s
                Common: %(common)s
                Control: %(control)s
                Programming: %(programming)s
                Admissions: %(admissions)s
                Recruiting: %(recruiting)s
                Student: %(student)s
                Financial: %(financial)s
                Student billing: %(student_billing)s
                Management: %(management)s
                Student services: %(student_services)s
                Financial aid: %(financial_aid)s
                Registrar: %(registrar)s
                Display registration: %(display_registration)s
                Development: %(development)s
                Donor accounting: %(donor_accounting)s
                Planned giving: %(planned_giving)s
                Institutional advancement grants: %(institutional_advancement_grants)s
                Alumni: %(alumni)s
                Phonathon: %(phonathon)s
                Health: %(health)s
                Add id records: %(add_id_records)s
                Registrar administration: %(registrar_administration)s
                Financial administration: %(financial_administration)s
                Admissions administration: %(admissions_administration)s
                Training: %(training)s
                Cisco vpn: %(cisco_vpn_remote_access_to_network)s
                Administrative access to user machines: %(administrative_access_to_user_machines)s
                Network security administration: %(network_security_administration)s
                System administration: %(system_administration)s
                Cognos: %(cognos)s
                Author: %(author)s
                Consumer: %(consumer)s
        """ % self.__dict__
