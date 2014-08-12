#You need all the imports below. Be sure to change the names of the models and forms accordingly!
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djreggie.consentfam.form import ModelForm, Parent
from djreggie.consentfam.models import ConsentModel, ParentForm
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.forms.formsets import formset_factory, BaseFormSet #For formsets
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF
from django.views.decorators.csrf import csrf_exempt


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
            form.save()        #Save the form data to the datbase table            
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql1 = 'SELECT ferpafamily_no FROM cc_stg_ferpafamily WHERE student_id = %s ORDER BY ferpafamily_no DESC' % (form.cleaned_data['student_id'])
            stud = connection.execute(sql1)
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
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect() #Set up to make a sql call where we get fields based on the ID in the url
            sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_id']))
            student = connection.execute(sql)
            for thing in student: #Put in database values for the hidden fields
                form.fields['student_id'].initial = thing['id']
                form.fields['full_name'].initial = thing['fullname']
            #getting info from database if form has already been submitted by student
            sql2 = '''SELECT ff_rec.*
                    FROM cc_stg_ferpafamily_rec AS ff_rec
                    INNER JOIN cc_stg_ferpafamily AS ff
                    ON ff_rec.ferpafamily_no = ff.ferpafamily_no
                    WHERE ff.student_id = %s''' % (request.GET['student_id'])
            family = connection.execute(sql2)
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
            connection.close()
        form.fields['student_id'].widget = forms.HiddenInput()
        form.fields['full_name'].widget = forms.HiddenInput()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'form': form,
         'Parent_formset': Parent_formset,
        }
    c.update(csrf(request))

    return render(request, 'consentfam/form.html', {
        'form': form, 
        'Parent_formset': Parent_formset,
        'submitted': False,
    })
    
def submitted(request):
    return render(request, 'consentfam/form.html')

def get_all_students(): #gets all entries in table for use by jquery autocomplete
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT id_rec.firstname, id_rec.lastname, cf.student_id
            FROM cc_stg_ferpafamily AS cf
            INNER JOIN id_rec
            ON cf.student_id = id_rec.id'''
    return connection.execute(sql)


def admin(request): #main admin page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    if  request.POST: #if delete button was clicked. removes entry from database and all other entries associated with it
        sql2 = '''DELETE FROM cc_stg_ferpafamily_rec
                WHERE ferpafamily_no = %s''' % (request.POST['record'])
        connection.execute(sql2)
        sql3 = '''DELETE FROM cc_stg_ferpafamily
                WHERE ferpafamily_no = %s''' % (request.POST['record'])
        connection.execute(sql3)
    #get all entries from database
    sql = '''SELECT ff.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpafamily AS ff
            INNER JOIN id_rec
            ON ff.student_id = id_rec.id
            ORDER BY ff.approved, ff.datecreated DESC'''
    student = connection.execute(sql)
    return render(request, 'consentfam/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id): #admin details page
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    #get entry's info
    sql = '''SELECT ff.*,
                    id_rec.firstname,
                    id_rec.lastname,
                    id_rec.addr_line1,
                    id_rec.addr_line2,
                    id_rec.city,
                    id_rec.st,
                    id_rec.zip,
                    id_rec.ctry,
                    id_rec.phone
            FROM cc_stg_ferpafamily AS ff
            INNER JOIN id_rec
            ON ff.student_id = id_rec.id
            WHERE ff.student_id = %s''' % (student_id)
    student = connection.execute(sql)
    sql2 = '''SELECT ff_rec.*
            FROM cc_stg_ferpafamily_rec AS ff_rec
            INNER JOIN cc_stg_ferpafamily AS ff
            ON ff_rec.ferpafamily_no = ff.ferpafamily_no
            WHERE ff.student_id = %s''' % (student_id)
    family = connection.execute(sql2)
    return render(request, 'consentfam/details.html', {
        'student': student.first(),
        'family': family,
        'full_student_list': get_all_students(),
    })

@csrf_exempt
def search(request): #admin details page accessed through search bar
    return student(request, request.POST['cid'])

@csrf_exempt
def set_approved(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''UPDATE cc_stg_ferpafamily
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE ferpafamily_no = %(id)s''' % (request.POST)
    connection.execute(sql)
    return HttpResponse('update successful')


@csrf_exempt
def family_set_approved(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''UPDATE cc_stg_ferpafamily_rec
            SET approved="%(approved)s", datemodified=CURRENT
            WHERE ferpafamilyrec_no = %(id)s''' % (request.POST)
    connection.execute(sql)
    return HttpResponse('update successful')

def advisor_search(request):
    return render(request, 'consentfam/advisorsearch.html', {
        'full_student_list': get_all_students(),
    })