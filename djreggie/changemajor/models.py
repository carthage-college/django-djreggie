#Need this
from django.db import models
from djzbar import settings
from djreggie import settings
from sqlalchemy import create_engine
from djzbar.utils.informix import do_sql


class ChangeModel(models.Model):
    student_id = models.CharField(max_length=7,blank=False, db_column='student_id')
    name = models.CharField(max_length=200,blank=False) #'blank=False' means the field is required
    majorlist = models.CharField(max_length=1000)
    minorlist = models.CharField(max_length=1000,blank=True,null=True)
    advisor = models.CharField(max_length=200, null=True, blank=True)
       
    
    #Majors
    sql1 = "SELECT txt, major from major_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           AND web_display = 'Y' \
           ORDER BY txt ASC"
    major = do_sql(sql1, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    CHOICES1 = tuple((row['major'], row['txt']) for row in major)
    
    #Minors
    sql2 = "SELECT txt, minor from minor_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           AND web_display = 'Y' \
           ORDER BY txt ASC"
    minor = do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
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
        #put data in staging tables
        sql = '''INSERT INTO cc_stg_changemajor (student_id, major1, major2, major3, minor1, minor2, minor3, advisor_id, datecreated)
        VALUES (%(student_id)s, "%(major1)s", "%(major2)s", "%(major3)s", "%(minor1)s", "%(minor2)s", "%(minor3)s", "%(advisor)s", CURRENT)''' % (self.__dict__)
        do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)