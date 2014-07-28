import re #For regular expressions
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
#Including the form class
from djreggie.undergradcandidacy.forms import UndergradForm


def admin(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT uc.*,
                    TRIM(majors1.txt) AS major1_txt,
                    TRIM(majors2.txt) AS major2_txt,
                    TRIM(majors3.txt) AS major3_txt,
                    TRIM(minors1.txt) AS minor1_txt,
                    TRIM(minors2.txt) AS minor2_txt,
                    TRIM(minors3.txt) AS minor3_txt
            FROM cc_stg_undergrad_candidacy AS uc
            LEFT JOIN major_table AS majors1
            ON uc.major1 = majors1.major
            LEFT JOIN major_table AS majors2
            ON uc.major2 = majors2.major
            LEFT JOIN major_table AS majors3
            ON uc.major3 = majors3.major
            LEFT JOIN minor_table AS minors1
            ON uc.minor1 = minors1.minor
            LEFT JOIN minor_table AS minors2
            ON uc.minor2 = minors2.minor
            LEFT JOIN minor_table AS minors3
            ON uc.minor3 = minors3.minor
            WHERE uc.approved != 'Y'
            ORDER BY uc.datecreated DESC'''
    undergrad_student = connection.execute(sql)
    sql2 = '''SELECT fd.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpadirectory AS fd
            INNER JOIN id_rec
            ON fd.student_id = id_rec.id
            ORDER BY fd.datecreated DESC'''
    consent_form_student = connection.execute(sql2)
    sql3 = '''SELECT ff.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpafamily AS ff
            INNER JOIN id_rec
            ON ff.student_id = id_rec.id
            WHERE ff.approved != 'Y'
            ORDER BY ff.datecreated DESC'''
    consent_fam_student = connection.execute(sql3)
    sql4 = '''SELECT cm.*,
                    id_rec.firstname,
                    id_rec.lastname,
                    advisor.firstname AS advisor_first,
                    advisor.lastname AS advisor_last,
                    TRIM(majors1.txt) AS major1_txt,
                    TRIM(majors2.txt) AS major2_txt,
                    TRIM(majors3.txt) AS major3_txt,
                    TRIM(minors1.txt) AS minor1_txt,
                    TRIM(minors2.txt) AS minor2_txt,
                    TRIM(minors3.txt) AS minor3_txt
            FROM cc_stg_changemajor AS cm
            INNER JOIN id_rec
            ON cm.student_id = id_rec.id
            LEFT JOIN id_rec AS advisor
            ON advisor.id = cm.advisor_id
            LEFT JOIN major_table AS majors1
            ON cm.major1 = majors1.major
            LEFT JOIN major_table AS majors2
            ON cm.major2 = majors2.major
            LEFT JOIN major_table AS majors3
            ON cm.major3 = majors3.major
            LEFT JOIN minor_table AS minors1
            ON cm.minor1 = minors1.minor
            LEFT JOIN minor_table AS minors2
            ON cm.minor2 = minors2.minor
            LEFT JOIN minor_table AS minors3
            ON cm.minor3 = minors3.minor
            WHERE cm.approved != 'Y'
            ORDER BY cm.datecreated DESC'''
    change_major_student = connection.execute(sql4)
    return render(request, 'dashboard/bigadmin.html', {
        'undergrad_student': undergrad_student,
        'consent_form_student': consent_form_student,
        'consent_fam_student': consent_fam_student,
        'change_major_student': change_major_student,
    })