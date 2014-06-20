#I need all the imports below
from django import forms
from djreggie.createemail.forms import EmailForm
from djreggie.createemail.models import EmailModel
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail #Need this to send email
from django.shortcuts import render
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.views import generic
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF

# Create your views here.    
def index(request):
    if request.POST: #If we do a POST
        (a, created) = EmailModel.objects.get_or_create(unique_id=request.POST['unique_id'])
        form = EmailForm(request.POST) #Scrape the data from the form and save it in a variable
        form.fields['unique_id'].widget = forms.HiddenInput()
        form.fields['requested_by'].widget = forms.HiddenInput()
        
        if form.is_valid(): #If the form is valid
            #syntax: 'subject'      'data to send', 'sender address', 'addresses to send to'
            send_mail("A new email request form is ready to view!",form.as_string(),"Django_Admin", ['zwenta@carthage.edu'])
            form.save()
            form = EmailForm()
            submitted = True
            return render(request, 'createemail/form.html', {
                'form': form,
                'submitted': submitted
            })
            
    else:
        form = EmailForm() #an unbound form
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['unique_id']))
            student = connection.execute(sql)
            for thing in student:
                form.fields['unique_id'].initial = thing['id']
                form.fields['requested_by'].initial = thing['fullname']
            connection.close()
        form.fields['unique_id'].widget = forms.HiddenInput()
        form.fields['requested_by'].widget = forms.HiddenInput()
        
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'form': form,
        }
    c.update(csrf(request))
        
    return render(request, 'createemail/form.html', {
        'form': form
    })

