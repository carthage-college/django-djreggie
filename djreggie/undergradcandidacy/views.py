#I need all the imports below
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

# Create your views here.
def index(request):
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    if request.POST: #If we do a POST
        form = UndergradForm(request.POST) #Scrape the data from the form and save it in a variable
        
        
        
        if form.is_valid(): #If the form is valid
            form.save()
            send_mail("Undergraduate Candidacy Response", "Thank you for submitting the form. Your information is now being reviewed.", 'confirmation.carthage.edu',
            ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
            #Checking if the email is a carthage email
            
            form = UndergradForm()
            submitted = True
            return render(request, 'undergradcandidacy/form.html', {
                'form': form,
                'submitted': submitted,
                'year_low': year,
                'year_up': year+1,
                'valid_class': "Y"
            })
    else:
        form = UndergradForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = '''SELECT IDrec.id, IDrec.firstname, IDrec.middlename, IDrec.lastname,
                    major1.major AS major1code, major2.major AS major2code,
                    major3.major AS major3code, minor1.minor AS minor1code,
                    minor2.minor AS minor2code, minor3.minor AS minor3code
FROM id_rec	IDrec	INNER JOIN	prog_enr_rec	PROGrec	ON	IDrec.id		=	PROGrec.id
					LEFT JOIN	major_table		major1	ON	PROGrec.major1	=	major1.major
					LEFT JOIN	major_table		major2	ON	PROGrec.major2	=	major2.major
					LEFT JOIN	major_table		major3	ON	PROGrec.major3	=	major3.major
					LEFT JOIN	minor_table		minor1	ON	PROGrec.minor1	=	minor1.minor
					LEFT JOIN	minor_table		minor2	ON	PROGrec.minor2	=	minor2.minor
					LEFT JOIN	minor_table		minor3	ON	PROGrec.minor3	=	minor3.minor
WHERE IDrec.id = %d''' % (int(request.GET['student_id']))
            student = connection.execute(sql)
            
            for thing in student:
                form.fields['student_id'].initial = thing['id']
                form.fields['fname'].initial = thing['firstname']
                form.fields['mname'].initial = thing['middlename']
                form.fields['lname'].initial = thing['lastname']
                form.fields['major1'].initial = thing['major1code']
                form.fields['major2'].initial = thing['major2code']
                form.fields['major3'].initial = thing['major3code']
                form.fields['minor1'].initial = thing['minor1code']
                form.fields['minor2'].initial = thing['minor2code']
                form.fields['minor3'].initial = thing['minor3code']
                
            sql2 = '''SELECT
                        CASE prog_enr_rec.cl
                            WHEN 'JR' THEN 'Y'
                            WHEN 'SR' THEN 'Y'
                            ELSE 'N'
                        END AS valid_class
                    FROM prog_enr_rec
                    WHERE prog_enr_rec.id = %s''' % (request.GET['student_id'])
            class_standing = connection.execute(sql2)
            valid_class = class_standing.first()['valid_class']
            connection.close()
        
    return render(request, 'undergradcandidacy/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1,
        'valid_class': valid_class,
    })

        

def submitted(request):
    return render(request, 'undergradcandidacy/form.html')

def contact(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT *
            FROM aa_rec
            WHERE id = %(id)s
            AND aa = "%(aa)s"
            AND TODAY BETWEEN beg_date AND NVL(end_date, TODAY)''' % (request.GET)
    contactinfo = connection.execute(sql)  
    return HttpResponse(contactinfo)

def get_all_students():
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT first_name, last_name, middle_initial, student_id
            FROM cc_stg_undergrad_candidacy'''
    return connection.execute(sql)


def admin(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    if request.POST:
        sql2 = '''DELETE FROM cc_stg_undergrad_candidacy
            WHERE undergradcandidacy_no = %s''' % (request.POST['record'])
        connection.execute(sql2)
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
    student = connection.execute(sql)
    return render(request, 'undergradcandidacy/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT uc.*,
                    id_rec.addr_line1,
                    id_rec.addr_line2,
                    id_rec.city AS rec_city,
                    id_rec.st,
                    id_rec.zip AS rec_zip,
                    id_rec.ctry,
                    id_rec.phone
            FROM cc_stg_undergrad_candidacy AS uc
            INNER JOIN id_rec
            ON uc.student_id = id_rec.id
            WHERE uc.student_id = %s''' % (student_id)
    student = connection.execute(sql)
    sql2 = '''SELECT TRIM(major1.txt) AS major_txt1, TRIM(major2.txt) AS major_txt2, TRIM(major3.txt) AS major_txt3, TRIM(minor1.txt) AS minor_txt1, TRIM(minor2.txt) AS minor_txt2, TRIM(minor3.txt) AS minor_txt3
            FROM cc_stg_undergrad_candidacy
            LEFT JOIN major_table major1 ON cc_stg_undergrad_candidacy.major1 = major1.major
            LEFT JOIN major_table major2 ON cc_stg_undergrad_candidacy.major2 = major2.major
            LEFT JOIN major_table major3 ON cc_stg_undergrad_candidacy.major3 = major3.major
            LEFT JOIN minor_table minor1 ON cc_stg_undergrad_candidacy.minor1 = minor1.minor
            LEFT JOIN minor_table minor2 ON cc_stg_undergrad_candidacy.minor2 = minor2.minor
            LEFT JOIN minor_table minor3 ON cc_stg_undergrad_candidacy.minor3 = minor3.minor
            WHERE cc_stg_undergrad_candidacy.student_id = %s''' % (student_id)
    reqmajors = connection.execute(sql2)
    return render(request, 'undergradcandidacy/details.html', {
        'student': student.first(),
        'reqmajors': reqmajors.first(),
        'full_student_list': get_all_students(),
    })

def search(request):
    return student(request, request.POST['cid'])
    
    
@csrf_exempt
def set_approved(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''UPDATE cc_stg_undergrad_candidacy
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE undergradcandidacy_no = %(id)s''' % (request.POST)
    connection.execute(sql)
    return HttpResponse('update successful')
