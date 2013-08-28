from django.db import models
from django import forms
from django.forms.models import modelformset_factory
from django.utils.safestring import mark_safe

class Independ(models.Model):

    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=1)
    lname = models.CharField(max_length=100)
    ssn = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    dob = models.DateField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    email = models.EmailField()
    hphone = models.CharField()
    cphone = models.CharField()
    
class FamInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(max_length=3)
    relationship = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    halftimeenroll = models.BooleanField()
    
class Sincome(models.Model):    
    IRSDRT= (
        ("HAS", mark_safe("I, the student, have used the IRS Data Retrieval Tool in FAFSA on the Web to transfer my (and, if married, my spouse\'s) 2012 IRS income information into my FAFSA, either on the initial FAFSA or when making a correction to the FAFSA. Your school will use the IRS information that was transferred in the verification process.<br><br>")),
        ("HASN", mark_safe("I, the student, have not yet used the IRS Data Retrieval Tool, but I will use the tool to transfer my (and, if married, my spouse\'s) 2012 IRS income information into my FAFSA once I have filed my 2012 IRS tax return. See instructions above for information on how to use the IRS Data Retrieval Tool. Your school cannot complete the verification process until your(and, if married, your spouse\'s) IRS information has been transferred into your FAFSA.<br><br>")),
        ("WONT", mark_safe("I, the student, am unable or choose not to use the IRS Data Retrieval Tool in FAFSA on the Web, and I will submit to the school 2012 IRS tax return transcript(s) - not photocopies of the income tax return. To obtain an IRS tax return transcript, go to www.IRS.gov and click on the \"Order a Return or Account Transcript link\", or call 1-800-908-9946. Make sure to request the \"IRS tax return transcript\" and not the \"IRS tax account transcript.\" You will need your Social Security Number, date of birth, and the address on file with the IRS (normally this will be the address used when your 2012 IRS tax return was filed). It takes up to two weeks for IRS income information to be available for electronic IRS tax return filers, and up to eight weeks for paper IRS tax return filers. If you are married and you and your spouse filed separate 2012 tax returns, you must submit tax return transcripts for both you and your spouse.")),        
        )
    
    TACHED= (
        ("IS", mark_safe('Check here if an IRS tax return transcript(s) is attached to this worksheet.<br><br>')),
        ("ISNT", mark_safe('Check here if IRS tax return transcript(s) will be submitted to your school later. Verification cannot be completed until the IRS tax return transcript(s) has been submitted to your school.')),    
        )
    
    PLOY= (
        ("WAS", mark_safe('The student (and, if married, the student\'s spouse) was not employed and had no income earned from work in 2012.<br><br>')),
        ("WSNT", 'The student (and/or the student\'s spouse if married) was employed in 2012 and has listed below the names of all employers, the amount earned from each employer in 2012, and whether an IRS W-2 form is attached. Attach copies of all 2012 W-2 forms issued to you (and, if married, to your spouse) by employers. List every employer even if the employer did not issue an IRS W-2 form.'),    
        )
    
    useddata = models.CharField(choices=IRSDRT, max_length=500, default="HAS")
    attached = models.CharField(choices=TACHED, max_length=500, default="IS")
    employed = models.CharField(choices=PLOY, max_length=500, default="WAS")

class Studwork(models.Model):
    empname = models.CharField(max_length=250)
    money = models.IntegerField(max_length=10)
    w2attach = models.BooleanField()
    
class Otherinfo(models.Model):
    snapbenefits = models.BooleanField()
    childsupport = models.BooleanField()
    
class CS(models.Model):
    namepaid = models.CharField(max_length=200)
    namepaidto = models.CharField(max_length=200)
    namechild = models.CharField(max_length=200)
    amntpaid = models.IntegerField(max_length=10)
    
class certification(models.Model):
    confirm = models.BooleanField()
    date = models.DateField(auto_now=True)
