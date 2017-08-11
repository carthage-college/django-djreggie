import re #For regular expressions
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from djzbar import settings
from djreggie import settings
from sqlalchemy import create_engine
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_exempt
#Including the form class
from djreggie.datareq.forms import DataReqForm
from djzbar.utils.mssql import get_userid
from djzbar.utils.informix import do_sql

def index(request):
    if request.POST: #If we do a POST
        form = DataReqForm(request.POST) #Scrape the data from the form and save it in a variable

        if form.is_valid(): #If the form is valid
            #email on valid submit
            send_mail("Data Request Submission",
                "Thank you for submitting your Candidacy Form for potential graduation this school year. Your submission has been received and is pending acceptance. Please keep an eye on your Carthage email for further correspondence regarding your eligibility for graduation.",
                'Testing Address <confirmation@carthage.edu>',
                'mkishline@carthage.edu', fail_silently=False)

            #form = DataReqForm()
            form = populateForm(int(request.POST['student_id']))
            valid_class = isValidClass(int(request.POST['student_id']))
            return render(request, 'datareq/form.html', {
                'form': form,
                'submitted': True,
                'year_low': year,
                'year_up': year+1,
                'userid':request.GET['student_id'],
                'valid_class': valid_class
            })
    else:
        if request.GET:
            if get_userid(request.GET['student_id']) == None:
                return render(request, 'datareq/no_access.html')

            cxID = int(get_userid(request.GET['student_id']))
            """
            #get student's id, name, and majors/minors
            getStudentSQL = '''
                SELECT
                    IDrec.id, TRIM(IDrec.firstname) AS firstname, TRIM(IDrec.middlename) AS middlename, TRIM(IDrec.lastname) AS lastname,
                    TRIM(major1.major) AS major1code, TRIM(major2.major) AS major2code, TRIM(major3.major) AS major3code,
                    TRIM(minor1.minor) AS minor1code, TRIM(minor2.minor) AS minor2code, TRIM(minor3.minor) AS minor3code
                FROM
                    id_rec    IDrec    INNER JOIN    prog_enr_rec    PROGrec    ON    IDrec.id        =    PROGrec.id
                                    LEFT JOIN    major_table        major1    ON    PROGrec.major1    =    major1.major
                                    LEFT JOIN    major_table        major2    ON    PROGrec.major2    =    major2.major
                                    LEFT JOIN    major_table        major3    ON    PROGrec.major3    =    major3.major
                                    LEFT JOIN    minor_table        minor1    ON    PROGrec.minor1    =    minor1.minor
                                    LEFT JOIN    minor_table        minor2    ON    PROGrec.minor2    =    minor2.minor
                                    LEFT JOIN    minor_table        minor3    ON    PROGrec.minor3    =    minor3.minor
                WHERE
                    IDrec.id = %d''' % (cxID)
            student = do_sql(getStudentSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)

            for row in student: #set student's initial data
                form.fields['student_id'].initial = row['id']
                form.fields['fname'].initial = row['firstname']
                form.fields['mname'].initial = row['middlename']
                form.fields['lname'].initial = row['lastname']
                form.fields['major1'].initial = row['major1code']
                form.fields['major2'].initial = row['major2code']
                form.fields['major3'].initial = row['major3code']
                form.fields['minor1'].initial = row['minor1code']
                form.fields['minor2'].initial = row['minor2code']
                form.fields['minor3'].initial = row['minor3code']
            """
            form = populateForm(cxID)
            """
            #check if student is a junior/senior or not
            getClassStandingSQL = '''SELECT
                        CASE prog_enr_rec.cl
                            WHEN    'JR'    THEN 'Y'
                            WHEN    'SR'    THEN 'Y'
                                            ELSE 'N'
                        END AS valid_class
                    FROM prog_enr_rec
                    WHERE prog_enr_rec.id = %s''' % (cxID)
            class_standing = do_sql(getClassStandingSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
            valid_class = class_standing.first()['valid_class']
            """
            valid_class = isValidClass(cxID)
            perm = getPermAddress(cxID)
        else:
            form = DataReqForm()

    return render(request, 'datareq/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1,
        'valid_class': valid_class,
        'submitted': False,
        'perm': perm,
        'userid': request.GET['student_id'],
    })

def populateForm(student_id):
    form = DataReqForm()
    #get student's id, name, and majors/minors
    getStudentSQL = '''
        SELECT
            IDrec.id, TRIM(IDrec.firstname) AS firstname, TRIM(IDrec.middlename) AS middlename, TRIM(IDrec.lastname) AS lastname,
            TRIM(major1.major) AS major1code, TRIM(major2.major) AS major2code, TRIM(major3.major) AS major3code,
            TRIM(minor1.minor) AS minor1code, TRIM(minor2.minor) AS minor2code, TRIM(minor3.minor) AS minor3code
        FROM
            id_rec    IDrec    INNER JOIN    prog_enr_rec    PROGrec    ON    IDrec.id        =    PROGrec.id
                            LEFT JOIN    major_table        major1    ON    PROGrec.major1    =    major1.major
                            LEFT JOIN    major_table        major2    ON    PROGrec.major2    =    major2.major
                            LEFT JOIN    major_table        major3    ON    PROGrec.major3    =    major3.major
                            LEFT JOIN    minor_table        minor1    ON    PROGrec.minor1    =    minor1.minor
                            LEFT JOIN    minor_table        minor2    ON    PROGrec.minor2    =    minor2.minor
                            LEFT JOIN    minor_table        minor3    ON    PROGrec.minor3    =    minor3.minor
        WHERE
            IDrec.id = %d''' % (student_id)
    student = do_sql(getStudentSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)

    for row in student: #set student's initial data
        form.fields['student_id'].initial = row['id']
        form.fields['fname'].initial = row['firstname']
        form.fields['mname'].initial = row['middlename']
        form.fields['lname'].initial = row['lastname']
        form.fields['major1'].initial = row['major1code']
        form.fields['major2'].initial = row['major2code']
        form.fields['major3'].initial = row['major3code']
        form.fields['minor1'].initial = row['minor1code']
        form.fields['minor2'].initial = row['minor2code']
        form.fields['minor3'].initial = row['minor3code']

    return form

def submitted(request):
    return render(request, 'datareq/form.html')

def contact(request): #gets student's contact info from form through ajax call
    getContactSQL = '''SELECT *
            FROM aa_rec
            WHERE id = %(id)s
            AND aa = "%(aa)s"
            AND TODAY BETWEEN beg_date AND NVL(end_date, TODAY)''' % (request.GET)
    contactinfo = do_sql(getContactSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    data = ''
    for row in contactinfo:
        for key in contactinfo.keys(): #we order the data this way so we can put it into a dict when it's recieved. HttpResponse only sends strings
            data = data + key + ':' + str(row[key]) + ','
    return HttpResponse(data)

def get_all_students(): #get all entries in table for use by jquery autocomplete
    sql = '''
        SELECT
            first_name, last_name, middle_initial, student_id
        FROM
            cc_stg_undergrad_candidacy
    '''
    return do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)


def admin(request): #main admin page
    return render(request, 'datareq/home.html', {
        'student': None,
        'full_student_list': None,
    })

def student(request, student_id): #admin details page
    return render(request, 'datareq/details.html', {
        'student': None,
        'reqmajors': None,
        'full_student_list': None,
    })

def search(request): #admin details page accessed through search bar
    return student(request, request.POST['cid'])


@csrf_exempt
def set_approved(request): #for setting the approved column in database for entry
    return HttpResponse('update successful')