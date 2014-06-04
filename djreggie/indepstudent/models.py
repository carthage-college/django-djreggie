from django.db import models
from django import forms
from django.forms.models import modelformset_factory
from django.utils.safestring import mark_safe
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
# Create your models here.
# Each class will exist in a separate table in the database
#SQL Alchemy
engine = create_engine(INFORMIX_EARL_TEST)
connection = engine.connect()


sql1 = "select * from st_table"
state = connection.execute(sql1)
array1 = []
for row in state:
    array1.append((row['st'],row['txt']))   
CHOICES1 = tuple(array1)
class Independ(models.Model):

    PHONES= (
            ("CELL", "Cell Phone"),
            ("HOME", "Home Phone"),
            ("WORK", "Work Phone"),
    )
    fname = models.CharField(max_length=100, verbose_name="First Name")
    mname = models.CharField(max_length=1, verbose_name="Middle Name")
    lname = models.CharField(max_length=100, verbose_name="Last Name")
    ssn = models.CharField(max_length=11, verbose_name="Social Security Number")
    address = models.CharField(max_length=500, verbose_name="Street Address")
    dob = models.DateField(verbose_name="Date of Birth")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=2,
                             choices=CHOICES1,
                             verbose_name="State")
    zip = models.CharField(max_length=5, verbose_name="Zip Code")
    email = models.EmailField(verbose_name="Email Address")
    hphone = models.CharField(max_length=16, verbose_name="Primary Phone")
    phonetype = models.CharField(max_length= 100,
                                 choices=PHONES,
                                 verbose_name="Type of Phone")
    cphone = models.CharField(max_length=16,
                              blank=True,
                              null=True,
                              verbose_name="Alternate Phone Number")
    phonetype2 = models.CharField(max_length= 100,
                                  choices=PHONES,
                                  blank=True,
                                  null=True,
                                  verbose_name="Type of Phone")
    file = models.FileField(upload_to='files',
                            verbose_name="Upload a tax return transcript here")
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
    snapbenefits = models.BooleanField(verbose_name="One of the persons listed\
                                       in Section B of this worksheet received\
                                       SNAP benefits in 2011 or 2012. If asked\
                                       by my school, I will provide\
                                       documentation of the receipt of SNAP\
                                       benefits during 2011 and/or 2012.")
    childsupport = models.BooleanField(verbose_name="Either I, or if married my\
                                       spouse who is listed in Section B of\
                                       this worksheet, paid child support in\
                                       2012. I have indicated\nbelow the name\
                                       of the person who paid the child\
                                       support, the name of the person to whom\
                                       the child support was paid, the\nnames\
                                       of the children for whom child support\
                                       was paid, and the total annual amount\
                                       of child support that was paid in\
                                       2012\nfor each child. If asked by my\
                                       school, I will provide documentation of\
                                       the payment of child support.\n\n")
    confirm = models.BooleanField(verbose_name="I certify that all of the\
                                  information reported on this worksheet is\
                                  complete and correct.")
    date = models.DateField(auto_now=True)
    
class FamInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.IntegerField(max_length=3, verbose_name="Age")
    relationship = models.CharField(max_length=100, verbose_name="Relationship")
    college = models.CharField(max_length=200, verbose_name="College")
    halftimeenroll = models.BooleanField(verbose_name="Will be Enrolled at Least Half Time")
    student = models.ForeignKey(Independ)

class Studwork(models.Model):
    empname = models.CharField(max_length=250, verbose_name="Employer's Name")
    money = models.IntegerField(max_length=10, verbose_name="2012 Amount Earned")
    w2attach = models.BooleanField(verbose_name="IRS W-2 Attached?")
    student = models.ForeignKey(Independ)

class CS(models.Model):
    namepaid = models.CharField(max_length=200, verbose_name="Name of Person who Paid Child Support")
    namepaidto = models.CharField(max_length=200, verbose_name="Name of Person to Whom Child Support was Paid")
    namechild = models.CharField(max_length=200, verbose_name="Name of Child for Whom Support Was Paid")
    amntpaid = models.IntegerField(max_length=10, verbose_name="Amount of Child Support Paid in 2012")
    student = models.ForeignKey(Independ)
    

