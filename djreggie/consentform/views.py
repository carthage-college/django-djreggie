#I need all the imports below
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#Need to include the form object
from djreggie.consentform.form import ModelForm

def create(request):
    if request.POST: #If we do a POST
        form = ModelForm(request.POST) #Scrape the data from the form and save it in a variable
        if form.is_valid(): #If the form is valid
            form.save() #Save the form data to the datbase table
            form = ModelForm()
            submitted = True
            return render(request, 'consentform/form.html', {
                            'form': form,
                            'submitted': submitted
            })
    else:
        form = ModelForm()

    return render(request, 'consentform/form.html', {
    'form': form,
    })
