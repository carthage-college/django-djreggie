# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.mail import send_mail

#Gotta make sure to include your form and model!
from djreggie.systemaccess.models import AccessFormModel
from djreggie.systemaccess.forms import AccessFormForm

def index(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AccessFormForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            #send_mail("email_form",form.as_string(),"this",['zwenta@carthage.edu'])
            # Process the data in form.cleaned_data
            # ...
            form = AccessFormForm()
            submitted = True
            return render(request, 'systemaccess/form.html', {
                'form': form,
                'submitted': submitted
            }) # Redirect after POST
    else:
        form = AccessFormForm() # An unbound form

    return render(request, 'systemaccess/form.html', {
        'form': form,
    })
