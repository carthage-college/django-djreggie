from django.db import models

#Each class is a model that will be turned into a form

class ConsentModel(models.Model):
    #CHOICES1 = (
    #    ("ACCEPT", 'I agree with the previous statement.'),
    #)
    Full_Name_of_Student = models.CharField(max_length=100, verbose_name='Name')
    Carthage_ID_Number = models.IntegerField(max_length=7, verbose_name='Student ID')
    Date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=14)
    email = models.EmailField()

    def __unicode__(self):
        return self.Full_Name_of_Student

class ParentForm(models.Model):
    form = models.ForeignKey(ConsentModel)
    share = models.CharField(max_length=200)    
    name = models.CharField(max_length=100)
    Relation = models.CharField(max_length=200)