#Need all these imports
from django import forms
from django.core import validators #Used for custom validation
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

#Need to import all the models here
from models import Depend, FamInfo, Sincome, Studwork, Parwork, Parincome , Otherinfo, CS, certification

# Create your forms here.
class DependForm(forms.ModelForm):

    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(DependForm, self).__init__(*args, **kwargs)
        
        #Custom labels
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
        self.fields['file'].label = "Upload a file"
        
        #Custom regex validation
        self.fields['fname'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in first name', code='bad_fname')]
        self.fields['mname'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in middle name', code='bad_mname')]
        self.fields['lname'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in last name', code='bad_lname')]
        #self.fields['ssn'].validators = [validators.RegexValidator(regex='^(?!000)([0-6]\d{2}|7([0-6]\d|7[012]))([ -]?)(?!00)\d\d\3(?!0000)\d{4}$', message='Invalid SSN', code='bad_ssn')]
        self.fields['ssn'].validators = [validators.RegexValidator(regex='^[\d]{3}[\s\-]?[\d]{2}[\s\-]?[\d]{4}$', message='Invalid SSN', code='bad_ssn')]
        self.fields['address'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in address', code='bad_address')]
        self.fields['city'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid city', code='bad_city')]
        self.fields['state'].validators = [validators.RegexValidator(regex='^[a-zA-Z]{2}$', message='Invalid state', code='bad_state')]
        self.fields['zip'].validators = [validators.RegexValidator(regex='^[\d]{5}$', message='Invalid zip', code='bad_zip')]
        self.fields['email'].validators = [validators.RegexValidator(regex='^[A-Za-z0-9\.\_\%\+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,4}$', message='Invalid email address', code='bad_email')]
        self.fields['hphone'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='Invalid home phone', code='bad_phone')]
        self.fields['cphone'].validators = [validators.RegexValidator(regex='^(\d{4}|\d{3}[\s\-\.]?\d{4}|1?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})$', message='Invalid cell phone', code='bad_phone')]
        
        #Custom error messages
        self.fields['fname'].error_messages = {'required': 'Please fill in a first name.', 'invalid':'Invalid characters in first name'}
        self.fields['mname'].error_messages = {'required': 'Please fill in a middle name.', 'invalid':'Invalid characters in middle name'}
        self.fields['lname'].error_messages = {'required': 'Please fill in a last name.', 'invalid':'Invalid characters in last name'}
        self.fields['ssn'].error_messages = {'required': 'Please fill in a social security number', 'invalid':'Invalid ssn'}
        self.fields['address'].error_messages = {'required': 'Please fill in an address.', 'invalid':'Invalid characters in address'}
        self.fields['dob'].error_messages = {'required': 'Please fill in your date of birth.', 'invalid':'Invalid date of birth'}
        self.fields['city'].error_messages = {'required': 'Please fill in a city.', 'invalid':'Invalid characters in city'}
        self.fields['state'].error_messages = {'required': 'Please fill in a state.', 'invalid':'Invalid characters in state'}
        self.fields['zip'].error_messages = {'required': 'Please fill in a zip code.', 'invalid':'Invalid zip code'}
        self.fields['email'].error_messages = {'required': 'Please fill in an email address.', 'invalid':'Invalid characters in address'}
        self.fields['hphone'].error_messages = {'required': 'Please fill in a home phone number. If you dont have a home phone enter your cell number', 'invalid':'Invalid phone number'}        
        self.fields['cphone'].error_messages = {'required': 'Please fill in a cell phone number. If you dont have a cell phone enter your home number', 'invalid':'Invalid phone number'}

    #Global options for the form
    class Meta:
        model = Depend #Fields come from the fields found in 'Depend' model
        widgets = {
            'dob': forms.TextInput(attrs={'type':'date'}) #Changing the display of a field, here it's a datepicker
        }
            
class FamInfoForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(FamInfoForm, self).__init__(*args, **kwargs)
        
        #Regex validation
        self.fields['name'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in name', code='bad_name')]
        self.fields['age'].validators = [validators.RegexValidator(regex='^[\d]{3}$', message='Invalid age', code='bad_age')]
        self.fields['relationship'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in relationship', code='bad_relationship')]
        self.fields['college'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in college', code='bad_college')]
        
        #Custom labels
        self.fields['name'].label = "Full Name"
        self.fields['age'].label = "Age"
        self.fields['relationship'].label = "Relationship"
        self.fields['college'].label = "College"
        self.fields['halftimeenroll'].label = "Will be Enrolled at Least Half Time"
        
        #Error messages
        self.fields['name'].error_messages = {'required':'Name is required', 'invalid':'Invalid characters in name'}
        self.fields['age'].error_messages = {'required':'Age is required', 'invalid':'Invalid age'}
        self.fields['relationship'].error_messages = {'required':'Relationship is required','invalid':'Invalid characters in relationship'}
        self.fields['college'].error_messages = {'required':'College is required', 'invalid':'Invalid characters in college'}
    
    #Global options for the class    
    class Meta:
        model = FamInfo #Fields come from the fields found in 'FamInfo' model
        
class SincomeForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(SincomeForm, self).__init__(*args, **kwargs)
        
        #Validation
        self.fields['useddata'].label = ""
        self.fields['attached'].label = ""
        self.fields['employed'].label = ""
        
    #Global options for the class    
    class Meta:
        model = Sincome #Fields come from the fields found in 'Sincome' model
        widgets = {
            'useddata': forms.RadioSelect(),
            'attached': forms.RadioSelect(),
            'employed': forms.RadioSelect()
            }
class StudworkForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(StudworkForm, self).__init__(*args, **kwargs)
        
        #Validation
        self.fields['empname'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in employee name', code='bad_emplname')]
        self.fields['money'].validators = [validators.RegexValidator(regex='^\d{10}$', message='Invalid amount earned', code='bad_amt')]
        
        #Custom labels
        self.fields['empname'].label = "Employer's Name"
        self.fields['money'].label = "2012 Amount Earned"
        self.fields['w2attach'].label = "IRS W-2 Attached?"
        
        #Error messages
        self.fields['empname'].error_messages = {'required':'Employee name is required','invalid':'Invalid characters in employee name'}
        self.fields['money'].error_messages = {'required':'Amount earned is required','invalid':'Invalid amount earned'}
        
    #Global options for the class    
    class Meta:
        model = Studwork #Fields come from the fields found in 'Studwork' model
        
class ParincomeForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(ParincomeForm, self).__init__(*args, **kwargs)
        self.fields['useddata2'].label = ""
        self.fields['attached2'].label = ""
        self.fields['employed2'].label = ""
        
    #Global options for the class    
    class Meta:
        model = Parincome #Fields come from the fields found in 'Parincome' model
        widgets = {
            'useddata2': forms.RadioSelect(),
            'attached2': forms.RadioSelect(),
            'employed2': forms.RadioSelect()
            }
        
class ParworkForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(ParworkForm, self).__init__(*args, **kwargs)
        
        #Custom labels
        self.fields['empname'].label = "Employer's Name"
        self.fields['money'].label = "2012 Amount Earned"
        self.fields['w2attach'].label = "IRS W-2 Attached?"
        
        #Validation
        self.fields['empname'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid characters in employee name', code='bad_emplname')]
        self.fields['money'].validators = [validators.RegexValidator(regex='^\d{1,10}$', message='Invalid amount earned', code='bad_amt')]
        
        #Error messages
        self.fields['empname'].error_messages = {'required':'Employee name is required','invalid':'Invalid characters in employee name'}
        self.fields['money'].error_messages = {'required':'Amount earned is required','invalid':'Invalid amount earned'}
        
    #Global options for the class    
    class Meta:
        model = Parwork #Fields come from the fields found in 'Parwork' model
        
class OtherinfoForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(OtherinfoForm, self).__init__(*args, **kwargs)
        self.fields['snapbenefits'].label = "One of the persons listed in Section B of this worksheet received SNAP benefits in 2011 or 2012. If asked by the student\'s school, I will provide documentation of the receipt of SNAP benefits during 2011 and/or 2012."
        self.fields['childsupport'].label =  mark_safe("One (or both) of the student's parents listed in Section B of this worksheet paid child support in 2012.<br>The parent has indicated below the name of the person who paid the child support, the name of the person to whom the child support was<br>paid, the names of the children for whom child support was paid, and the total annual amount of child support that was<br>paid in 2012 for each child. If asked by the school, I will provide documentation of the payment of child support.<br><br>")
    
    #Global options for the class
    class Meta:
        model = Otherinfo #Fields come from the fields found in 'Otherinfo' model

class CSForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(CSForm, self).__init__(*args, **kwargs)
                
        #Custom labels
        self.fields['namepaid'].label = "Name of Person who Paid Child Support"
        self.fields['namepaidto'].label = "Name of Person to Whom Child Support was Paid"
        self.fields['namechild'].label = "Name of Child for Whom Support Was Paid"
        self.fields['amntpaid'].label = "Amount of Child Support Paid in 2012"
        
        #Custom validation
        self.fields['namepaid'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid name', code='bad_name')]
        self.fields['namepaidto'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid name', code='bad_name')]
        self.fields['namechild'].validators = [validators.RegexValidator(regex='^.+$', message='Invalid name', code='bad_name')]
        self.fields['amntpaid'].validators = [validators.RegexValidator(regex='^\d{1,10}$', message='Invalid amount', code='bad_amt')]
        
        #Custom error messages
        self.fields['namepaid'].error_messages = {'required':'Name is required','invalid':'Name has invalid characters'}
        self.fields['namepaidto'].error_messages = {'required':'Name is required', 'invalid':'Name has invalid characters'}
        self.fields['namechild'].error_messages = {'required':'Name is required', 'invalid':'Name has invalid characters'}
    
    #Global options for the class
    class Meta:
        model = CS #Fields come from the fields found in 'CS' model
        
class CertificationForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(CertificationForm, self).__init__(*args, **kwargs)
        
        self.fields['confirm'].label = "I confirm on behalf of student and parent that this form contains correct information filled out to the best of our ability and knowledge."
    
    #Global options for the class
    class Meta:
        model = certification #Fields come from the fields found in 'certification' model
