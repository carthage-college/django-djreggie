from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from forms import ChangeForm
from models import ChangeModel
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt # For CSRF
from django.template import RequestContext  # For CSRF
from django.core.mail import send_mail

def create(request):
    if request.POST: #If we do a POST            
        #(a, created) = ChangeModel.objects.get_or_create(student_id=request.POST[student_id])
        form = ChangeForm(request.POST) #Scrape the data from the form and save it in a variable
        
        if form.is_valid(): #If the form is valid
            if form.cleaned_data['advisor'] != '': #if they put in an new advisor
                engine = create_engine(INFORMIX_EARL_TEST)
                connection = engine.connect()
                #get new advisor's email
                advisor_sql = '''SELECT TRIM(aa_rec.line1) AS email
                                FROM aa_rec
                                WHERE id = %s''' % (form.cleaned_data['advisor'])
                advisor = connection.execute(advisor_sql)
                advisor_email = advisor.first()['email']
                connection.close()
                #email new advisor
                send_mail("You can't replace me, I'm the advisor!", "I'm the captai- er, advisor now", 'confirmation.carthage.edu',
                    ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
            form.save()        #Save the form data to the datbase table            
            form = ChangeForm()
            return render(request, 'changemajor/form.html', {
                'form': form, 
                'submitted': True
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ChangeForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            #gets student's id, name, and current majors/minors
            sql = '''SELECT IDrec.id, IDrec.fullname, major1.major AS major1code,
                    TRIM(major1.txt) AS major1, major2.major AS major2code, TRIM(major2.txt) AS major2,
                    major3.major AS major3code, TRIM(major3.txt) AS major3, minor1.minor AS minor1code,
                    TRIM(minor1.txt) AS minor1, minor2.minor AS minor2code, TRIM(minor2.txt) AS minor2,
                    minor3.minor AS minor3code, TRIM(minor3.txt) AS minor3
FROM id_rec	IDrec	INNER JOIN	prog_enr_rec	PROGrec	ON	IDrec.id		=	PROGrec.id
					LEFT JOIN	major_table		major1	ON	PROGrec.major1	=	major1.major
					LEFT JOIN	major_table		major2	ON	PROGrec.major2	=	major2.major
					LEFT JOIN	major_table		major3	ON	PROGrec.major3	=	major3.major
					LEFT JOIN	minor_table		minor1	ON	PROGrec.minor1	=	minor1.minor
					LEFT JOIN	minor_table		minor2	ON	PROGrec.minor2	=	minor2.minor
					LEFT JOIN	minor_table		minor3	ON	PROGrec.minor3	=	minor3.minor
WHERE IDrec.id = %d''' % (int(request.GET['student_id'])) #hvae to have ?student_id= in url for now
            student = connection.execute(sql)
            for thing in student: # set initial data based on student
                form.fields['student_id'].initial = thing['id']
                form.fields['name'].initial = thing['fullname']
                if thing['major2'] == None and thing['major3'] == None:
                    form.fields['majorlist'].initial = (thing['major1'])
                elif thing['major3'] == None:
                    form.fields['majorlist'].initial = "%s and %s" % (thing['major1'], thing['major2'])
                else:
                    form.fields['majorlist'].initial = "%s, %s, and %s" % (thing['major1'], thing['major2'],thing['major3'])
                if thing['minor2'] == None and thing['minor3'] == None:
                    form.fields['minorlist'].initial = (thing['minor1'])
                elif thing['minor3'] == None:
                    form.fields['minorlist'].initial = "%s and %s" % (thing['minor1'], thing['minor2'])
                else:
                    form.fields['minorlist'].initial = "%s, %s, and %s" % (thing['minor1'], thing['minor2'],thing['minor3'])
                form.fields['major1'].initial = thing['major1code']
                form.fields['major2'].initial = thing['major2code']
                form.fields['major3'].initial = thing['major3code']
                form.fields['minor1'].initial = thing['minor1code']
                form.fields['minor2'].initial = thing['minor2code']
                form.fields['minor3'].initial = thing['minor3code']
            connection.close()
        

    form.fields['student_id'].widget = forms.HiddenInput()
    form.fields['name'].widget = forms.HiddenInput()
    form.fields['majorlist'].widget = forms.HiddenInput()
    form.fields['minorlist'].widget = forms.HiddenInput()
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    #get list of valid advisors for jquery autocomplete
    sql2 = '''SELECT UNIQUE id_rec.id, TRIM(id_rec.firstname) AS firstname, TRIM(id_rec.lastname) AS lastname
            FROM job_rec
            INNER JOIN id_rec ON job_rec.id = id_rec.id
            WHERE hrstat = 'FT'
            AND TODAY BETWEEN job_rec.beg_date AND NVL(job_rec.end_date, TODAY)
            ORDER BY lastname, firstname'''
    advisor_list = connection.execute(sql2)
    
    return render(request, 'changemajor/form.html', {
        'form': form,
        'advisor_list': advisor_list,
        'submitted': False,
    })

def get_all_students(): #function to get a list of all entries in table for use in jquery autocomplete
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT id_rec.firstname, id_rec.lastname, cm.student_id
            FROM cc_stg_changemajor AS cm
            INNER JOIN id_rec
            ON cm.student_id = id_rec.id'''
    return connection.execute(sql)


def admin(request): #the function for the main admin page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    if request.POST: #if the delete button was clicked. remove entry from database
        sql2 = '''DELETE FROM cc_stg_changemajor
                WHERE changemajor_no = %s''' % (request.POST['record'])
        connection.execute(sql2)
    #get all entries in database along with advisor full name and major/minor full text
    sql = '''SELECT cm.*, 
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
            ORDER BY cm.approved, cm.datecreated DESC'''
    student = connection.execute(sql)
    return render(request, 'changemajor/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id): #admin details page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT cm.*,
                    id_rec.firstname,
                    id_rec.lastname,
                    id_rec.addr_line1,
                    id_rec.addr_line2,
                    id_rec.city,
                    id_rec.st,
                    id_rec.zip,
                    id_rec.ctry,
                    id_rec.phone,
                    advisor.firstname AS advisor_first,
                    advisor.lastname AS advisor_last
            FROM cc_stg_changemajor AS cm
            INNER JOIN id_rec
            ON cm.student_id = id_rec.id
            LEFT JOIN id_rec AS advisor
            ON advisor.id = cm.advisor_id
            WHERE cm.student_id = %s''' % (student_id)
    #get current majors/minors full text
    sql2 = '''SELECT TRIM(major1.txt) AS major1, TRIM(major2.txt) AS major2, TRIM(major3.txt) AS major3,
                    TRIM(minor1.txt) AS minor1,TRIM(minor2.txt) AS minor2, TRIM(minor3.txt) AS minor3
FROM id_rec	IDrec	INNER JOIN	prog_enr_rec	PROGrec	ON	IDrec.id		=	PROGrec.id
					LEFT JOIN	major_table		major1	ON	PROGrec.major1	=	major1.major
					LEFT JOIN	major_table		major2	ON	PROGrec.major2	=	major2.major
					LEFT JOIN	major_table		major3	ON	PROGrec.major3	=	major3.major
					LEFT JOIN	minor_table		minor1	ON	PROGrec.minor1	=	minor1.minor
					LEFT JOIN	minor_table		minor2	ON	PROGrec.minor2	=	minor2.minor
					LEFT JOIN	minor_table		minor3	ON	PROGrec.minor3	=	minor3.minor
WHERE IDrec.id = %s''' % (student_id)
    #get requested majors/minors full text
    sql3 = '''SELECT TRIM(major1.txt) AS major_txt1, TRIM(major2.txt) AS major_txt2, TRIM(major3.txt) AS major_txt3,
                TRIM(minor1.txt) AS minor_txt1, TRIM(minor2.txt) AS minor_txt2, TRIM(minor3.txt) AS minor_txt3
FROM cc_stg_changemajor
    LEFT JOIN major_table major1 ON cc_stg_changemajor.major1 = major1.major
    LEFT JOIN major_table major2 ON cc_stg_changemajor.major2 = major2.major
    LEFT JOIN major_table major3 ON cc_stg_changemajor.major3 = major3.major
    LEFT JOIN minor_table minor1 ON cc_stg_changemajor.minor1 = minor1.minor
    LEFT JOIN minor_table minor2 ON cc_stg_changemajor.minor2 = minor2.minor
    LEFT JOIN minor_table minor3 ON cc_stg_changemajor.minor3 = minor3.minor
WHERE cc_stg_changemajor.student_id = %s'''  % (student_id)
    student = connection.execute(sql)
    majors = connection.execute(sql2)
    reqmajors = connection.execute(sql3)
    return render(request, 'changemajor/details.html', {
        'student': student.first(),
        'majors': majors.first(),
        'reqmajors': reqmajors.first(),
        'full_student_list': get_all_students(),
    })

def search(request): #admin details page access through search bar
    return student(request, request.POST['cid'])

@csrf_exempt
def set_approved(request): #for setting entry to be approved
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''UPDATE cc_stg_changemajor
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE changemajor_no = %(id)s''' % (request.POST)
    connection.execute(sql)
    send_mail("Change Major Approval", "Congratulations! Your request to change your major has been approved",
                'confirmation.carthage.edu', ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
    sql2 = '''SELECT *
            FROM cc_stg_changemajor
            WHERE changemajor_no = %s''' % (request.POST['id'])
    result = connection.execute(sql2)
    student = result.first()
    sql3 = '''UPDATE prog_enr_rec
        SET major1 = "%(major1)s",
            major2 = "%(major2)s",
            major3 = "%(major3)s",
            minor1 = "%(minor1)s",
            minor2 = "%(minor2)s",
            minor3 = "%(minor3)s"''' % (student)
    if student['advisor_id']: #if advisor id exists then update that field in the database otherwise don't
        sql3 += ', adv_id = %s' % (student['advisor_id'])
    sql3 += 'WHERE id = %s' % (student['student_id'])
    connection.execute(sql3)
    return HttpResponse('update successful')
