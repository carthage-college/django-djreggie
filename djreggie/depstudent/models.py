from django.conf import settings
from django.db import models
from django import forms
from django.forms.models import modelformset_factory
from django.utils.safestring import mark_safe

from sqlalchemy import create_engine

'''
engine = create_engine(settings.INFORMIX_EARL)
connection = engine.connect()


sql1 = "select * from st_table"
state = connection.execute(sql1)
array1 = []
for row in state:
    array1.append((row['st'],row['txt']))
CHOICES1 = tuple(array1)
'''

class Depend(models.Model):

    PHONES= (
            ("CELL", "Cell Phone"),
            ("HOME", "Home Phone"),
            ("WORK", "Work Phone"),
    )

    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    ssn = models.CharField(max_length=11)
    address = models.CharField(max_length=500)
    dob = models.DateField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    email = models.EmailField()
    hphone = models.CharField(max_length=16)
    phonetype = models.CharField(max_length= 100, choices=PHONES)
    cphone = models.CharField(max_length=16, blank=True)
    phonetype2 = models.CharField(max_length= 100, choices=PHONES, blank=True)
    file = models.FileField(upload_to='files', blank=True)
    file2 = models.FileField(upload_to='files', blank=True)
    IRSDRT= (
        ("HAS",""),
        ("HASN", ""),
        ("WONT", "")
    )
    TACHED= (
        ("IS", ""),
        ("ISNT", "")
    )
    PLOY= (
        ("WASNT", ""),
        ("WAS", "")
    )
    useddata = models.CharField(choices=IRSDRT, max_length=500, default="HAS")
    attached = models.CharField(choices=TACHED, max_length=500, default="IS")
    employed = models.CharField(choices=PLOY, max_length=500, default="WAS")
    IRSDRT2= (
        ("HAS", ""),
        ("HASN", ""),
        ("WONT", "")
    )
    TACHED2= (
        ("IS", ""),
        ("ISNT", "")
    )
    PLOY2= (
        ("WAS", ""),
        ("WSNT", "")
    )
    useddata2 = models.CharField(
        choices=IRSDRT2, max_length=500, default="HAS"
    )
    attached2 = models.CharField(choices=TACHED2, max_length=500, default="IS")
    employed2 = models.CharField(choices=PLOY2, max_length=500, default="WAS")
    snapbenefits = models.BooleanField()
    childsupport = models.BooleanField()
    confirm = models.BooleanField()
    date = models.DateField(auto_now_add=True)


class FamInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.IntegerField(verbose_name="Age")
    relationship = models.CharField(
        max_length=100, verbose_name="Relationship"
    )
    college = models.CharField(max_length=200, verbose_name="College")
    halftimeenroll = models.BooleanField(verbose_name="Enrolled half time")
    student = models.ForeignKey(Depend)


class Studwork(models.Model):
    empname = models.CharField(max_length=250, verbose_name="Employer's Name")
    money = models.IntegerField(verbose_name="2012 Amount Earned")
    w2attach = models.BooleanField(verbose_name="IRS W-2 Attached?")
    student = models.ForeignKey(Depend)


class Parwork(models.Model):
    empname = models.CharField(
        max_length=250, verbose_name="Employer's Name"
    )
    money = models.IntegerField(verbose_name="2012 Amount Earned")
    w2attach = models.BooleanField(verbose_name="IRS W-2 Attached?")
    student = models.ForeignKey(Depend)


class CS(models.Model):
    namepaid = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Name of Person who Paid Child Support"
    )
    namepaidto = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Name of Person to Whom Child Support was Paid"
    )
    namechild = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Name of Child for Whom Support Was Paid"
    )
    amntpaid = models.IntegerField(
        blank=True,
        verbose_name="Amount of Child Support Paid in 2012",
    )
    student = models.ForeignKey(Depend)
