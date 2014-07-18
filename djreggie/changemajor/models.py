#Need this
from django.db import models
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine



class ChangeModel(models.Model):
    student_id = models.CharField(max_length=7,blank=False, db_column='student_id')
    name = models.CharField(max_length=200,blank=False) #'blank=False' means the field is required
    majorlist = models.CharField(max_length=1000)
    minorlist = models.CharField(max_length=1000,blank=True,null=True)
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
    
    major1 = models.CharField(max_length=200, choices=CHOICES1, db_column='major1')
    minor1 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True,
                              db_column='minor1')
    major2 = models.CharField(max_length=200,
                              choices=CHOICES1,
                              null=True,
                              blank=True,
                              db_column='major2')
    minor2 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True,
                              db_column='minor2')
    major3 = models.CharField(max_length=200,
                              choices=CHOICES1,
                              null=True,
                              blank=True,
                              db_column='major3')
    minor3 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True,
                              db_column='minor3')
   
    def __unicode__(self):
        return self.name
    

    def save(self):
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        sql = '''INSERT INTO cc_stg_changemajor (student_id, major1, major2, major3, minor1, minor2, minor3, advisor_id, datecreated)
        VALUES (%(student_id)s, "%(major1)s", "%(major2)s", "%(major3)s", "%(minor1)s", "%(minor2)s", "%(minor3)s", "%(advisor)s", CURRENT)''' % (self.__dict__)
        connection.execute(sql)