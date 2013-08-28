#You need all the imports below. Be sure to change the names of the models and forms accordingly!
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djreggie.consentfam.form import ModelForm, Parent
from djreggie.consentfam.models import Form, ParentForm, Contact
#Import this if you'll be using formsets
from django.forms.formsets import formset_factory

def create(request):
    ParentFormSet = formset_factory(Parent, extra=1)
    boolean = False
    if request.POST:    #If we do a POST    
        Parent_formset = ParentFormSet(request.POST, prefix='Parent_or_Third_Party_Name')#Scrape the data from the form and save it in a variable
        if 'add' in request.POST: #This is the algorithm for dynamically adding to our formset.
            boolean = True
            list=[]
            for i in range(0,int(Parent_formset.data['Parent_or_Third_Party_Name-TOTAL_FORMS'])):
                list.append({'name': Parent_formset.data['Parent_or_Third_Party_Name-%s-name' % (i)], 'Relation': Parent_formset.data['Parent_or_Third_Party_Name-%s-Relation' % (i)]})
            Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name', initial= list)
        form = ModelForm(request.POST)#Scrape the data from the form and save it in a variable
        if form.is_valid() and Parent_formset.is_valid(): #If the forms are valid
            form_instance = form.save()        #Save the form data to the datbase table            
            
            for f in Parent_formset:#This is how we save formset data, since there are multiple forms in a formset
                if f.clean():
                    (contobj, created) = Contact.objects.get_or_create(name=f.cleaned_data['name'])
                    (obj, created) = ParentForm.objects.get_or_create(form=form_instance, contact=contobj, Relation=f.cleaned_data['Relation'])
            form = ModelForm()
            Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')
            submitted = True
            return render(request, 'consentfam/form.html', {
                'form': form, 
                'Parent_formset': Parent_formset,
                'bool': boolean,
                'submitted': submitted
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ModelForm()
        Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')

    return render(request, 'consentfam/form.html', {
        'form': form, 
        'Parent_formset': Parent_formset,
        'bool': boolean,
    })
    
def submitted(request):
    return render(request, 'consentfam/form.html')
