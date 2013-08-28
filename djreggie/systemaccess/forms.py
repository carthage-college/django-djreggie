#Include django.forms
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from djreggie.systemaccess.models import AccessFormModel #Include the model that goes with this form

# Create your models here.
class AccessFormForm(forms.ModelForm):

    #This is needed if you want to add error messages, labels or additional validation for fields
    def __init__(self, *args, **kwargs):
        super(AccessFormForm, self).__init__(*args,**kwargs)
        
        #Validate all form fields here
        self.fields['full_name'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a valid name',code='a')]
        self.fields['carthage_id'].validators = [validators.RegexValidator(regex=('^[\d]{5,7}$'),message='Not a valid 5-7 digit Carthage id',code='a')]
        self.fields['department'].validators = [validators.RegexValidator(regex=('^.+$'),message='Is not a department',code='a')]
        self.fields['position'].validators = [validators.RegexValidator(regex=('^.+$'),message='Not a position',code='a')]
        self.fields['work_phone'].validators = [validators.RegexValidator(regex=('^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}|NEW)$'),message='Not a valid phone number',code='a')]
        #self.fields['supervisor_name'].validators = [validators.RegexValidator(regex=('^[a-zA-Z]+[a-zA-Z\s-]*$'),message='Not a valid name',code='a')]
    
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
    
    Reason for change: %s
    Other: %s

ADMINISTRATION-->
    Supervisor name: %s
    Supervisor signature: %s
    Employee entered payroll: %s
    Employee entered payroll date: %s
    Registrar created web access: %s
    Registrar created web access date: %s
    Administrative system approval: %s
    Administrative system approval date: %s
    Administrative system created or changed: %s
    Administrative system created or changed date: %s
        """ % (self.cleaned_data['full_name'],self.cleaned_data['carthage_id'],self.cleaned_data['department'],self.cleaned_data['date_submitted'],self.cleaned_data['position'],self.cleaned_data['work_phone'],self.cleaned_data['email'],self.cleaned_data['novell_file_and_print_access'],self.cleaned_data['eracer'],self.cleaned_data['common'],self.cleaned_data['control'],self.cleaned_data['programming'],self.cleaned_data['admissions'],self.cleaned_data['recruiting'],self.cleaned_data['student'],self.cleaned_data['financial'],self.cleaned_data['student_billing'],self.cleaned_data['management'],self.cleaned_data['student_services'],self.cleaned_data['financial_aid'],self.cleaned_data['registrar'],self.cleaned_data['display_registration'],self.cleaned_data['development'],self.cleaned_data['donor_accounting'],self.cleaned_data['planned_giving'],self.cleaned_data['institutional_advancement_grants'],self.cleaned_data['alumni'],self.cleaned_data['phonathon'],self.cleaned_data['health'],self.cleaned_data['add_id_records'],self.cleaned_data['registrar_administration'],self.cleaned_data['financial_administration'],self.cleaned_data['admissions_administration'],self.cleaned_data['training'],self.cleaned_data['cisco_vpn_remote_access_to_network'],self.cleaned_data['administrative_access_to_user_machines'],self.cleaned_data['network_security_administration'],self.cleaned_data['system_administration'],self.cleaned_data['cognos'],self.cleaned_data['author'],self.cleaned_data['consumer'],self.cleaned_data['reason_for_change'],self.cleaned_data['other_textbox'],self.cleaned_data['supervisor_name'],self.cleaned_data['supervisor_signature'],self.cleaned_data['employee_entered_payroll_system'],self.cleaned_data['employee_entered_payroll_system_by'],self.cleaned_data['registrar_created_web_access'],self.cleaned_data['registrar_created_web_access_by'],self.cleaned_data['administrative_system_approval'],self.cleaned_data['administrative_system_approval_date'],self.cleaned_data['administrative_system_created_or_changed_date'],self.cleaned_data['administrative_system_created_or_changed_date_by'])
        
    class Meta:
        model = AccessFormModel
        exclude = ['supervisor_name','supervisor_date']
        #db_table = 'access_form'
