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
    fname = models.CharField(max_length=200, db_column='first_name') #'max_length' is required in (most) all fields
    mname = models.CharField(max_length=200,
                             null=True,
                             blank=True,
                             db_column='middle_initial') #'null=True' means this data member can be represented as null in the database
    lname = models.CharField(max_length=200, db_column='last_name')
    fnamepro = models.CharField(max_length=200, db_column='first_name_pronounce')
    lnamepro = models.CharField(max_length=200, db_column='last_name_pronounce')
    student_id = models.PositiveIntegerField(db_column='student_id') #Only positive numbers are valid
    
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
    
    participate_in_graduation = models.BooleanField(db_column='plan_to_walk') #Renders as a checkbox


    YEAR_CHOICES = ((year,year),(year+1,year+1))
    grad_yr = models.CharField(max_length=4,
                               choices=YEAR_CHOICES,
                               verbose_name='Year Graduating',
                               db_column='grad_yr')
    
    SESSION_CHOICES = (
        ('Fall', 'RA'),
        ('J-Term', 'RB'),
        ('Spring', 'RC'),
        ('Summer', 'RE')
    )
    grad_session = models.CharField(max_length=2,
                                    choices=SESSION_CHOICES,
                                    verbose_name='Session Graduating',
                                    db_column='grad_sess')
    
    will_teach = models.CharField(max_length=4,
                                  db_column='prog')
    sql4 = '''SELECT aa, TRIM(txt) AS txt
            FROM aa_table
            WHERE aa IN ("BILL","EML2","MAIL","PERM","PGDN")'''
            
    contact_types = connection.execute(sql4)
    CONTACT_CHOICES = tuple((row['txt'], row['txt']) for row in contact_types)
    
    best_contact = models.CharField(max_length=4,
                                    choices=CONTACT_CHOICES,
                                    db_column='aa')
    
    best_contact_value = models.CharField(max_length=50,
                                          db_column='aa_value')
    
    address = models.CharField(max_length=200, db_column=address)
    city = models.CharField(max_length=200, db_column=city)
    
    sql3 = "SELECT * FROM st_table WHERE NVL(low_zone,1) > 1 AND NVL(high_zone,1) > 0 ORDER BY txt ASC"
    state = connection.execute(sql3)  
    CHOICESST = tuple((row['st'], row['txt']) for row in state)    
    connection.close()   
    
    state = models.CharField(max_length=2, choices=CHOICESST, db_column=state)
    zipcode = models.PositiveIntegerField(max_length=5,
                                          verbose_name='Zip',
                                          db_column=zip)
    date = models.DateField(auto_now_add=True, db_column=datecreated) #'auto_now_add' sets the date to the current date and makes this field invisible in the form

    #How the class is displayed in the admin page
    def __unicode__(self):
        return '%s, %s %d' % (self.lname, self.fname, self.student_id)
    
    class Meta:
        db_table = 'cc_stg_undergrad_candidacy'