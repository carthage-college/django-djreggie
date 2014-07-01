#I need all the imports below
import re #For regular expressions
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date

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
            obj = form.save(commit=False) #'commit=False' - Don't save the data to the database yet
            
            #Checking if the email is a carthage email
            if re.search('^.*@carthage\.edu$', form.cleaned_data['email']) != None:
                obj.carthage_email = True
            obj.save()
            
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
        
    return render(request, 'undergradcandidacy/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1
    })

        

def submitted(request):
    return render(request, 'undergradcandidacy/form.html')