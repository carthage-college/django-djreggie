from django.db import models
from django.conf import settings

from djzbar.utils.informix import do_sql

from datetime import date

EARL = settings.INFORMIX_EARL
DEBUG = settings.INFORMIX_DEBUG


class UndergradModel(models.Model):
    year = date.today().year
    if date.today().month <= 5:
            year = year - 1

    # All the fields in the form are below
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25, null=True, blank=True)
    lname = models.CharField(max_length=25)
    fnamepro = models.CharField(
        max_length=48, null=True, blank=True, default=""
    )
    mnamepro = models.CharField(
        max_length=48, null=True, blank=True, default=""
    )
    lnamepro = models.CharField(max_length=48)
    student_id = models.PositiveIntegerField()

    # Majors
    getMajorSQL = "SELECT txt, major from major_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           AND (web_display = 'Y' OR major = 'SELF') \
           ORDER BY txt ASC"
    major = do_sql(getMajorSQL, key=DEBUG, earl=EARL)
    MAJORS_TUPLE = tuple((row['major'], row['txt']) for row in major)

    # Minors
    getMinorSQL = "SELECT txt, minor from minor_table \
           WHERE sysdate BETWEEN active_date AND NVL(inactive_date, sysdate) \
           AND LENGTH(txt) > 0 \
           ORDER BY txt ASC"
    minor = do_sql(getMinorSQL, key=DEBUG, earl=EARL)
    MINORS_TUPLE = tuple((row['minor'], row['txt']) for row in minor)

    major1 = models.CharField(max_length=200, choices=MAJORS_TUPLE)
    minor1 = models.CharField(
        max_length=200, choices=MINORS_TUPLE, null=True, blank=True
    )
    major2 = models.CharField(
        max_length=200, choices=MAJORS_TUPLE, null=True, blank=True
    )
    minor2 = models.CharField(
        max_length=200, choices=MINORS_TUPLE, null=True, blank=True
    )
    major3 = models.CharField(
        max_length=200, choices=MAJORS_TUPLE, null=True, blank=True
    )
    minor3 = models.CharField(
        max_length=200, choices=MINORS_TUPLE, null=True, blank=True
    )
    participate_in_graduation = models.BooleanField()

    YEAR_CHOICES = ((str(year),year),(str(year+1),year+1))
    grad_yr = models.CharField(
        max_length=4, choices=YEAR_CHOICES, verbose_name='Year Graduating'
    )

    SESSION_CHOICES = (
        ('RA', 'Fall'),
        ('RB', 'J-Term'),
        ('RC', 'Spring'),
        ('RE', 'Summer')
    )
    grad_session = models.CharField(
        max_length=2,
        choices=SESSION_CHOICES,
        verbose_name='Session Graduating'
    )

    YESNOCHOICE = (
        ('T', 'Yes'),
        ('F', 'No')
    )
    will_teach = models.CharField(max_length=1, choices=YESNOCHOICE)

    year_teach = models.CharField(
        null=True, blank=True, max_length=4, choices=YEAR_CHOICES
    )
    TERMCHOICE = (
        ('SPR', 'Spring'),
        ('FAL', 'Fall')
    )
    term = models.CharField(
        null=True, blank=True, max_length=3, choices=TERMCHOICE
    )

    CONTACT_CHOICES = (('PHN', 'Phone'), ('EML', 'Email'))

    best_contact = models.CharField(
        max_length=4,
        choices=CONTACT_CHOICES
    )

    best_contact_value = models.CharField(max_length=50)

    address = models.CharField(
        max_length=64, null=True, blank=True, default=""
    )
    city = models.CharField(max_length=64, null=True, blank=True, default="")

    getStateSQL = '''
        SELECT
            TRIM(st) AS st,
            TRIM(txt) AS txt
        FROM
            st_table
        WHERE
            NVL(low_zone,1) > 1 AND NVL(high_zone,1) > 0
        ORDER BY
            txt ASC
    '''
    state = do_sql(getStateSQL, key=DEBUG, earl=EARL)
    CHOICESST = tuple((row['st'], row['txt']) for row in state)

    state = models.CharField(
        max_length=2, choices=CHOICESST, null=True, blank=True, default=""
    )
    zipcode = models.PositiveIntegerField(
        max_length=5, verbose_name='Zip', null=True, blank=True
    )

    diploma_aa_type = models.CharField(
        max_length = 4,
        choices = (('PERM','Current Address'), ('DIPL','Different Address')),
        blank = False,
        default = 'PERM'
    )

    date = models.DateField(auto_now_add=True)

    # How the objects are displayed in the admin page
    def __unicode__(self):
        return '{}, {} {}'.format(self.lname, self.fname, str(self.student_id))

    def save(self):
        '''
        # deal with funky characters
        dic = {}
        include = [
            'fname','mname','lname','fnamepro','mnamepro',
            'lnamepro','address','city','state'
        ]
        for n,v in self.__dict__.items():
            if n in include and v:
                #dic[n] = u'{}'.format(v.encode('cp1252'))
                #dic[n] = u'{}'.format(v.encode('ISO-8859-2'))
                #dic[n] = u'{}'.format(v.encode('ISO-8859-1'))
                #dic[n] = u'{}'.format(v.encode('utf-8'))
                #dic[n] = u'{}'.format(v.decode('ISO-8859-2').encode('utf-8'))
                #dic[n] = u'{}'.format(v.decode('utf-8').encode('cp1252'))
                #dic[n] = u'{}'.format(v.decode('cp1252').encode('utf-8'))
                #dic[n] = u'{}'.format(v.decode('utf-8'))
                #dic[n] = u'{}'.format(v.decode('ISO-8859-2'))
            else:
                dic[n] = v
        '''
        # put data into staging tables
        sql = u'''
            INSERT INTO cc_stg_undergrad_candidacy
            (
                student_id, first_name, middle_initial, last_name,
                first_name_pronounce, middle_name_pronounce,
                last_name_pronounce, major1, major2, major3, minor1,
                minor2, minor3, plan_to_walk, grad_yr, grad_sess, prog,
                aa, aa_value, address, city, state,
                zip, diploma_aa_type, datecreated
            )
            VALUES
            (
                {student_id},"{fname}","{mname}","{lname}","{fnamepro}",
                "{mnamepro}","{lnamepro}","{major1}","{major2}","{major3}",
                "{minor1}","{minor2}","{minor3}",
                "{participate_in_graduation}","{grad_yr}","{grad_session}",
                "{will_teach}","{best_contact}","{best_contact_value}",
                "{address}","{city}","{state}","{zipcode}",
                "{diploma_aa_type}", CURRENT
            )
        '''.format(**self.__dict__)
        #'''.format(**dic)
        insertSQL = sql.replace('"True"','"t"').replace('"False"','"f"')
        do_sql(insertSQL, key=DEBUG, earl=EARL)
