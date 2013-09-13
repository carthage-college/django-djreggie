from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from djzbar.settings import INFORMIX_EARL_TEST
from sqlalchemy import create_engine
from models import Major, Student

#SQL Alchemy

#Need to import the form
from djreggie.changemajor.forms import StudentForm, MajorMinorForm
def set_major_choices(form, selected):
        selected_choices = []
        majors_list = list(form.fields['majors_list'].widget.choices)
        for major in majors_list:
                if major[0] in selected:
                        selected_choices.append(major)
                        majors_list.remove(major)
        form.fields['majors_list'].widget.choices = tuple(majors_list)
        form.fields['majors'].widget.choices = tuple(selected_choices)
        
def set_minor_choices(form, selected):
        selected_choices = []
        minors_list = list(form.fields['minors_list'].widget.choices)
        for minor in minors_list:
                if minor[0] in selected:
                        selected_choices.append(minor)
                        minors_list.remove(minor)
        form.fields['minors_list'].widget.choices = tuple(minors_list)
        form.fields['minors'].widget.choices = tuple(selected_choices)
        
# Create your views here.    
def index(request):
    if request.POST: #If we do a POST
        form = StudentForm(request.POST) #Scrape the data from the form and save it in a variable
        mm_form = MajorMinorForm(request.POST)
        major_list = request.POST.getlist('majors')
        minor_list = request.POST.getlist('minors')
        set_major_choices(mm_form, major_list)
        set_minor_choices(mm_form, minor_list)
        if form.is_valid() and mm_form.is_valid(): #If the form is valid
            instance = form.save(commit=False) #Save the form data to the datbase table
            major_list = request.POST.getlist('majors')
            minor_list = request.POST.getlist('minors')
            instance.save()
            engine = create_engine(INFORMIX_EARL_TEST)
            connection = engine.connect()
            for m in major_list:
                    sql = "SELECT txt FROM major_table WHERE major = '%s'" % (m)
                    txt = connection.execute(sql)
                    (major, created) = Major.objects.get_or_create(major=m, defaults={'txt': txt})
                    instance.majors.add(major)
            for m in minor_list:
                    sql = "SELECT txt FROM minor_table WHERE minor = '%s'" % (m)
                    txt = connection.execute(sql)
                    (minor, created) = Minor.objects.get_or_create(minor=m, defaults={'txt': txt})
                    instance.minors.add(minor)
            connection.close()
            form.save_m2m()
            form = StudentForm()
            mm_form = MajorMinorForm()
            submitted = True
            
            return render(request, 'changemajor/form.html', {
                            'form': form,
                            'mm_form': mm_form,
                            'submitted': submitted
            })
    else:
        form = StudentForm() #An unbonded form
        mm_form = MajorMinorForm()
        if request.GET:
                engine = create_engine(INFORMIX_EARL_TEST)
                connection = engine.connect()
                sql = 'SELECT student.id, student.firstname AS stu_fname, student.lastname AS stu_lname, prog_enr_rec.major1, prog_enr_rec.major2, prog_enr_rec.major3, prog_enr_rec.minor1, prog_enr_rec.minor2, prog_enr_rec.minor3, advisor.firstname AS adv_fname, advisor.lastname AS adv_lname, prog_enr_rec.cl FROM id_rec AS student, id_rec AS advisor, prog_enr_rec WHERE student.id = prog_enr_rec.id AND prog_enr_rec.adv_id = advisor.id AND student.id = %d' % (int(request.GET['student_id']))
                student = connection.execute(sql)
                for thing in student:
                        form.fields['student_id'].initial = thing['id']
                        form.fields['name'].initial = '%s %s' % (thing['stu_fname'], thing['stu_lname'])
                        form.fields['year'].initial = thing['cl']
                        form.fields['advisor'].initial = '%s %s' % (thing['adv_fname'], thing['adv_lname'])
                        set_major_choices(mm_form, [thing['major1'], thing['major2'], thing['major3']])
                        set_minor_choices(mm_form, [thing['minor1'], thing['minor2'], thing['minor3']])
                connection.close()
                
    return render(request, 'changemajor/form.html', {
        'form': form,
        'mm_form': mm_form,
    })
