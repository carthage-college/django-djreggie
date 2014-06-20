#You need all the imports below. Be sure to change the names of the models and forms accordingly!
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djreggie.consentfam.form import ModelForm, Parent
from djreggie.consentfam.models import ConsentModel, ParentForm, Contact
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from django.forms.formsets import formset_factory, BaseFormSet #For formsets
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF

def create(request):
    #For info on setting up formsets, see this link: http://goo.gl/Oz53K2
    ParentFormSet = formset_factory(Parent)
    if request.POST:    #If we do a POST        
        (a, created) = ConsentModel.objects.get_or_create(Carthage_ID_Number=request.POST['Carthage_ID_Number'])    
        form = ModelForm(request.POST, instance=a)#Scrape the data from the form and save it in a variable
        form.fields['Carthage_ID_Number'].widget = forms.HiddenInput()
        form.fields['Full_Name_of_Student'].widget = forms.HiddenInput()
        
        #Scrape the data from the form and save it in a variable
        Parent_formset = ParentFormSet(request.POST, prefix='Parent_or_Third_Party_Name')
           
        if form.is_valid() and Parent_formset.is_valid(): #If the forms are valid
            form_instance = form.save()        #Save the form data to the datbase table            
            
            for f in Parent_formset:#This is how we save formset data, since there are multiple forms in a formset
               share_with = f.save(commit=False)
               share_with.list = form_instance
               share_with.save()
            form = ModelForm()
            Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')
            submitted = True
            return render(request, 'consentfam/form.html', {
                'form': form, 
                'Parent_formset': Parent_formset,
                'submitted': submitted
            })#This is the URL where users are redirected after submitting the form
    else: #This is for the first time you go to the page. It sets it all up
        form = ModelForm()
        Parent_formset = ParentFormSet(prefix='Parent_or_Third_Party_Name')
        if request.GET:
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            sql = 'SELECT id_rec.id, id_rec.fullname FROM id_rec WHERE id_rec.id = %d' % (int(request.GET['Carthage_ID_Number']))
            student = connection.execute(sql)
            for thing in student:
                form.fields['Carthage_ID_Number'].initial = thing['id']
                form.fields['Full_Name_of_Student'].initial = thing['fullname']
            connection.close()
        form.fields['Carthage_ID_Number'].widget = forms.HiddenInput()
        form.fields['Full_Name_of_Student'].widget = forms.HiddenInput()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'form': form,
         'Parent_formset': Parent_formset,
        }
    c.update(csrf(request))

    return render(request, 'consentfam/form.html', {
        'form': form, 
        'Parent_formset': Parent_formset,
    })
    
def submitted(request):
    return render(request, 'consentfam/form.html')
