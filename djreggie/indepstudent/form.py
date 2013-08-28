from django import forms
from models import Independ, FamInfo, Sincome, Studwork, Otherinfo, CS, certification 
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.safestring import mark_safe

# Create your forms here.
class DependForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(DependForm, self).__init__(*args, **kwargs)
        self.fields['fname'].label = "First Name"
        self.fields['mname'].label = "Middle Name"
        self.fields['lname'].label = "Last Name"
        self.fields['ssn'].label = "Social Security Number"
        self.fields['address'].label = "Street Address"
        self.fields['dob'].label = "Date of Birth"
        self.fields['city'].label = "City"
        self.fields['state'].label = "State"
        self.fields['zip'].label = "Zip Code"
        self.fields['email'].label = "Email Address"
        self.fields['hphone'].label = "Home Phone"
        self.fields['cphone'].label = "Cell or Alternate Phone"
        self.fields['hphone'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='You entered an invalid phone number', code='bad_phone')]
        self.fields['cphone'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='You entered an invalid phone number', code='bad_phone')]
        self.fields['fname'].error_messages = {'required': 'Please fill in a first name.'}
        self.fields['mname'].error_messages = {'required': 'Please fill in a middle initial.'}
        self.fields['lname'].error_messages = {'required': 'Please fill in a last name.'}
        self.fields['ssn'].validators = [validators.RegexValidator(regex='^(?!000)([0-6]\d{2}|7([0-6]\d|7[012]))([ -]?)(?!00)\d\d\3(?!0000)\d{4}$', message='This is an invalid Social Security Number', code='bad_ssn')]
        self.fields['ssn'].error_messages = {'required': 'Please fill in a social security number'}
        self.fields['address'].error_messages = {'required': 'Please fill in an address.'}
        self.fields['dob'].error_messages = {'required': 'Please fill in your date of birth.'}
        self.fields['city'].error_messages = {'required': 'Please fill in a city.'}
        self.fields['state'].error_messages = {'required': 'Please fill in a state.'}
        self.fields['zip'].error_messages = {'required': 'Please fill in a zip code.'}
        self.fields['email'].error_messages = {'required': 'Please fill in an email address.'}
        self.fields['hphone'].error_messages = {'required': 'Please fill in a home phone number. If you dont have a home phone enter your cell number'}        
        self.fields['cphone'].error_messages = {'required': 'Please fill in a cell phone number. If you dont have a cell phone enter your home number'}
        self.fields['zip'].validators = [validators.RegexValidator(regex='^\d{5}$', message='enter a valid zipcode', code='a')]

    class Meta:
        model = Independ
        widgets = {
            'dob': forms.TextInput(attrs={'type':'date'})
            }
            
class FamInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FamInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Full Name"
        self.fields['age'].label = "Age"
        self.fields['relationship'].label = "Relationship"
        self.fields['college'].label = "College"
        self.fields['halftimeenroll'].label = "Will be Enrolled at Least Half Time"
    class Meta:
        model = FamInfo
        
class SincomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SincomeForm, self).__init__(*args, **kwargs)
        self.fields['useddata'].label = ""
        self.fields['attached'].label = ""
        self.fields['employed'].label = ""
    class Meta:
        model = Sincome
        widgets = {
            'useddata': forms.RadioSelect(),
            'attached': forms.RadioSelect(),
            'employed': forms.RadioSelect()
            }
class StudworkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudworkForm, self).__init__(*args, **kwargs)
        self.fields['empname'].label = "Employer's Name"
        self.fields['money'].label = "2012 Amount Earned"
        self.fields['w2attach'].label = "IRS W-2 Attached?"
    class Meta:
        model = Studwork
class OtherinfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OtherinfoForm, self).__init__(*args, **kwargs)
        self.fields['snapbenefits'].label = "One of the persons listed in Section B of this worksheet received SNAP benefits in 2011 or 2012. If asked by my school, I will provide documentation of the receipt of SNAP benefits during 2011 and/or 2012."
        self.fields['childsupport'].label =  mark_safe("Either I, or if married my spouse who is listed in Section B of this worksheet, paid child support in 2012. I have indicated<br>below the name of the person who paid the child support, the name of the person to whom the child support was paid, the<br>names of the children for whom child support was paid, and the total annual amount of child support that was paid in 2012<br>for each child. If asked by my school, I will provide documentation of the payment of child support.<br><br>")
    class Meta:
        model = Otherinfo

class CSForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CSForm, self).__init__(*args, **kwargs)
        self.fields['namepaid'].label = "Name of Person who Paid Child Support"
        self.fields['namepaidto'].label = "Name of Person to Whom Child Support was Paid"
        self.fields['namechild'].label = "Name of Child for Whom Support Was Paid"
        self.fields['amntpaid'].label = "Amount of Child Support Paid in 2012"
    class Meta:
        model = CS
        
class CertificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CertificationForm, self).__init__(*args, **kwargs)
        self.fields['confirm'].label = "I certify that all of the information reported on this worksheet is complete and correct."
    class Meta:
        model = certification

