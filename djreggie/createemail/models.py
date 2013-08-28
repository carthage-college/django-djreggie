#Need this import
from django.db import models

# Create your models here.
class EmailModel(models.Model):
    
    #All of my fields in my form

    #date = models.DateField(max_length=16,blank=False) #Keeping this commented out unless we need this field in the database
    requested_by = models.CharField(max_length=64,blank=False) #'blank=False' means the field is required
    name_of_account_requested = models.CharField(max_length=64,blank=False)
    purpose_of_account = models.CharField(max_length=300,blank=False)
    names_of_all_users = models.CharField(max_length=300,blank=False)
    needed_until = models.DateField(max_length=16,blank=False)
    unique_id = models.CharField("ID",max_length=7,blank=False)#'ID' sets the label of this field        
