from django.db import models

#My model with the fields I will find in the form
class Form(models.Model):
    
    #All my fields in the form are below
    name = models.CharField(max_length=100) #'max_length' is required in (most) all fields
    student_ID = models.CharField(max_length=7, db_column='student_id')
    consent = models.CharField() #This renders as a select box
    date = models.DateField(auto_now_add=True, db_column='datecreated') #'auto_now_add' automatically adds the current date as well as sets this field invisible on the form
    
    class Meta:
        db_table = 'cc_stg_ferpadirectory'