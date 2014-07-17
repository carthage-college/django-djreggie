from django.db import models

#Each class is a model that will be turned into a form

class ConsentModel(models.Model):
    #CHOICES1 = (
    #    ("ACCEPT", 'I agree with the previous statement.'),
    #)
    Full_Name_of_Student = models.CharField(max_length=100, verbose_name='Name')
    Carthage_ID_Number = models.CharField(max_length=7,
                                             verbose_name='Student ID',
                                             db_column='student_id')
    Date = models.DateField(auto_now_add=True, db_column='datecreated')
    phone = models.CharField(max_length=14)
    email = models.EmailField()

    def __unicode__(self):
        return self.Full_Name_of_Student
    
    class Meta:
        db_table = 'cc_stg_ferpafamily'

class ParentForm(models.Model):
    form = models.ForeignKey(ConsentModel, db_column='ferpafamily_no')
    share = models.CharField(max_length=200, db_column='allow')    
    name = models.CharField(max_length=100, db_column='name')
    phone = models.CharField(max_length=16, db_column='phone')
    email = models.EmailField(db_column='email')
    relation = models.CharField(max_length=20,
                                verbose_name='Relation',
                                db_column='relation')