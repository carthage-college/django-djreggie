from django.db import models

#My model with the fields I will find in the form
class Form(models.Model):
    
    #All my fields in the form are below
    name = models.CharField(max_length=100) #'max_length' is required in (most) all fields
    student_ID = models.PositiveIntegerField(max_length=7)
    
    #First string is value, second string is what users sees
    CHOICES = (
        ("CONSENT", 'I authorize and consent to the release of my directory information'),
        ("NOCONSENT", 'I hereby request that Carthage College not release my directory information.'),
    )
    consent = models.CharField(choices=CHOICES, max_length=200) #This renders as a select box
    Date = models.DateField(auto_now_add=True) #'auto_now_add' automatically adds the current date as well as sets this field invisible on the form
    
