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
    fname = models.CharField(max_length=200) #'max_length' is required in (most) all fields
    mname = models.CharField(max_length=200,
                             null=True,
                             blank=True) #'null=True' means this data member can be represented as null in the database
    lname = models.CharField(max_length=200)
    fnamepro = models.CharField(max_length=200)
    lnamepro = models.CharField(max_length=200)
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
    
    major1 = models.CharField(max_length=200, choices=CHOICES1)
    minor1 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True)
    major2 = models.CharField(max_length=200,
                              choices=CHOICES1,
                              null=True,
                              blank=True)
    minor2 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True)
    major3 = models.CharField(max_length=200,
                              choices=CHOICES1,
                              null=True,
                              blank=True)
    minor3 = models.CharField(max_length=200,
                              choices=CHOICES2,
                              null=True,
                              blank=True)
    
    participate_in_graduation = models.BooleanField() #Renders as a checkbox


    YEAR_CHOICES = ((str(year),year),(str(year+1),year+1))
    grad_yr = models.CharField(max_length=4,
                               choices=YEAR_CHOICES,
                               verbose_name='Year Graduating')
    
    SESSION_CHOICES = (
        ('RA', 'Fall'),
        ('RB', 'J-Term'),
        ('RC', 'Spring'),
        ('RE', 'Summer')
    )
    grad_session = models.CharField(max_length=2,
                                    choices=SESSION_CHOICES,
                                    verbose_name='Session Graduating')
    
    will_teach = models.CharField(max_length=4)
    sql4 = '''SELECT aa, TRIM(txt) AS txt
            FROM aa_table
            WHERE aa IN ("BILL","EML2","MAIL","PERM","PGDN")'''
            
    contact_types = connection.execute(sql4)
    CONTACT_CHOICES = tuple((row['aa'], row['txt']) for row in contact_types)
    
    best_contact = models.CharField(max_length=4,
                                    choices=CONTACT_CHOICES)
    
    best_contact_value = models.CharField(max_length=50)
    
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    
    sql3 = "SELECT * FROM st_table WHERE NVL(low_zone,1) > 1 AND NVL(high_zone,1) > 0 ORDER BY txt ASC"
    state = connection.execute(sql3)  
    CHOICESST = tuple((row['st'], row['txt']) for row in state)    
    connection.close()   
    
    state = models.CharField(max_length=2, choices=CHOICESST)
    zipcode = models.PositiveIntegerField(max_length=5,
                                          verbose_name='Zip')
    date = models.DateField(auto_now_add=True) #'auto_now_add' sets the date to the current date and makes this field invisible in the form

    #How the class is displayed in the admin page
    def __unicode__(self):
        return '%s, %s %d' % (self.lname, self.fname, self.student_id)
    
    def save(self): #put data into staging tables
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        sql = '''INSERT INTO cc_stg_undergrad_candidacy (student_id, first_name, middle_initial, last_name, first_name_pronounce, last_name_pronounce, major1, major2, major3, minor1, minor2, minor3, plan_to_walk, grad_yr, grad_sess, prog, aa, aa_value, address, city, state, zip, datecreated)
        VALUES (%(student_id)s, "%(fname)s", "%(mname)s", "%(lname)s", "%(fnamepro)s", "%(lnamepro)s", "%(major1)s", "%(major2)s", "%(major3)s", "%(minor1)s", "%(minor2)s", "%(minor3)s", "%(participate_in_graduation)s", "%(grad_yr)s", "%(grad_session)s", "%(will_teach)s", "%(best_contact)s", "%(best_contact_value)s", "%(address)s", "%(city)s", "%(state)s", "%(zipcode)s", CURRENT)''' % (self.__dict__)
        connection.execute(sql)