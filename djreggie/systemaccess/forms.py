#Include django.forms
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
import re

from djreggie.systemaccess.models import AccessFormModel #Include the model that goes with this form

# Create your models here.
class AccessFormForm(forms.ModelForm):

    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(AccessFormForm, self).__init__(*args,**kwargs)
        
        #Validate all form fields here
        #self.fields['full_name'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a valid name',code='a')]
        #self.fields['carthage_id'].validators = [validators.RegexValidator(regex=('^[\d]{5,7}$'),message='Not a valid 5-7 digit Carthage id',code='a')]
        #self.fields['department'].validators = [validators.RegexValidator(regex=('^.+$'),message='Is not a department',code='a')]
        #self.fields['position'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a position',code='a')]
        #self.fields['work_phone'].validators = [validators.RegexValidator(regex=('^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}|NEW)$'),message='Not a valid phone number',code='a')]
        #self.fields['supervisor_name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z]+[a-zA-Z\s-]*$'),message='Not a valid name',code='a')]
    
    def clean_carthage_id(self):
        data = self.cleaned_data['carthage_id']
        if not re.match(r'^(\d{5,7})$', data):
            raise forms.ValidationError('Not a valid 5-7 digit Carthage id')
        return data
    
    def clean_work_phone(self):
        data = self.cleaned_data['work_phone']
        if not re.match(r'^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}|NEW)$', data):
            raise forms.ValidationError('Not a valid phone number')
        return data
    
    #Another option to include validation    
    def clean(self):
        cleaned_data = super(AccessFormForm, self).clean() #Grabs the clean data
        
        reason = cleaned_data.get("reason_for_change")
        other = cleaned_data.get("other_textbox")
        
        #Doesn't work now?
        if reason == "OTH" and other == "":
            msg = u"Please fill in the 'other' textbox"
            self._errors['reason_for_change'] = self.error_class([msg]) #Adds the error message to the field
            self._errors['other_textbox'] = self.error_class([msg])
            
            del cleaned_data['reason_for_change'] #Django told me to do this
            del cleaned_data['other_textbox']
            
        return cleaned_data
        
    def as_string(self):
        return """
INFO-->
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
    Registrar: (registrar)s
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
    
    Reason for change: %(reason_for_change)s
    Other: %(other_textbox)s

ADMINISTRATION-->
    Supervisor name: %(supervisor_name)s
    Supervisor signature: %(supervisor_signature)s
    Employee entered payroll: %(employee_entered_payroll_system)s
    Employee entered payroll date: %(employee_entered_payroll_system_by)s
    Registrar created web access: %(registrar_created_web_access)s
    Registrar created web access date: %(registrar_created_web_access_by)s
    Administrative system approval: %(administrative_system_approval)s
    Administrative system approval date: %(administrative_system_approval_date)s
    Administrative system created or changed: %(administrative_system_created_or_changed_date)s
    Administrative system created or changed date: %(administrative_system_created_or_changed_date_by)s
        """ % self.cleaned_data
        
    class Meta:
        model = AccessFormModel
        exclude = ['supervisor_name','supervisor_date']
        #db_table = 'access_form'
