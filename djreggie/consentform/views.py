# I need all the imports below
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from djzbar import settings
from djreggie import settings
from sqlalchemy import create_engine
from django import forms
# We do this instead of send_mail because we need HTML (bullets)
# NOTE: you CAN send HTML with send_mail() method
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from djzbar.utils.informix import do_sql
from djzbar.utils.mssql import get_userid
# Need to include the form object
from form import ModelForm
from models import Form

def create(request):
    if request.POST: #If we do a POST
        #(a, created) = Form.objects.get(student_ID=request.POST['student_ID'])    
        form = ModelForm(request.POST) #Scrape the data from the form and save it in a variable
        
        if form.is_valid(): #If the form is valid
            if form.data['consent'] == 'NOCONSENT':
                subject, from_email, to = 'Subject: Directory Information Confirmation',\
                'registrar@carthage.edu',\
                'mkauth@carthage.edu'
                text_content = ''
                html_content = '''Thank you for completing the form regarding your preferences for directory information, as required by FERPA.  Given that you have selected that you do not want directory information released, please note that Carthage will not be able to disclose information such as:
<br><br><li>Dean's List accomplishments to your local newspaper</li>
<li>Verification of enrollment/degree completion for potential or current employers</li>
<li>Your name will not be published in the program for graduation</li>
<br>Please note that you can change your directory information selection at any time, should you wish that Carthage be able to release this type of information.  If you would like to update your preferences, this can be done by completing the electronic form again with your updated selection.'''
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            form.save() #Save the form data to the datbase table
            form = ModelForm()
           # submitted = True
            return render(request, 'consentform/form.html', {
                'form': form,
                'submitted': True,
            })
    else:
        form = ModelForm()
        sql = 'SELECT id_rec.id FROM id_rec WHERE id_rec.id = %d' % (int(get_userid(request.GET['student_id'])))
        student = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        for thing in student:
            form.fields['student_ID'].initial = thing['id']
        sql2 = 'SELECT cc_stg_ferpadirectory.consent FROM cc_stg_ferpadirectory WHERE cc_stg_ferpadirectory.student_id = %d' % (int(get_userid(request.GET['student_id'])))
        student2 = do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        for thing in student2:
            if thing['consent'] == "N":
                form.fields['consent'].initial = "NOCONSENT"
            else:
                form.fields['consent'].initial = "CONSENT"
        form.fields['student_ID'].widget = forms.HiddenInput()

    return render(request, 'consentform/form.html', {
        'form': form,
        'submitted': False,
    })

@csrf_exempt
def mobile(request):
    if request.POST: #If we do a POST
        #(a, created) = Form.objects.get(student_ID=request.POST['student_ID'])    
        form = ModelForm(request.POST) #Scrape the data from the form and save it in a variable
        
        if form.is_valid(): #If the form is valid
            if form.data['consent'] == 'NOCONSENT':
                subject, from_email, to = 'FERPA Denial Information', 'confirmation@carthage.edu', 'zorpixfang@gmail.com'
                text_content = ''
                html_content = '''Thank you for completing the form regarding your preferences for directory information, as required by FERPA.  Given that you have selected that you do not want directory information released, please note that Carthage will not be able to disclose information such as:
<br><br><li>Dean's List accomplishments to your local newspaper</li>
<li>Verification of enrollment/degree completion for potential or current employers</li>
<li>Your name will not be published in the program for graduation</li>
<br>Please note that you can change your directory information selection at any time, should you wish that Carthage be able to release this type of information.  If you would like to update your preferences, this can be done by completing the electronic form again with your updated selection.'''
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            form.save() #Save the form data to the datbase table
            form = ModelForm()
           # submitted = True
            return render(request, 'consentform/mobile.html', {
                'form': form,
                'submitted': True,
            })
    else:
        form = ModelForm()
        sql = 'SELECT id_rec.id FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_id']))
        student = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        for thing in student:
            form.fields['student_ID'].initial = thing['id']
        sql2 = 'SELECT cc_stg_ferpadirectory.consent FROM cc_stg_ferpadirectory WHERE cc_stg_ferpadirectory.student_id = %d' % (int(request.GET['student_id']))
        student2 = do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
        for thing in student2:
            if thing['consent'] == "N":
                form.fields['consent'].initial = "NOCONSENT"
            else:
                form.fields['consent'].initial = "CONSENT"
        form.fields['student_ID'].widget = forms.HiddenInput()

    return render(request, 'consentform/mobile.html', {
        'form': form,
        'submitted': False,
    })

def get_all_students():
    sql = '''SELECT id_rec.firstname, id_rec.lastname, cf.student_id
            FROM cc_stg_ferpadirectory AS cf
            INNER JOIN id_rec
            ON cf.student_id = id_rec.id'''
    return do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)

def admin(request):
    if request.POST:
        sql2 = '''DELETE FROM cc_stg_ferpadirectory
                WHERE ferpadirectory_no = %s''' % (request.POST['record'])
        do_sql(sql2, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    sql = '''SELECT fd.*, id_rec.firstname, id_rec.lastname
            FROM cc_stg_ferpadirectory AS fd
            INNER JOIN id_rec
            ON fd.student_id = id_rec.id
            ORDER BY fd.datecreated DESC'''
    student = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return render(request, 'consentform/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })

def student(request, student_id):
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
    student = do_sql(sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL)
    return render(request, 'consentform/details.html', {
        'student': student.first(),
        'full_student_list': get_all_students(),
    })

def search(request):
    return student(request, request.POST['cid'])
