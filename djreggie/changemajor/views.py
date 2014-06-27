from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djreggie.changemajor.forms import ChangeForm
from djreggie.changemajor.models import ChangeModel
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF

def create(request):
    if request.POST: #If we do a POST
        (a, created) = ChangeModel.objects.get_or_create(student_id=request.POST['student_id'])
        form = ChangeForm(request.POST, instance=a) #Scrape the data from the form and save it in a variable
        form.fields['student_id'].widget = forms.HiddenInput()
        form.fields['name'].widget = forms.HiddenInput()
        
        if form.is_valid(): #If the form is valid
            form_instance = form.save()        #Save the form data to the datbase table            
            form = ChangeForm()
            submitted = True
            return render(request, 'changemajor/form.html', {
                'form': form, 
                'submitted': submitted
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ChangeForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['student_id']))
            student = connection.execute(sql)
            for thing in student:
                form.fields['carthage_id'].initial = thing['id']
                form.fields['name'].initial = thing['fullname']
            connection.close()
        form.fields['student_id'].widget = forms.HiddenInput()
        form.fields['name'].widget = forms.HiddenInput()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'form': form,
        }
    c.update(csrf(request))
    
    return render(request, 'changemajor/form.html', {
        'form': form, 
    })

def submitted(request):
    return render(request, 'changemajor/form.html')