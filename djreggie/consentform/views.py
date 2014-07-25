#I need all the imports below
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django import forms
from django.core.mail import send_mail

#Need to include the form object
from form import ModelForm
from models import Form

def create(request):
    if request.POST: #If we do a POST
        #(a, created) = Form.objects.get(student_ID=request.POST['student_ID'])    
        form = ModelForm(request.POST) #Scrape the data from the form and save it in a variable
        
        if form.is_valid(): #If the form is valid
            if form.data['consent'] == 'NOCONSENT':
                send_mail("Don\'t do it!", "You\'re making a huge mistake", 'confirmation.carthage.edu',
                    ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)  
            form.save() #Save the form data to the datbase table
            form = ModelForm()
           # submitted = True
            return render(request, 'consentform/form.html', {
                'form': form
            })
    else:
        form = ModelForm()
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        sql = 'SELECT id_rec.id FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_ID']))
        student = connection.execute(sql)
        for thing in student:
            form.fields['student_ID'].initial = thing['id']
        connection.close()
        form.fields['student_ID'].widget = forms.HiddenInput()

    return render(request, 'consentform/form.html', {
    'form': form,
    })
def admin(request):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    if request.POST:
        sql2 = '''DELETE FROM cc_stg_ferpadirectory
                WHERE ferpadirectory_no = %s''' % (request.POST['record'])
        connection.execute(sql2)
    sql = '''SELECT fd.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpadirectory AS fd
            INNER JOIN id_rec
            ON fd.student_id = id_rec.id
            ORDER BY fd.datecreated DESC'''
    student = connection.execute(sql)
    return render(request, 'consentform/home.html', {
        'student': student
    })

def student(request, student_id):
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()
    sql = '''SELECT fd.*,
                    id_rec.firstname,
                    id_rec.lastname,
                    id_rec.addr_line1,
                    id_rec.addr_line2,
                    id_rec.city,
                    id_rec.st,
                    id_rec.zip,
                    id_rec.ctry,
                    id_rec.phone
            FROM cc_stg_ferpadirectory AS fd
            INNER JOIN id_rec
            ON fd.student_id = id_rec.id
            WHERE fd.student_id = %s''' % (student_id)
    student = connection.execute(sql)
    return render(request, 'consentform/details.html', {
        'student': student.first()
    })

def search(request):
    student(request, request.POST['cid'])