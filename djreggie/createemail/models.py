from django.db import models


class EmailModel(models.Model):

    #Keeping this commented out unless we need this field in the database
    #date = models.DateField(max_length=16,blank=False)
    requested_by = models.CharField(max_length=64, blank=False)
    account_name = models.CharField(max_length=64, blank=False)
    purpose = models.EmailField(max_length=300, blank=False)
    users = models.CharField(max_length=300, blank=False)
    needed_until = models.DateField(max_length=16, blank=False)
    unique_id = models.CharField("ID",max_length=7, blank=False)
