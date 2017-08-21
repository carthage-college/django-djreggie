from django.conf import settings
from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.mail import send_mail


from djreggie.changemajor.forms import ChangeForm
from djreggie.changemajor.models import ChangeModel

from djzbar.utils.informix import do_sql
from djzbar.utils.mssql import get_userid

from sqlalchemy import create_engine


def create(request):
    if request.POST:
        # (a, created) = ChangeModel.objects.get_or_create(
        #    student_id=request.POST[student_id]
        # )
        # Scrape the data from the form and save it in a variable
        form = ChangeForm(request.POST)
        # If the form is valid
        if form.is_valid():
            # Save the form data to the datbase table
            form.save()
            form = ChangeForm()
            # This is the URL where users are redirected after
            # submitting the form
            return render(request, 'changemajor/form.html', {
                'form': form,
                'submitted': True
            })
    else:
        # This is for the first time you go to the page. It sets it all up
        form = ChangeForm()
        if request.GET:
            if get_userid(request.GET['student_id']) == None:
                return render(request, 'changemajor/no_access.html')

            # have to have ?student_id= in url for now
            sid = get_userid(request.GET['student_id'])
            # selects student's id, name, and current majors/minors
            #REPLACE(IDrec.fullname,"'","") AS fullname,
            getStudentDetailSQL = '''
                SELECT
                    IDrec.id, IDrec.fullname AS fullname,
                    major1.major AS major1code,
                    TRIM(major1.txt) AS major1,
                    major2.major AS major2code,
                    TRIM(NVL(major2.txt,"")) AS major2,
                    major3.major AS major3code,
                    TRIM(NVL(major3.txt,"")) AS major3,
                    minor1.minor AS minor1code,
                    TRIM(minor1.txt) AS minor1,
                    minor2.minor AS minor2code,
                    TRIM(NVL(minor2.txt,"")) AS minor2,
                    minor3.minor AS minor3code,
                    TRIM(NVL(minor3.txt,"")) AS minor3
                FROM
                    id_rec IDrec
                INNER JOIN
                    prog_enr_rec PROGrec
                ON
                    IDrec.id = PROGrec.id
                LEFT JOIN
                    major_table major1
                ON
                    PROGrec.major1 = major1.major
                LEFT JOIN
                    major_table major2
                ON
                    PROGrec.major2 = major2.major
                LEFT JOIN
                    major_table major3
                ON
                    PROGrec.major3 = major3.major
                LEFT JOIN
                    minor_table minor1
                ON
                    PROGrec.minor1 = minor1.minor
                LEFT JOIN
                    minor_table minor2
                ON
                    PROGrec.minor2 = minor2.minor
                LEFT JOIN
                    minor_table minor3
                ON
                    PROGrec.minor3 = minor3.minor
                WHERE
                    IDrec.id = {}
            '''.format(int(sid))

            student = do_sql(
                getStudentDetailSQL,
                key=settings.INFORMIX_DEBUG,
                earl=settings.INFORMIX_EARL
            )

            for row in student: # set initial data based on student
                form.fields['student_id'].initial = row['id']
                form.fields['name'].initial = row['fullname'].decode(
                    'ISO-8859-2'
                ).encode('utf-8')
                if row['major2'] == '' and row['major3'] == '':
                    form.fields['majorlist'].initial = (row['major1'])
                elif row['major3'] == '':
                    form.fields['majorlist'].initial = "{} and {}".format(
                        row['major1'], row['major2']
                    )
                else:
                    form.fields['majorlist'].initial = "{}, {}, and {}".format(
                        row['major1'], row['major2'], row['major3']
                    )
                if row['minor2'] == '' and row['minor3'] == '':
                    form.fields['minorlist'].initial = (row['minor1'])
                elif row['minor3'] == '':
                    form.fields['minorlist'].initial = "{} and {}".format(
                        row['minor1'], row['minor2']
                    )
                else:
                    form.fields['minorlist'].initial = "{}, {}, and {}".format(
                        row['minor1'], row['minor2'], row['minor3']
                    )
                form.fields['major1'].initial = row['major1code']
                form.fields['major2'].initial = row['major2code']
                form.fields['major3'].initial = row['major3code']
                form.fields['minor1'].initial = row['minor1code']
                form.fields['minor2'].initial = row['minor2code']
                form.fields['minor3'].initial = row['minor3code']

    form.fields['student_id'].widget = forms.HiddenInput()
    form.fields['name'].widget = forms.HiddenInput()
    form.fields['majorlist'].widget = forms.HiddenInput()
    form.fields['minorlist'].widget = forms.HiddenInput()
    # get list of valid advisors for jquery autocomplete
    advisorSQL = '''
        SELECT
            id_rec.id, TRIM(id_rec.firstname) AS firstname,
            TRIM(id_rec.lastname) AS lastname
        FROM
            job_rec INNER JOIN id_rec ON job_rec.id = id_rec.id
        WHERE
            hrstat = 'FT'
        AND
            TODAY BETWEEN job_rec.beg_date AND NVL(job_rec.end_date, TODAY)
        GROUP BY
            id_rec.id, firstname, lastname
        ORDER BY
            lastname, firstname
    '''
    advisor_list = do_sql(
        advisorSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    return render(request, 'changemajor/form.html', {
        'form': form,
        'advisor_list': advisor_list,
        'submitted': False,
    })


def get_all_students():
    """
    function to get a list of all entries in table
    for use in jquery autocomplete
    """
    allStudentSQL = '''
        SELECT
            id_rec.firstname, id_rec.lastname, cm.student_id
        FROM
            cc_stg_changemajor cm
        INNER JOIN
            id_rec
        ON
            cm.student_id = id_rec.id
    '''
    return do_sql(
        allStudentSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )


def admin(request):
    """
    the function for the main admin page
    """
    # if the delete button was clicked. remove entry from database
    if request.POST:
        deleteMajorSQL = '''
            DELETE FROM
                cc_stg_changemajor
            WHERE
                changemajor_no = {}'''.format(request.POST['record'])
        do_sql(
            deleteMajorSQL,
            key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
        )

    # get all entries in database along with advisor full name
    # and major/minor full text
    getListSQL = '''
        SELECT
            cm.*, TRIM(id_rec.firstname) AS firstname,
            TRIM(id_rec.lastname) AS lastname,
            TRIM(advisor.firstname) AS advisor_first,
            TRIM(advisor.lastname) AS advisor_last,
            TRIM(majors1.txt) AS major1_txt,
            TRIM(majors2.txt) AS major2_txt,
            TRIM(majors3.txt) AS major3_txt,
            TRIM(minors1.txt) AS minor1_txt,
            TRIM(minors2.txt) AS minor2_txt,
            TRIM(minors3.txt) AS minor3_txt
        FROM
            cc_stg_changemajor cm
        INNER JOIN  id_rec              ON  cm.student_id   =   id_rec.id
        LEFT JOIN   id_rec      advisor ON  advisor.id      =   cm.advisor_id
        LEFT JOIN   major_table majors1 ON  cm.major1       =   majors1.major
        LEFT JOIN   major_table majors2 ON  cm.major2       =   majors2.major
        LEFT JOIN   major_table majors3 ON  cm.major3       =   majors3.major
        LEFT JOIN   minor_table minors1 ON  cm.minor1       =   minors1.minor
        LEFT JOIN   minor_table minors2 ON  cm.minor2       =   minors2.minor
        LEFT JOIN   minor_table minors3 ON  cm.minor3       =   minors3.minor
        ORDER BY
            cm.approved, cm.datecreated DESC
    '''
    student = do_sql(
        getListSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    all_students = get_all_students()
    return render(request, 'changemajor/home.html', {
        'student':student,
        'full_student_list':all_students
    })


def student(request, changemajor_no): #admin details page
    getStudentSQL = '''
        SELECT
            cm.changemajor_no, cm.student_id, cm.datecreated, cm.datemodified,
            cm.modified_id, cm.approved, cm.advisor_id,
            TRIM(IDrec.firstname) AS firstname,
            TRIM(IDrec.lastname) AS lastname,
            TRIM(IDrec.addr_line1) AS addr_line1,
            TRIM(IDrec.addr_line2) AS addr_line2,
            TRIM(IDrec.city) AS city, TRIM(IDrec.st) AS st, IDrec.zip,
            TRIM(IDrec.ctry) AS ctry, TRIM(IDrec.phone) AS phone,
            TRIM(advisor.firstname) AS advisor_first,
            TRIM(advisor.lastname) AS advisor_last,
            CASE TRIM(PROGrec.cl)
                WHEN    'FF'    THEN    'Freshman'
                WHEN    'FR'    THEN    'Freshman'
                WHEN    'SO'    THEN    'Sophomore'
                WHEN    'JR'    THEN    'Junior'
                WHEN    'SR'    THEN    'Senior'
            END AS classyear,
            TRIM(major1.txt) AS major1, TRIM(major2.txt) AS major2,
            TRIM(major3.txt) AS major3, TRIM(minor1.txt) AS minor1,
            TRIM(minor2.txt) AS minor2, TRIM(minor3.txt) AS minor3,
            TRIM(rmajor1.txt) AS major_txt1, TRIM(rmajor2.txt) AS major_txt2,
            TRIM(rmajor3.txt) AS major_txt3,
            TRIM(rminor1.txt) AS minor_txt1, TRIM(rminor2.txt) AS minor_txt2,
            TRIM(rminor3.txt) AS minor_txt3
        FROM
            cc_stg_changemajor cm
        INNER JOIN
            id_rec        IDrec   ON  cm.student_id   =   IDrec.id
        LEFT JOIN
            id_rec        advisor ON  advisor.id      =   cm.advisor_id
        INNER JOIN
            prog_enr_rec  PROGrec ON  IDrec.id        =   PROGrec.id
        LEFT JOIN
            major_table   major1  ON  PROGrec.major1  =   major1.major
        LEFT JOIN
            major_table   major2  ON  PROGrec.major2  =   major2.major
        LEFT JOIN
            major_table   major3  ON  PROGrec.major3  =   major3.major
        LEFT JOIN
            minor_table   minor1  ON  PROGrec.minor1  =   minor1.minor
        LEFT JOIN
            minor_table   minor2  ON  PROGrec.minor2  =   minor2.minor
        LEFT JOIN
            minor_table   minor3  ON  PROGrec.minor3  =   minor3.minor
        LEFT JOIN
            major_table   rmajor1 ON  cm.major1   =   rmajor1.major
        LEFT JOIN
            major_table   rmajor2 ON  cm.major2   =   rmajor2.major
        LEFT JOIN
            major_table   rmajor3 ON  cm.major3   =   rmajor3.major
        LEFT JOIN
            minor_table   rminor1 ON  cm.minor1   =   rminor1.minor
        LEFT JOIN
            minor_table   rminor2 ON  cm.minor2   =   rminor2.minor
        LEFT JOIN
            minor_table   rminor3 ON  cm.minor3   =   rminor3.minor
        WHERE
            cm.changemajor_no = {}
    '''.format(changemajor_no)
    student_info = do_sql(
        getStudentSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    return render(request, 'changemajor/details.html', {
        'student': student_info.first(),
        #'majors': majors.first(),
        #'reqmajors': reqmajors.first(),
        'full_student_list': get_all_students(),
    })


def search(request): #admin details page access through search bar
    return student(request, request.POST['cid'])


@csrf_exempt
def set_approved(request): #for setting entry to be approved
    getMajorSQL = '''
        SELECT
            CM.changemajor_no, CM.student_id, CM.major1, CM.major2, CM.major3,
            CM.minor1, CM.minor2, CM.minor3, NVL(CM.advisor_id,0) AS advisor_id,
            CM.datecreated, CM.datemodified, NVL(CM.modified_id,0), CM.approved,
            TRIM(id_rec.firstname) || ' ' || TRIM(id_rec.lastname) AS name
        FROM
            cc_stg_changemajor CM
        INNER JOIN
            id_rec
        ON
            CM.student_id = id_rec.id
        WHERE
            changemajor_no = {}
    '''.format(request.POST['id'])
    result = do_sql(
        getMajorSQL, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    student = result.first()

    updateMajorSQL = '''
        UPDATE
            cc_stg_changemajor
        SET
            approved="{approved}", datemodified=CURRENT
        WHERE
            changemajor_no = {id}'''.format(
            request.POST['approved'],
            request.POST['id']
        )
    do_sql(
        updateMajorSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    if request.POST["approved"] == "Y":
        student_email = getEmailById(student['student_id'])
        send_mail(
            "Congratulations - Major/Minor/Advisor Change Accepted",
            '''Please accept this email as notification that your change of Major/Minor/Advisor has been accepted by the Registrar's Office and your record has been updated.
            \n\nGiven this approved change, you should be able to view your updated graduation requirements within your Degree Audit (which is accessible through my.carthage.edu).''',
            'Brigid Patterson <bpatterson@carthage.edu>', [student_email]
        )

        # if they put in an new advisor
        if student['advisor_id'] != 0:
            # get new advisor's email
            advisor_email = getEmailById(student['advisor_id'])
            # TODO: replace hard-coded emails with [advisor_email]
            # and put into template using djtool's send_mail
            # email new advisor
            send_mail(
                "New Advisee Notification",
                '''Please accept this email as notification that the following student has selected you as their advisor. Given this, you are now able to view their Degree Audit information through my.carthage.edu to assist in your advising of this student.\n
                \nStudent name:{}
                \nStudent ID: {}'''.format(student['name'], student['student_id']),
                'Brigid Patterson <bpatterson@carthage.edu>',
                [advisor_email], fail_silently=False
            )

        updateProgEnrRecSQL = '''
            UPDATE
                prog_enr_rec
            SET
                major1 = (CASE WHEN "{major1}" = "None" THEN "" ELSE "{major1}" END),
                major2 = (CASE WHEN "{major2}" = "None" THEN "" ELSE "{major2}" END),
                major3 = (CASE WHEN "{major3}" = "None" THEN "" ELSE "{major3}" END),
                minor1 = (CASE WHEN "{minor1}" = "None" THEN "" ELSE "{minor1}" END),
                minor2 = (CASE WHEN "{minor2}" = "None" THEN "" ELSE "{minor2}" END),
                minor3 = (CASE WHEN "{minor3}" = "None" THEN "" ELSE "{minor3}" END)
        '''.format(**student)
        # if advisor id exists then update that field in the database
        # otherwise don't
        if student['advisor_id']:
            updateProgEnrRecSQL += ', adv_id = %s' % (student['advisor_id'])
        updateProgEnrRecSQL += ' WHERE id = %s' % (student['student_id'])
        do_sql(
            updateProgEnrRecSQL,
            key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
        )
    return HttpResponse('update successful')


def getEmailById(cx_id):
    email_sql = '''
        SELECT
            TRIM(aa_rec.line1) AS email
        FROM
            aa_rec
        WHERE
            id = {}
        AND
            aa = "EML1"
        AND
            TODAY BETWEEN beg_date AND NVL(end_date, TODAY)
    '''.format(cx_id)
    email = do_sql(
        email_sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    return email.first()['email']

