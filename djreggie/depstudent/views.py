from django.shortcuts import render
from django.http import HttpResponse
from form import DependForm, FamInfoForm, SincomeForm, StudworkForm, ParincomeForm, ParworkForm, OtherinfoForm, CSForm, CertificationForm
from models import Depend, FamInfo, Sincome, Studwork, Parincome, Parwork,  Otherinfo, CS, certification
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
import datetime

def create(request):
    
    FamInfoFormset = formset_factory(FamInfoForm, extra=10)
    StudWorkFormset = formset_factory(StudworkForm, extra=6)
    ParWorkFormset = formset_factory(ParworkForm, extra=6)
    CSFormset = formset_factory(CSForm, extra=8)
    
    if request.POST:
        formsetfam = FamInfoFormset(request.POST)
        formsetstud = StudWorkFormset(request.POST)
        formsetpar = ParWorkFormset(request.POST)
        formsetcs = CSFormset(request.POST)
        formdepend = DependForm(request.POST, request.FILES)
        formsincome = SincomeForm(request.POST)
        formparincome = ParincomeForm(request.POST)
        formotherinformation = OtherinfoForm(request.POST)
        formcertification = CertificationForm(request.POST)

        if formdepend.is_valid() and formsetcs.is_valid() and formsetpar.is_valid() and formsetstud.is_valid() and formsetfam.is_valid() and formsincome.is_valid() and formparincome.is_valid() and formotherinformation.is_valid() and formcertification.is_valid():
            newdoc = Depend(file = request.FILES['file'])
            newdoc.save()
            formsincome.save()
            formparincome.save()
            formotherinformation.save()
            formcertification.save()
            for f in formsetfam:
                f.clean()
            for f in formsetcs:
                f.clean()
            for f in formsetpar:
                f.clean()
            for f in formsetstud:
                f.clean()
            formsetfam = FamInfoFormset()
            formsetstud = StudWorkFormset()
            formsetpar = ParWorkFormset()
            formsetcs = CSFormset()
            formdepend = DependForm()
            formsincome = SincomeForm()
            formparincome = ParincomeForm()
            formotherinformation = OtherinfoForm()
            formcertification = CertificationForm()
            submitted = True
            return render(request, 'depstudent/design.html', {'formsetfam': formsetfam, 'formsetstud': formsetstud, 'formsetpar': formsetpar, 'formsetcs': formsetcs, 'formdepend': formdepend, 'formsincome': formsincome, 'formparincome': formparincome, 'formotherinformation': formotherinformation, 'formcertification': formcertification, 'submitted': submitted})
    else:
        formsetfam = FamInfoFormset()
        formsetstud = StudWorkFormset()
        formsetpar = ParWorkFormset()
        formsetcs = CSFormset()
        formdepend = DependForm()
        formsincome = SincomeForm()
        formparincome = ParincomeForm()
        formotherinformation = OtherinfoForm()
        formcertification = CertificationForm()
    return render(request, 'depstudent/design.html', {
        'formsetfam': formsetfam,
        'formsetstud': formsetstud,
        'formsetpar': formsetpar,
        'formsetcs': formsetcs,
        'formdepend': formdepend,
        'formsincome': formsincome,
        'formparincome': formparincome,
        'formotherinformation': formotherinformation,
        'formcertification': formcertification,
        'year00': datetime.datetime.now().year - 2,
        'year0': datetime.datetime.now().year - 1,
        'year': datetime.datetime.now().year,
        'year2': datetime.datetime.now().year + 1
    })
