#I need all the imports below
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail #Need this to send email
from django.shortcuts import render
from django.views import generic

from djreggie.createemail.forms import EmailForm
from djreggie.createemail.models import EmailModel
# Create your views here.
    
def index(request):
    if request.method == 'POST': #If we do a POST
        form = EmailForm(request.POST) #Scrape the data from the form and save it in a variable
        if form.is_valid(): #If the form is valid
            #syntax: 'subject'      'data to send', 'sender address', 'addresses to send to'
            send_mail("email form",form.as_string(),"this", ['zwenta@carthage.edu'])
            form.save()
            form = EmailForm()
            submitted = True
            return render(request, 'createemail/form.html', {
                'form': form,
                'submitted': submitted
            })
            
    else:
        form = EmailForm() #an unbound form
        
    return render(request, 'createemail/form.html', {
        'form': form
    })

