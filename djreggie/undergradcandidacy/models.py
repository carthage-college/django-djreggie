from django.db import models
from datetime import date
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
# Create your models here.
# Each class will exist in a separate table in the database
#SQL Alchemy
engine = create_engine(INFORMIX_EARL_TEST)
connection = engine.connect()

#The main fields in the form are in this class listed below
class UndergradModel(models.Model):
    year = date.today().year
    if date.today().month <= 5:
            year = year - 1
    #All the fields in the form are below
    fname = models.CharField(max_length=200, verbose_name='First Name') #'max_length' is required in (most) all fields
    mname = models.CharField(max_length=200,
                             null=True,
                             blank=True,
                             verbose_name='Middle Name') #'null=True' means this data member can be represented as null in the database
    lname = models.CharField(max_length=200, verbose_name='Last Name')
    student_id = models.PositiveIntegerField() #Only positive numbers are valid
    
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
    
    participate_in_graduation = models.BooleanField() #Renders as a checkbox

    FINISH_REQUIREMENTS_LIST = (
        ('RA', 'I will be finished with all required courses & degree requirements by the end of the %d/%d Fall Term (December)' % (year, year+1)),
        ('RB', 'I will be finished with all required courses & degree requirements by the end of the %d/%d J-Term (January)' % (year, year+1)),
        ('RC', 'I will be finished with all required courses & degree requirements by the end of the %d/%d Spring Term (May)' % (year, year+1)),
        ('RE', 'I will be finished with all required courses & degree requirements by the end of the %d/%d Summer Term (August)' % (year, year+1)),
    )
    finish_requirements_by = models.CharField(max_length=200, choices=FINISH_REQUIREMENTS_LIST) #Renders as a select box

    WHEN_TEACH_LIST = (
        ('F1', 'Fall Term %d' % (year)),
        ('SP', 'Spring Term %d' % (year+1)),
        ('F2', 'Fall Term %d' % (year+1)),
    )
    when_teach = models.CharField(max_length=200,
                                  null=True,
                                  blank=True,
                                  choices=WHEN_TEACH_LIST)

    best_phone = models.CharField(max_length=16, verbose_name='Best phone')
    cell = models.CharField(max_length=16,
                            null=True,
                            blank=True,
                            verbose_name='Cell')
    carthage_email = models.BooleanField(verbose_name='Check if carthage email')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    
    sql3 = "SELECT * FROM st_table WHERE NVL(low_zone,1) > 1 AND NVL(high_zone,1) > 0 ORDER BY txt ASC"
    state = connection.execute(sql3)  
    CHOICESST = tuple((row['st'], row['txt']) for row in state)    
    connection.close()   
    
    state = models.CharField(max_length=2, choices=CHOICESST)
    zipcode = models.PositiveIntegerField(max_length=5, verbose_name='Zip')
    date = models.DateField(auto_now_add=True) #'auto_now_add' sets the date to the current date and makes this field invisible in the form

    #How the class is displayed in the admin page
    def __unicode__(self):
        return '%s, %s %d' % (self.lname, self.fname, self.student_id)
