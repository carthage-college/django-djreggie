#Need this
from django.db import models
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine



class ChangeModel(models.Model):
    student_id = models.IntegerField(max_length=7,blank=False)
    name = models.CharField(max_length=200,blank=False) #'blank=False' means the field is required

    YEAR_IN_SCHOOL = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )

    year = models.CharField(max_length=2,blank=False,choices=YEAR_IN_SCHOOL) #Renders as a select field
    advisor = models.CharField(max_length=200, null=True, blank=True)
    
        
    #SQL Alchemy
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    
    #Majors
    sql1 = "SELECT txt, major from major_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           AND web_display = 'Y' \
           ORDER BY txt ASC"
    major = connection.execute(sql1)
    CHOICES1 = tuple((row['major'], row['txt']) for row in major)
    
    #Minors
    sql2 = "SELECT txt, minor from minor_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           AND web_display = 'Y' \
           ORDER BY txt ASC"
    minor = connection.execute(sql2)
    CHOICES2 = tuple((row['minor'], row['txt']) for row in minor)
    connection.close()   
    
    MJORMN = (
        ('MJ', 'Major'),
        ('MN', 'Minor'),
    )

    mjormn1 = models.CharField(max_length=2,
                              blank=False,
                              default = 'MJ',
                              choices=MJORMN,
                              verbose_name="Would you like to add a major or a minor?")
    major1 = models.CharField(max_length=200, choices=CHOICES1)
    minor1 = models.CharField(max_length=200, choices=CHOICES2)
    
    mjormn2 = models.CharField(max_length=2,
                              blank=False,
                              default = 'MJ',
                              choices=MJORMN,
                              verbose_name="Would you like to add a major or a minor?")
    major2 = models.CharField(max_length=200, choices=CHOICES1)
    minor2 = models.CharField(max_length=200, choices=CHOICES2)
    
    mjormn3 = models.CharField(max_length=2,
                              blank=False,
                              default = 'MJ',
                              choices=MJORMN,
                              verbose_name="Would you like to add a major or a minor?")
    major3 = models.CharField(max_length=200, choices=CHOICES1)
    minor3 = models.CharField(max_length=200, choices=CHOICES2)
   
    def __unicode__(self):
        return self.name