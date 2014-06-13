from django import forms
from models import Independ, FamInfo, Studwork, CS
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.safestring import mark_safe
from django.forms.formsets import BaseFormSet
import re
# Create your forms here.
class DependForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(DependForm, self).__init__(*args, **kwargs)
        
    def clean_fname(self):
        data = self.cleaned_data['fname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please just enter a first name.')
        return data    
    def clean_mname(self):
        data = self.cleaned_data['mname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please just enter a middle name.')
        return data    
    def clean_lname(self):
        data = self.cleaned_data['lname']
        if not re.match(r'^([a-zA-Z]+)$', data):
            raise forms.ValidationError('Please just enter a last name.')
        return data
    
    def clean_ssn(self):
        data = self.cleaned_data['ssn']
        if not re.match(r'^(\d{3}[\-|\.\s]?\d{2}[\-|\.\s]??\d{4})$', data):
            raise forms.ValidationError('Invalid SSN')
        return data
    
    def clean_address(self):
        data = self.cleaned_data['address']
        if not re.match(r'^((?:[\w]+\s?)+[\w]+)$', data):
            raise forms.ValidationError('Invalid address. Alphanumerics and spaces only please.')
        return data
    
    def clean_state(self):
        data = self.cleaned_data['state']
        if not re.match(r'^((?:[a-zA-Z]+\s?)+[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid state. Just letters and spaces.')
        return data
    
    def clean_city(self):
        data = self.cleaned_data['city']
        if not re.match(r'^((?:[a-zA-Z]+\s?)+[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid city. Just letters and spaces.')
        return data
    
    def clean_hphone(self):
        data = self.cleaned_data['hphone']
        if not re.match(r'^((?:1?[\s\-\.\/]?\(?(?:\d{3})\)?)?[\s\-\.\/]?\d{3}[\s\-\.\/]?\d{4}(?:\s?(?:x|ext|\.)?\s?\d{4})?)$', data):
            raise forms.ValidationError('Invalid home phone')
        return data
    
    def clean_cphone(self):
        data = self.cleaned_data['cphone']
        if not re.match(r'^((?:1?[\s\-\.\/]?\(?(?:\d{3})\)?)?[\s\-\.\/]?\d{3}[\s\-\.\/]?\d{4}(?:\s?(?:x|ext|\.)?\s?\d{4})?)$', data):
            raise forms.ValidationError('Invalid cell phone')
        return data
    def clean_dob(self):
        data = self.cleaned_data['dob']
        if data > datetime.date.today():
            raise ValidationError(message = "This birthdate is in the future!")        
        return data
        
    
    def clean(self):                                                                                                                                      
        cleaned_data = self.cleaned_data #Grabs the clean data
        
        cphone = cleaned_data.get("cphone")
        phonetype2 = cleaned_data.get("phonetype2")
        
        if cphone == "" and phonetype2 == "":
            msg = u"You must fill out what type of phone your alternate phone is" #Adds the error message to the field
            self._errors["phonetype2"] = self.error_class([msg])
            
            
            
        return cleaned_data

    
    class Meta:
        model = Independ
        widgets = {
            'dob': forms.TextInput(attrs={'type':'date'})
            }
            
class FamInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FamInfoForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        data = self.cleaned_data['name']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('Invalid name. No special characters please.')
        return data    
    
    class Meta:
        model = FamInfo
        exclude = ['student']
        
class SincomeForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(SincomeForm, self).__init__(*args, **kwargs)
        
        #Validation
        self.fields['useddata'].label = ""
        self.fields['attached'].label = ""
        self.fields['employed'].label = ""
    
    def clean(self):
        cleaned_data = super(SincomeForm, self).clean() #Grabs the clean data

        attached = cleaned_data.get("attached")
        file = cleaned_data.get("file")
        
        if attached == "IS" and file == "" or None:
            msg = u"Please upload a file" #Adds the error message to the field
            self._errors["file"] = self.error_class([msg])

            del cleaned_data["attached"] #Django told me to do this?
            del cleaned_data["file"]
        
        return cleaned_data #Return the data back to the form
        
    #Global options for the class    
    class Meta:
        model = Independ #Fields come from the fields found in 'Sincome' model
        fields = ['useddata','attached', 'employed']
        widgets = {
            'useddata': forms.RadioSelect(),
            'attached': forms.RadioSelect(),
            'employed': forms.RadioSelect()
            }

class StudworkForm(forms.ModelForm):
    
    #We need to override this if we want to add custom validation/labels to our class
    def __init__(self, *args, **kwargs):
        super(StudworkForm, self).__init__(*args, **kwargs)
        
    def clean_empname(self):
        data = self.cleaned_data['empname']
        if not re.match(r'^((?:[\w]+\s?)+[\w]+)$', data):
            raise forms.ValidationError('Invalid company name. Alphanumerics and spaces only, please.')
    
    def clean_money(self):
        data = self.cleaned_data['money']
        if not re.match(r'^(\$?\d{1,3}(?:,?\d{3})*(?:\.\d{2})?|\.\d{2})?$', data):
            raise forms.ValidationError('Invalid amount earned')
        return data
    
    #Global options for the class    
    class Meta:
        model = Studwork #Fields come from the fields found in 'Studwork' model
        exclude = ['student']

class OtherinfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OtherinfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Independ
        fields = ['snapbenefits', 'childsupport']

class CSForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CSForm, self).__init__(*args, **kwargs)
   
    def clean_namepaid(self):
        data = self.cleaned_data['namepaid']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('That name is invalid. Letters and spaces only, please.')
        return data
    def clean_namepaidto(self):
        data = self.cleaned_data['namepaidto']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('That name is invalid. Letters and spaces only, please.')
        return data
    def clean_namechild(self):
        data = self.cleaned_data['namechild']
        if not re.match(r'^((?:[a-zA-Z]+\s?){1,2}[a-zA-Z]+)$', data):
            raise forms.ValidationError('That name is invalid. Letters and spaces only, please.')
        return data
    def clean_amntpaid(self):
        data = self.cleaned_data['amntpaid']
        if not re.match(r'^(\$?\d{1,3}(?:,?\d{3})*(?:\.\d{2})?|\.\d{2})?$', data):
            raise forms.ValidationError('Invalid amount')
        return data
    
    #Global options for the class
    class Meta:
        model = CS #Fields come from the fields found in 'CS' model
        exclude = ['student']
        
        
class CertificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CertificationForm, self).__init__(*args, **kwargs)
        #self.fields['confirm'].label = "I certify that all of the information reported on this worksheet is complete and correct."
    class Meta:
        model = Independ
        fields = ['confirm']


