from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import RequestContext

from djreggie.createemail.forms import EmailForm
from djreggie.createemail.models import EmailModel

from sqlalchemy import create_engine


@csrf_protect
def index(request):
    if request.POST:
        (a, created) = EmailModel.objects.get_or_create(
            unique_id=request.POST['unique_id']
        )
        form = EmailForm(request.POST)
        form.fields['unique_id'].widget = forms.HiddenInput()
        form.fields['requested_by'].widget = forms.HiddenInput()

        if form.is_valid():
            send_mail(
                "A new email request form is ready to view!",
                form.as_string(), settings.SERVER_MAIL,
                [settings.SERVER_EMAIL]
            )
            form.save()
            form = EmailForm()
            submitted = True
            return render(request, 'createemail/form.html', {
                'form': form,
                'submitted': submitted
            })
    else:
        form = EmailForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = '''
                SELECT
                    id_rec.id, id_rec.fullname
                FROM
                    id_rec WHERE id_rec.id = {}
            '''.format(
                int(request.GET['unique_id'])
            )
            student = connection.execute(sql)
            for thing in student:
                form.fields['unique_id'].initial = thing['id']
                form.fields['requested_by'].initial = thing['fullname']
            connection.close()
        form.fields['unique_id'].widget = forms.HiddenInput()
        form.fields['requested_by'].widget = forms.HiddenInput()

    c = {'form': form, }
    c.update(request)

    return render(request, 'createemail/form.html', {
        'form': form
    })
