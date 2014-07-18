from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from forms import ChangeForm
from models import ChangeModel
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF
from django.core.mail import send_mail

def create(request):
    if request.POST: #If we do a POST            
        #(a, created) = ChangeModel.objects.get_or_create(student_id=request.POST[student_id])
        form = ChangeForm(request.POST) #Scrape the data from the form and save it in a variable
        
        if form.is_valid(): #If the form is valid
            if form.data['advisor'] != '':
                send_mail("You can't replace me, I'm the advisor!", "I'm the captai- er, advisor now", 'confirmation.carthage.edu',
                    ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
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
            sql = '''SELECT IDrec.id, IDrec.fullname, major1.major AS major1code,
                    TRIM(major1.txt) AS major1, major2.major AS major2code, TRIM(major2.txt) AS major2,
                    major3.major AS major3code, TRIM(major3.txt) AS major3, minor1.minor AS minor1code,
                    TRIM(minor1.txt) AS minor1, minor2.minor AS minor2code, TRIM(minor2.txt) AS minor2,
                    minor3.minor AS minor3code, TRIM(minor3.txt) AS minor3
FROM id_rec	IDrec	INNER JOIN	prog_enr_rec	PROGrec	ON	IDrec.id		=	PROGrec.id
					LEFT JOIN	major_table		major1	ON	PROGrec.major1	=	major1.major
					LEFT JOIN	major_table		major2	ON	PROGrec.major2	=	major2.major
					LEFT JOIN	major_table		major3	ON	PROGrec.major3	=	major3.major
					LEFT JOIN	minor_table		minor1	ON	PROGrec.minor1	=	minor1.minor
					LEFT JOIN	minor_table		minor2	ON	PROGrec.minor2	=	minor2.minor
					LEFT JOIN	minor_table		minor3	ON	PROGrec.minor3	=	minor3.minor
WHERE IDrec.id = %d''' % (int(request.GET['student_id']))
            student = connection.execute(sql)
            for thing in student:
                form.fields['student_id'].initial = thing['id']
                form.fields['name'].initial = thing['fullname']
                if thing['major2'] == None and thing['major3'] == None:
                    form.fields['majorlist'].initial = (thing['major1'])
                elif thing['major3'] == None:
                    form.fields['majorlist'].initial = "%s and %s" % (thing['major1'], thing['major2'])
                else:
                    form.fields['majorlist'].initial = "%s, %s, and %s" % (thing['major1'], thing['major2'],thing['major3'])
                if thing['minor2'] == None and thing['minor3'] == None:
                    form.fields['minorlist'].initial = (thing['minor1'])
                elif thing['minor3'] == None:
                    form.fields['minorlist'].initial = "%s and %s" % (thing['minor1'], thing['minor2'])
                else:
                    form.fields['minorlist'].initial = "%s, %s, and %s" % (thing['minor1'], thing['minor2'],thing['minor3'])
                form.fields['major1'].initial = thing['major1code']
                form.fields['major2'].initial = thing['major2code']
                form.fields['major3'].initial = thing['major3code']
                form.fields['minor1'].initial = thing['minor1code']
                form.fields['minor2'].initial = thing['minor2code']
                form.fields['minor3'].initial = thing['minor3code']
            connection.close()
        form.fields['student_id'].widget = forms.HiddenInput()
        form.fields['name'].widget = forms.HiddenInput()
        form.fields['majorlist'].widget = forms.HiddenInput()
        form.fields['minorlist'].widget = forms.HiddenInput()

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