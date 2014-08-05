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
    valid_class = 'Y'
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    if request.POST: #If we do a POST
        form = UndergradForm(request.POST) #Scrape the data from the form and save it in a variable
        
        
        
        if form.is_valid(): #If the form is valid
            form.save()
            #email on valid submit
            send_mail("Undergraduate Candidacy Response", "Thank you for submitting your Candidacy Form for potential graduation this school year.  Your submission has been received and is pending acceptance.  Please keep an eye on your Carthage email for further correspondence regarding your eligibility for graduation.", 'confirmation.carthage.edu',
            ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
            
            form = UndergradForm()
            return render(request, 'undergradcandidacy/form.html', {
                'form': form,
                'submitted': True,
                'year_low': year,
                'year_up': year+1,
                'valid_class': "Y" #this is here so there isn't an error.
            })
    else:
        form = UndergradForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            #get student's id, name, and majors/minors
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
            
            for thing in student: #set student's initial data
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
            #check if student is a junior/senior or not
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
        'submitted': False,
    })

        

def submitted(request):
    return render(request, 'undergradcandidacy/form.html')

def contact(request): #gets student's contact info from form through ajax call
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT *
            FROM aa_rec
            WHERE id = %(id)s
            AND aa = "%(aa)s"
            AND TODAY BETWEEN beg_date AND NVL(end_date, TODAY)''' % (request.GET)
    contactinfo = connection.execute(sql)
    data = ''
    for thing in contactinfo:
        for key in contactinfo.keys(): #we order the data this way so we can put it into a dict when it's recieved. HttpResponse only sends strings
            data = data + key + ':' + str(thing[key]) + ','
    return HttpResponse(data)

def get_all_students(): #get all entries in table for use by jquery autocomplete
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT first_name, last_name, middle_initial, student_id
            FROM cc_stg_undergrad_candidacy'''
    return connection.execute(sql)


def admin(request): #main admin page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    if request.POST: #if delete button was clicked. removes entry from database
        sql2 = '''DELETE FROM cc_stg_undergrad_candidacy
            WHERE undergradcandidacy_no = %s''' % (request.POST['record'])
        connection.execute(sql2)
    #gets all entries along with majors/minors full text 
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
            ORDER BY uc.approved, uc.datecreated DESC'''
    student = connection.execute(sql)
    return render(request, 'undergradcandidacy/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id): #admin details page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    #gets entry's info
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
    #gets majors/minors full text
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

def search(request): #admin details page accessed through search bar
    return student(request, request.POST['cid'])
    
    
@csrf_exempt
def set_approved(request): #for setting the approved column in database for entry
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''UPDATE cc_stg_undergrad_candidacy
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE undergradcandidacy_no = %(id)s''' % (request.POST)
    connection.execute(sql)
    sql2 = '''SELECT COUNT(*) AS count
            FROM gradwalk_rec
            WHERE id = %s ''' % (request.POST['student_id'])
    record = connection.execute(sql2)
    record_exists = record.first()['count']
    sql3 = '''SELECT *
            FROM cc_stg_undergradcandidacy
            WHERE undergradcandidacy_no = %s''' % (request.POST['id'])
    student = connection.execute(sql3)
    if record_exists:
        sql4 = '''UPDATE gradwalk_rec
                SET grad_sess = "%(grad_sess)s",
                    grad_yr = "%(grad_yr)s",
                    name_on_diploma = "%(first_name)s %(middle_initial)s %(last_name)s",
                    fname_pronounce = "%(first_name_pronounce)s",
                    lname_pronounce = "%(last_name_pronounce)s",
                    addr = "%(address)s %(city)s, %(state)s %(zip)s",
                    plan2walk = "%(plan_to_walk)s",
                    major1 = "%(major1)s",
                    major2 = "%(major2)s",
                    major3 = "%(major3)s",
                    minor1 = "%(minor1)s",
                    minor2 = "%(minor2)s",
                    minor3 = "%(minor3)s"
                WHERE id = %(student_id)s''' % (student.first())
        connection.execute(sql4)
    else:
        sql5 = '''INSERT INTO gradwalk_rec
                (id,
                prog,
                site,
                degree,
                grad_sess,
                grad_yr,
                name_on_diploma,
                fname_pronounce,
                lname_pronounce,
                addr,
                plan2walk,
                major1,
                major2,
                major3,
                minor1,
                minor2,
                minor3)
                VALUES (%(student_id)s,
                        "UNDG",
                        "CART",
                        "BA",
                        "%(grad_sess)s",
                        "%(grad_yr)s",
                        "%(first_name)s %(middle_initial)s %(last_name)s",
                        "%(first_name_pronounce)s",
                        "%(last_name_pronounce)s",
                        "%(address)s %(city)s, %(state)s %(zip)s",
                        "%(plan_to_walk)s",
                        "%(major1)s",
                        "%(major2)s",
                        "%(major3)s",
                        "%(minor1)s",
                        "%(minor2)s",
                        "%(minor3)s")''' % (student.first())
        connection.execute(sql5)
    return HttpResponse('update successful')
