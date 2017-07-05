#You need all the imports below. Be sure to change the names of the models and forms accordingly!
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djreggie.consentfam.form import ModelForm, Parent
from djreggie.consentfam.models import ConsentModel, ParentForm
from djzbar import settings
from djreggie import settings
from djzbar.utils.informix import do_sql
from sqlalchemy import create_engine
from django.forms.formsets import formset_factory, BaseFormSet #For formsets
from django.core.mail import send_mail
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from djzbar.utils.mssql import get_userid


@csrf_protect
def create(request):
    #For info on setting up formsets, see this link: http://goo.gl/Oz53K2
    ParentFormSet = formset_factory(Parent)
    if request.POST:    #If we do a POST        
        #(a, created) = ConsentModel.objects.get_or_create(Carthage_ID_Number=request.POST['Carthage_ID_Number'])    
        form = ModelForm(request.POST)#Scrape the data from the form and save it in a variable
        form.fields['student_id'].widget = forms.HiddenInput() #This makes these fields hidden on the actual form
        form.fields['full_name'].widget = forms.HiddenInput()

        #Scrape the data from the form and save it in a variable
        Parent_formset = ParentFormSet(request.POST, prefix='Parent_or_Third_Party_Name')

        if form.is_valid() and Parent_formset.is_valid(): #If the forms are valid
            send_mail("Authorized Users (FERPA)",
                      "Thank you for submitting your selections regarding individuals who are allowed access to your financial and/or academic records. This information has been received and documented. You can view your preferences within my.carthage.edu. Should you wish to change the approved access for any or all individuals, please update accordingly using the electronic form.",
                      'registrar@carthage.edu',
                      ['mkishline@carthage.edu'],
                      fail_silently=False)

            form.save()        #Save the form data to the datbase table            
            getKeySQL = 'SELECT ferpafamily_no FROM cc_stg_ferpafamily WHERE student_id = %s ORDER BY ferpafamily_no DESC' % (form.cleaned_data['student_id'])
            stud = do_sql(getKeySQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
            prim_key = stud.first()['ferpafamily_no']
            for f in Parent_formset:#This is how we save formset data, since there are multiple forms in a formset
                f.cleaned_data['form'] = prim_key
                f.save()
            form = ModelForm()
            Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')
            return render(request, 'consentfam/form.html', {
                'form': form, 
                'Parent_formset': Parent_formset,
                'submitted': True
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ModelForm()
        
        if request.GET: #If we do a GET
            studentNameSQL = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(get_userid(request.GET['student_id'])))
            student = do_sql(studentNameSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
            for row in student: #Put in database values for the hidden fields
                form.fields['student_id'].initial = row['id']
                form.fields['full_name'].initial = row['fullname']
            #getting info from database if form has already been submitted by student
            family = get_family_ferpa(get_userid(request.GET['student_id']))

            #making dict of data for setting formset's initial data
            data = {'Parent_or_Third_Party_Name-TOTAL_FORMS': '1',
                    'Parent_or_Third_Party_Name-INITIAL_FORMS': '0',
                    'Parent_or_Third_Party_Name-MAX_NUM_FORMS': ''}
            for count, person in enumerate(family):
                data['Parent_or_Third_Party_Name-'+str(count)+'-share'] = person['allow']
                data['Parent_or_Third_Party_Name-'+str(count)+'-name'] = person['name']
                data['Parent_or_Third_Party_Name-'+str(count)+'-phone'] = person['phone']
                data['Parent_or_Third_Party_Name-'+str(count)+'-email'] = person['email']
                data['Parent_or_Third_Party_Name-'+str(count)+'-relation'] = person['relation']
                data['Parent_or_Third_Party_Name-TOTAL_FORMS'] = count + 1
            Parent_formset = ParentFormSet(data, prefix='Parent_or_Third_Party_Name')
        form.fields['student_id'].widget = forms.HiddenInput()
        form.fields['full_name'].widget = forms.HiddenInput()

    c = {'form': form, 'Parent_formset': Parent_formset }
    c.update(request)

    return render(request, 'consentfam/form.html', {
        'form': form,
        'Parent_formset': Parent_formset,
        'submitted': False,
    })

def submitted(request):
    return render(request, 'consentfam/form.html')

def get_all_students(): #gets all entries in table for use by jquery autocomplete
    sql = '''SELECT id_rec.firstname, id_rec.lastname, cf.student_id
            FROM cc_stg_ferpafamily cf  INNER JOIN  id_rec  ON  cf.student_id   =   id_rec.id'''
    return do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)


def admin(request): #main admin page
    if  request.POST: #if delete button was clicked. removes entry from database and all other entries associated with it
        sql2 = '''DELETE FROM cc_stg_ferpafamily_rec
                WHERE ferpafamily_no = %s''' % (request.POST['record'])
        do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        sql3 = '''DELETE FROM cc_stg_ferpafamily
                WHERE ferpafamily_no = %s''' % (request.POST['record'])
        do_sql(sql3, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    #get all entries from database
    sql = '''SELECT ff.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpafamily AS ff
            INNER JOIN id_rec
            ON ff.student_id = id_rec.id
            ORDER BY ff.approved, ff.datecreated DESC'''
    student = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return render(request, 'consentfam/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id): #admin details page
    return render(request, 'consentfam/details.html', {
        'student': get_student_info(student_id),
        'family': get_family_ferpa(student_id),
        'family2': get_family_ferpa(student_id),
        'full_student_list': get_all_students(),
    })

@csrf_exempt
def advisor_results(request, student_id):
    return render(request, 'consentfam/mresults.html', {
        'student': get_student_info(student_id),
        'family': get_family_ferpa(student_id),
        'submitted': True,
    })

@csrf_exempt
def search(request): #admin details page accessed through search bar
    return student(request, request.POST['cid'])

@csrf_exempt
def advisor_search(request):
    return render(request, 'consentfam/advisorsearch.html', {
        'full_student_list': get_all_students(),
    })

@csrf_exempt
def set_approved(request):
    sql = '''UPDATE cc_stg_ferpafamily
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE ferpafamily_no = %(id)s''' % (request.POST)
    do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return HttpResponse('update successful')

@csrf_exempt
def family_set_approved(request):
    sql = '''UPDATE cc_stg_ferpafamily_rec
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE ferpafamilyrec_no = %(id)s''' % (request.POST)
    do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return HttpResponse('update successful')

def get_student_info(student_id):
    getStudentInfoSQL = '''
        SELECT
            ff.*, TRIM(id_rec.firstname) AS firstname, TRIM(id_rec.lastname) AS lastname, TRIM(id_rec.addr_line1) AS addr_line1, TRIM(id_rec.addr_line2) AS addr_line2,
            TRIM(id_rec.city) AS city, TRIM(id_rec.st) AS st, id_rec.zip, TRIM(id_rec.ctry) AS ctry, TRIM(id_rec.phone) AS phone
        FROM
            cc_stg_ferpafamily  ff  INNER JOIN  id_rec  ON  ff.student_id   =   id_rec.id
        WHERE
            ff.student_id = %s''' % (student_id)
    student = do_sql(getStudentInfoSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return student.first()

def get_family_ferpa(student_id):
    ferpaFamilySQL = '''
        SELECT
            ff_rec.*
        FROM
            cc_stg_ferpafamily_rec  ff_rec  INNER JOIN  cc_stg_ferpafamily  ff  ON  ff_rec.ferpafamily_no   =   ff.ferpafamily_no
        WHERE
            ff.student_id = %s''' % (student_id)
    family = do_sql(ferpaFamilySQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return family
