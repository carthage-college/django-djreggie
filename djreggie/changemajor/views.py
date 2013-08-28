from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

#Need to import the form
from djreggie.changemajor.forms import StudentForm

# Create your views here.    
def index(request):
    if request.POST: #If we do a POST
        form = StudentForm(request.POST) #Scrape the data from the form and save it in a variable
        if form.is_valid(): #If the form is valid
            form.save() #Save the form data to the datbase table
            form = StudentForm()
            submitted = True
            return render(request, 'changemajor/form.html', {
                            'form': form,
                            'submitted': submitted
            })
    else:
        form = StudentForm() #An unbonded form
    
    return render(request, 'changemajor/form.html', {
        'form': form
    })
