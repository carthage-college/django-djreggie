from django.shortcuts import render
from django.http import HttpResponse
from form import DependForm, FamInfoForm, SincomeForm, StudworkForm, OtherinfoForm, CSForm, CertificationForm
from models import Independ, FamInfo, Sincome, Studwork, Otherinfo, CS, certification
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

def create(request):
    
    FamInfoFormset = formset_factory(FamInfoForm, extra=10)
    StudWorkFormset = formset_factory(StudworkForm, extra=6)
    CSFormset = formset_factory(CSForm, extra=8)
    
    if request.POST:
        formsetfam = FamInfoFormset(request.POST)
        formsetstud = StudWorkFormset(request.POST)
        formsetcs = CSFormset(request.POST)
        formdepend = DependForm(request.POST)
        formsincome = SincomeForm(request.POST)
        formotherinformation = OtherinfoForm(request.POST)
        formcertification = CertificationForm(request.POST)

        if formdepend.is_valid() and formsetcs.is_valid() and formsetstud.is_valid() and formsetfam.is_valid() and formsincome.is_valid() and formotherinformation.is_valid() and formcertification.is_valid():
            formdepend.save()
            formsincome.save()
            formotherinformation.save()
            formcertification.save()
            for f in formsetfam:
                f.clean()
            for f in formsetcs:
                f.clean()
            for f in formsetstud:
                f.clean()
            formsetfam = FamInfoFormset()
            formsetstud = StudWorkFormset()
            formsetcs = CSFormset()
            formdepend = DependForm()
            formsincome = SincomeForm()
            formotherinformation = OtherinfoForm()
            formcertification = CertificationForm()
            submitted = True
            return render(request, 'indepstudent/design.html', {'formsetfam': formsetfam, 'formsetstud': formsetstud, 'formsetcs': formsetcs, 'formdepend': formdepend, 'formsincome': formsincome, 'formotherinformation': formotherinformation, 'formcertification': formcertification, 'submitted': submitted})
    else:
        formsetfam = FamInfoFormset()
        formsetstud = StudWorkFormset()
        formsetcs = CSFormset()
        formdepend = DependForm()
        formsincome = SincomeForm()
        formotherinformation = OtherinfoForm()
        formcertification = CertificationForm()
    return render(request, 'indepstudent/design.html', {'formsetfam': formsetfam, 'formsetstud': formsetstud, 'formsetcs': formsetcs, 'formdepend': formdepend, 'formsincome': formsincome, 'formotherinformation': formotherinformation, 'formcertification': formcertification})
