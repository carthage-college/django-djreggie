from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.mail import send_mail

from djreggie.systemaccess.models import AccessFormModel
from djreggie.systemaccess.forms import AccessFormForm

def index(request):
    if request.method == 'POST':
        form = AccessFormForm(request.POST)
        if form.is_valid():
            form.save()
            #send_mail(
            #    "email_form",form.as_string(),"this",[settings.SERVER_EMAIL,]
            #)
            form = AccessFormForm()
            submitted = True
            return render(request, 'systemaccess/form.html', {
                'form': form,
                'submitted': submitted
            })
    else:
        form = AccessFormForm()

    return render(request, 'systemaccess/form.html', {
        'form': form,
    })
