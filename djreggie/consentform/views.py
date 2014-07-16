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
        
        #Email stuff should be inside "if form.is_valid()", but for right now, we need to test it. 
        if form.data['consent'] == 'NOCONSENT':
            send_mail("Don\'t do it!", "You\'re making a huge mistake", 'confirmation.carthage.edu',
                ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)   
        
        if form.is_valid(): #If the form is valid
            form.save() #Save the form data to the datbase table
            form = ModelForm()
           # submitted = True
            return render(request, 'consentform/form.html', {
                'form': form,
                'submitted': submitted
            })
    else:
        form = ModelForm()
        engine = create_engine(INFORMIX_EARL_TEST)
        connection = engine.connect()
        sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_ID']))
        student = connection.execute(sql)
        for thing in student:
            form.fields['student_ID'].initial = thing['id']
            form.fields['name'].initial = thing['fullname']
        connection.close()
        form.fields['student_ID'].widget = forms.HiddenInput()
        form.fields['name'].widget = forms.HiddenInput()

    return render(request, 'consentform/form.html', {
    'form': form,
    })
