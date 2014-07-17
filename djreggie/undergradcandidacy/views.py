#I need all the imports below
import re #For regular expressions
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.core.mail import send_mail

#Including the form class
from djreggie.undergradcandidacy.forms import UndergradForm

# Create your views here.
def index(request):
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    if request.POST: #If we do a POST
        form = UndergradForm(request.POST) #Scrape the data from the form and save it in a variable
        
        
        
        if form.is_valid(): #If the form is valid
            form.save() #'commit=False' - Don't save the data to the database yet
            send_mail("Undergraduate Candidacy Response", "Thank you for submitting the form. Your information is now being reviewed.", 'confirmation.carthage.edu',
            ['zorpixfang@gmail.com', 'mkauth@carthage.edu'], fail_silently=False)
            #Checking if the email is a carthage email
            
            form = UndergradForm()
            submitted = True
            return render(request, 'undergradcandidacy/form.html', {
                'form': form,
                'submitted': submitted,
                'year_low': year,
                'year_up': year+1,
            })
    else:
        form = UndergradForm()
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = '''SELECT IDrec.id, IDrec.firstname, IDrec.middlename, IDrec.lastname,
                    major1.major AS major1code, major2.major AS major2code,
                    major3.major AS major3code, minor1.minor AS minor1code,
                    minor2.minor AS minor2code, minor3.minor AS minor3code
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
                form.fields['fname'].initial = thing['firstname']
                form.fields['mname'].initial = thing['middlename']
                form.fields['lname'].initial = thing['lastname']
                form.fields['major1'].initial = thing['major1code']
                form.fields['major2'].initial = thing['major2code']
                form.fields['major3'].initial = thing['major3code']
                form.fields['minor1'].initial = thing['minor1code']
                form.fields['minor2'].initial = thing['minor2code']
                form.fields['minor3'].initial = thing['minor3code']
            connection.close()
        
    return render(request, 'undergradcandidacy/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1
    })

        

def submitted(request):
    return render(request, 'undergradcandidacy/form.html')