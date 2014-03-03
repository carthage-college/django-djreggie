#You want these.
from django.db import models
from django import forms

#Each class is a model that will be turned into a form
class Contact(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
    
class ConsentModel(models.Model):
    #CHOICES1 = (
    #    ("ACCEPT", 'I agree with the previous statement.'),
    #)
    CHOICES2 = (
        ("ACADEMIC", 'Academic Records'),
        ("FINANCIAL", 'Financial Records'),
        ("BOTH", 'I would like to share both'),
        ("NEITHER", 'I would like to share neither'),
        ("OLD", "I would like to keep my old sharing settings"),
    )
        
    #Please_accept = models.CharField(choices=CHOICES1, max_length=200)
    Which_information_would_you_like_to_share = models.CharField(choices=CHOICES2, max_length=2000)
    Full_Name_of_Student = models.CharField(max_length=100)
    Carthage_ID_Number = models.IntegerField(max_length=7)
    Date = models.DateField(auto_now_add=True)
    name = models.ManyToManyField(Contact, through="ParentForm")
    
    def __unicode__(self):
        return self.Full_Name_of_Student
    
class ParentForm(models.Model):
    form = models.ForeignKey(ConsentModel, primary_key=True)
    contact = models.ForeignKey(Contact, primary_key=True)
    
    CHOICES3 = (
    ("MOM", 'Mother'),
    ("DAD", 'Father'),
    ("GRAN", 'Grandparent'),
    ("BRO", 'Brother'),
    ("SIS", 'Sister'),
    ("AUNT", 'Aunt'),
    ("UNC", 'Uncle'),
    ("HUSB", 'Husband'),
    ("FRIE", 'Friend'),
    ("OTHE", 'Other'),
    ("STEP", 'Stepparent'),
    )
    Relation = models.CharField(choices=CHOICES3, max_length=200)
    #def __unicode__(self):
    #    return self.form
