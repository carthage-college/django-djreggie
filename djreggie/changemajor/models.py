from django.conf import settings
from django.db import models

from djzbar.utils.informix import do_sql

class ChangeModel(models.Model):
    student_id = models.CharField(
        max_length=7, blank=False, db_column='student_id'
    )
    name = models.CharField(
        max_length=200, blank=True
    )
    majorlist = models.CharField(
        max_length=1000
    )
    minorlist = models.CharField(
        max_length=1000, blank=True, null=True
    )
    advisor = models.CharField(
        max_length=200, null=True, blank=True
    )

    # Majors
    # 2015-10-30: Brigid requested that nursing not be included
    # in the list of available majors

    getMajorSQL = '''
        SELECT
            TRIM(txt) AS txt, TRIM(major) AS major
        FROM
            major_table
        WHERE
            TODAY   BETWEEN active_date AND NVL(inactive_date, TODAY)
        AND
            LENGTH(txt) > 0
        AND
            web_display = 'Y'
        AND
            major       <>  'NUR'
        ORDER BY
            txt ASC
    '''

    major = do_sql(
        getMajorSQL,
        key=settings.INFORMIX_DEBUG,
        earl=settings.INFORMIX_EARL
    )

    MAJOR_CHOICES = tuple((row['major'], row['txt']) for row in major)

    # Minors
    getMinorSQL = '''
        SELECT
            TRIM(txt) AS txt, TRIM(minor) AS minor
        FROM
            minor_table
        WHERE
            TODAY   BETWEEN active_date AND NVL(inactive_date, TODAY)
        AND
            LENGTH(txt) > 0
        AND
            web_display = 'Y'
        ORDER BY
            txt ASC
    '''

    minor = do_sql(
        getMinorSQL,
        key=settings.INFORMIX_DEBUG,
        earl=settings.INFORMIX_EARL
    )

    MINOR_CHOICES = tuple((row['minor'], row['txt']) for row in minor)

    major1 = models.CharField(
        max_length=200,
        choices=MAJOR_CHOICES, db_column='major1'
    )
    minor1 = models.CharField(
        max_length=200,
        choices=MINOR_CHOICES, db_column='minor1',
        null=True, blank=True
    )
    major2 = models.CharField(
        max_length=200,
        choices=MAJOR_CHOICES, db_column='major2',
        null=True, blank=True
    )
    minor2 = models.CharField(
        max_length=200,
        choices=MINOR_CHOICES, db_column='minor2',
        null=True, blank=True
    )
    major3 = models.CharField(
        max_length=200,
        choices=MAJOR_CHOICES, db_column='major3',
        null=True, blank=True
    )
    minor3 = models.CharField(
        max_length=200,
        choices=MINOR_CHOICES, db_column='minor3',
        null=True, blank=True
    )

    def __unicode__(self):
        return self.name

    def save(self):

        # put data in staging tables

        insertSQL = '''
            INSERT INTO
                cc_stg_changemajor (
                    student_id, major1, major2, major3, minor1,
                    minor2, minor3, advisor_id, datecreated
                )
            VALUES (
                "{student_id}", "{major1}", "{major2}",
                "{major3}", "{minor1}", "{minor2}", "{minor3}",
                "{advisor}", CURRENT
            )
        '''.format(self.__dict__)

        do_sql(
            insertSQL,
            key=settings.INFORMIX_DEBUG,
            earl=settings.INFORMIX_EARL
        )
