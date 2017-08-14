from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory

from form import DependForm, FamInfoForm, SincomeForm, StudworkForm, CSForm
from form import ParincomeForm, ParworkForm, OtherinfoForm, CertificationForm
from models import Depend, FamInfo, Studwork, Parwork, CS

import datetime


def create(request):

    FamInfoFormset = formset_factory(FamInfoForm, extra=1)
    StudWorkFormset = formset_factory(StudworkForm, extra=1)
    ParWorkFormset = formset_factory(ParworkForm, extra=1)
    CSFormset = formset_factory(CSForm, extra=1)

    if request.POST:
        formsetfam = FamInfoFormset(request.POST, prefix='fam')
        formsetstud = StudWorkFormset(request.POST, prefix='stud')
        formsetpar = ParWorkFormset(request.POST, prefix='par')
        formsetcs = CSFormset(request.POST, prefix='cs')
        formdepend = DependForm(request.POST, request.FILES)
        formsincome = SincomeForm(request.POST)
        formparincome = ParincomeForm(request.POST)
        formotherinformation = OtherinfoForm(request.POST)
        formcertification = CertificationForm(request.POST)
        if formdepend.is_valid() and formsetcs.is_valid() and \
          formsetpar.is_valid() and formsetstud.is_valid() and \
          formsetfam.is_valid() and formsincome.is_valid() and \
          formparincome.is_valid() and formotherinformation.is_valid() and \
          formcertification.is_valid():
            instance = formdepend.save(commit=False)
            instance.useddata = formsincome.cleaned_data['useddata']
            instance.attached = formsincome.cleaned_data['attached']
            instance.employed = formsincome.cleaned_data['employed']
            instance.useddata2 = formparincome.cleaned_data['useddata2']
            instance.attached2 = formparincome.cleaned_data['attached2']
            instance.employed2 = formparincome.cleaned_data['employed2']
            instance.snapbenfits = formotherinformation.cleaned_data['snapbenefits']
            instance.childsupport = formotherinformation.cleaned_data['childsupport']
            instance.confirm = formcertification.cleaned_data['confirm']
            instance.save()
            for f in formsetfam:
                if f.clean():
                        instance2 = f.save(commit=False)
                        instance2.student = instance
                        instance2.save()
            for f in formsetcs:
                if f.clean():
                        instance2 = f.save(commit=False)
                        instance2.student = instance
                        instance2.save()
            for f in formsetpar:
                if f.clean():
                        instance2 = f.save(commit=False)
                        instance2.student = instance
                        instance2.save()
            for f in formsetstud:
                if f.clean():
                        instance2 = f.save(commit=False)
                        instance2.student = instance
                        instance2.save()
            formsetfam = FamInfoFormset(prefix='fam')
            formsetstud = StudWorkFormset(prefix='stud')
            formsetpar = ParWorkFormset(prefix='par')
            formsetcs = CSFormset(prefix='cs')
            formdepend = DependForm()
            formsincome = SincomeForm()
            formparincome = ParincomeForm()
            formotherinformation = OtherinfoForm()
            formcertification = CertificationForm()
            submitted = True
            return render(request, 'depstudent/design.html', {
                'formsetfam': formsetfam, 'formsetstud': formsetstud,
                'formsetpar': formsetpar, 'formsetcs': formsetcs,
                'formdepend': formdepend, 'formsincome': formsincome,
                'formparincome': formparincome,
                'formotherinformation': formotherinformation,
                'formcertification': formcertification,
                'submitted': submitted,
                'year': datetime.datetime.now().year,
                'year2': datetime.datetime.now().year + 1
            })
    else:
        formsetfam = FamInfoFormset(prefix='fam')
        formsetstud = StudWorkFormset(prefix='stud')
        formsetpar = ParWorkFormset(prefix='par')
        formsetcs = CSFormset(prefix='cs')
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
