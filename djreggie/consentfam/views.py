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
        form.fields['student_id'].widget = forms.HiddenInput()
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
            submitted = True
            return render(request, 'consentfam/form.html', {
                'form': form, 
                'Parent_formset': Parent_formset,
                'submitted': submitted
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ModelForm()
        Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_id']))
            student = connection.execute(sql)
            for thing in student:
                form.fields['student_id'].initial = thing['id']
                form.fields['full_name'].initial = thing['fullname']
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
    })
    
def submitted(request):
    return render(request, 'consentfam/form.html')

def admin(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = 'SELECT * FROM cc_stg_ferpafamily INNER JOIN id_rec ON cc_stg_ferpafamily.student_id = id_rec.id'
    student = connection.execute(sql)
    return render(request, 'consentfam/home.html', {
        'student': student
    })

def student(request, student_id):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT *
            FROM cc_stg_ferpafamily
            INNER JOIN id_rec
            ON cc_stg_ferpafamily.student_id = id_rec.id
            WHERE cc_stg_ferpafamily.student_id = %s''' % (student_id)
    student = connection.execute(sql)
    sql2 = '''SELECT *
            FROM cc_stg_ferpafamily
            INNER JOIN cc_ferpafamily_rec
            ON cc_stg_ferpafamily.ferpafamily_no = cc_stg_ferpafamily_rec.ferpafamily_no
            WHERE cc_stg_ferpafamily.student_id = %s''' % (student_id)
    family = connection.execute(sql2)
    return render(request, 'consentfam/details.html', {
        'student': student.first(),
        'family': family,
    })

def search(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT *
            FROM cc_stg_ferpafamily
            INNER JOIN id_rec
            ON cc_stg_ferpafamily.student_id = id_rec.id
            WHERE cc_stg_ferpafamily.student_id = %s''' % (request.POST['cid'])
    student = connection.execute(sql)
    sql2 = '''SELECT *
            FROM cc_stg_ferpafamily
            INNER JOIN cc_ferpafamily_rec
            ON cc_stg_ferpafamily.ferpafamily_no = cc_stg_ferpafamily_rec.ferpafamily_no
            WHERE cc_stg_ferpafamily.student_id = %s''' % (request.POST['cid'])
    family = connection.execute(sql2)
    return render(request, 'consentfam/details.html', {
        'student': student.first(),
        'family': family,
    })

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
