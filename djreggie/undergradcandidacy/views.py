from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect

from djreggie.undergradcandidacy.forms import UndergradForm
from djreggie.core.utils import get_email

from djzbar.utils.informix import do_sql
from djzbar.utils.mssql import get_userid
from djzbar.decorators.auth import portal_auth_required

from djtools.utils.mail import send_mail

from datetime import date
import re

DEBUG=settings.INFORMIX_DEBUG
EARL=settings.INFORMIX_EARL


def index(request):
    valid_class = 'Y'
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    perm = None
    if request.POST:
        form = UndergradForm(request.POST)

        perm = getPermAddress(int(request.POST['student_id']))
        if form.is_valid():
            data = form.save()
            # email on valid submit
            studentEmail = get_email(request.POST['student_id'])

            if settings.DEBUG:
                to_list = [settings.SERVER_EMAIL]
            else:
                to_list = [studentEmail]

            send_mail(
                request, to_list,
                "Candidacy Received and Pending Approval",
                settings.REGISTRAR_EMAIL,
                'undergradcandidacy/email_submitted.html',
                {'data':data,}, settings.MANAGERS
            )


            form = populateForm(int(request.POST['student_id']))
            valid_class = isValidClass(int(request.POST['student_id']))
            return render(request, 'undergradcandidacy/form.html', {
                'form': form,
                'submitted': True,
                'year_low': year,
                'year_up': year+1,
                'userid':request.GET['student_id'],
                'valid_class': valid_class
            })
    else:
        if request.GET:
            suid = request.GET.get('student_id')
            guid = get_userid(suid)
            if not suid or guid == None:
                return render(
                    request, 'undergradcandidacy/no_access.html'
                )

            cxID = int(guid)
            form = populateForm(cxID)
            valid_class = isValidClass(cxID)
            perm = getPermAddress(cxID)
        else:
            form = UndergradForm()

    return render(request, 'undergradcandidacy/form.html', {
        'form': form,
        'year_low': year,
        'year_up': year+1,
        'valid_class': valid_class,
        'submitted': False,
        'perm': perm,
        'userid': request.GET.get('student_id')
    })


def populateForm(student_id):
    form = UndergradForm()
    # get student's id, name, and majors/minors
    getStudentSQL = '''
        SELECT
            IDrec.id, TRIM(IDrec.firstname) AS firstname,
            TRIM(IDrec.middlename) AS middlename,
            TRIM(IDrec.lastname) AS lastname,
            TRIM(major1.major) AS major1code, TRIM(major2.major) AS major2code,
            TRIM(major3.major) AS major3code, TRIM(minor1.minor) AS minor1code,
            TRIM(minor2.minor) AS minor2code, TRIM(minor3.minor) AS minor3code
        FROM
            id_rec IDrec
        INNER JOIN
            prog_enr_rec PROGrec ON IDrec.id = PROGrec.id
        LEFT JOIN
            major_table major1 ON PROGrec.major1 = major1.major
        LEFT JOIN
            major_table major2 ON PROGrec.major2 = major2.major
        LEFT JOIN
            major_table major3 ON PROGrec.major3 = major3.major
        LEFT JOIN
            minor_table minor1 ON PROGrec.minor1 = minor1.minor
        LEFT JOIN
            minor_table minor2 ON PROGrec.minor2 = minor2.minor
        LEFT JOIN
            minor_table minor3 ON PROGrec.minor3 = minor3.minor
        WHERE
            IDrec.id = {}
    '''.format(student_id)

    student = do_sql(getStudentSQL, key=DEBUG, earl=EARL)

    # set student's initial data
    for row in student:
        form.fields['student_id'].initial = row['id']
        form.fields['fname'].initial = row['firstname']
        form.fields['mname'].initial = row['middlename']
        form.fields['lname'].initial = row['lastname']
        form.fields['major1'].initial = row['major1code']
        form.fields['major2'].initial = row['major2code']
        form.fields['major3'].initial = row['major3code']
        form.fields['minor1'].initial = row['minor1code']
        form.fields['minor2'].initial = row['minor2code']
        form.fields['minor3'].initial = row['minor3code']

    return form


def isValidClass(student_id):
    # check if student is a junior/senior or not
    getClassStandingSQL = '''
        SELECT
            CASE prog_enr_rec.cl
                WHEN    'JR'    THEN 'Y'
                WHEN    'SR'    THEN 'Y'
                                ELSE 'N'
            END AS valid_class
        FROM prog_enr_rec
        WHERE prog_enr_rec.id = {}
    '''.format(student_id)
    class_standing = do_sql(getClassStandingSQL, key=DEBUG, earl=EARL)

    try:
        cs = class_standing.first()['valid_class']
    except:
        cs = None
    return cs


@portal_auth_required(
    session_var='DJREGGIE_AUTH',
    group='Registrar',
    redirect_url=reverse_lazy('access_denied')
)
def contact(request):
    '''
    retrieves student's contact info from form through ajax call
    '''

    getContactSQL = '''
        SELECT
            *
        FROM
            aa_rec
        WHERE
            id = {id}
        AND
            aa = "{aa}"
        AND
            TODAY BETWEEN beg_date AND NVL(end_date, TODAY)
    '''.format(
        request.GET['id'], request.GET['aa']
    )
    contactinfo = do_sql(getContactSQL, key=DEBUG, earl=EARL)
    data = ''
    for row in contactinfo:
        # we order the data this way so we can put it into a dict
        # when it's recieved. HttpResponse only sends strings
        for key in contactinfo.keys():
            data = data + key + ':' + str(row[key]) + ','
    return HttpResponse(data)


def get_all_students():
    '''
    retrieve all entries in table for use by jquery autocomplete
    '''

    sql = '''
        SELECT
            first_name, last_name, middle_initial, student_id
        FROM
            cc_stg_undergrad_candidacy
    '''
    return do_sql(sql, key=DEBUG, earl=EARL)


@portal_auth_required(
    session_var='DJREGGIE_AUTH',
    group='Registrar',
    redirect_url=reverse_lazy('access_denied')
)
def admin(request):
    '''
    main admin page
    '''

    # if delete button was clicked. removes entry from database
    if request.POST:
        deleteRowSQL = '''
            DELETE FROM cc_stg_undergrad_candidacy
            WHERE undergradcandidacy_no = {}
        '''.format(request.POST.get('record'))
        do_sql(deleteRowSQL, key=DEBUG, earl=EARL)
    # retrieves all entries along with majors/minors full text
    getMajorMinorSQL = '''
        SELECT
            uc.*,
            CASE WHEN
                uc.aa == 'PHN' AND LENGTH(uc.aa_value) = 10
            THEN
                uc.aa_value[1,3] || '-' || uc.aa_value[4,6] || '-' || uc.aa_value[7,10]
            ELSE
                uc.aa_value
            END AS formatted_contact,
            TRIM(majors1.txt) AS major1_txt, TRIM(majors2.txt) AS major2_txt,
            TRIM(majors3.txt) AS major3_txt, TRIM(minors1.txt) AS minor1_txt,
            TRIM(minors2.txt) AS minor2_txt, TRIM(minors3.txt) AS minor3_txt
        FROM
            cc_stg_undergrad_candidacy uc
        LEFT JOIN major_table majors1 ON uc.major1 = majors1.major
        LEFT JOIN major_table majors2 ON uc.major2 = majors2.major
        LEFT JOIN major_table majors3 ON uc.major3 = majors3.major
        LEFT JOIN minor_table minors1 ON uc.minor1 = minors1.minor
        LEFT JOIN minor_table minors2 ON uc.minor2 = minors2.minor
        LEFT JOIN minor_table minors3 ON uc.minor3 = minors3.minor
        ORDER BY
            uc.approved, uc.datecreated DESC
    '''
    student = do_sql(getMajorMinorSQL, key=DEBUG, earl=EARL)

    return render(request, 'undergradcandidacy/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })


@portal_auth_required(
    session_var='DJREGGIE_AUTH',
    group='Registrar',
    redirect_url=reverse_lazy('access_denied')
)
def student(request, student_id):
    """
    admin details page
    """

    # retrieves entry's info
    getStudentSQL = '''
        SELECT uc.*,
            TRIM(id_rec.addr_line1) AS addr_line1,
            TRIM(id_rec.addr_line2) AS addr_line2,
            TRIM(id_rec.city) AS rec_city, TRIM(id_rec.st) AS st,
            TRIM(id_rec.zip) AS rec_zip, TRIM(id_rec.ctry) AS ctry,
            TRIM(id_rec.phone) AS phone, uc.diploma_aa_type AS diploma_type,
            CASE
                uc.diploma_aa_type
            WHEN
                'DIPL'
            THEN
                uc.address
            ELSE
                TRIM(id_rec.addr_line1 || ' ' || id_rec.addr_line2)
            END AS dipl_addr,
            CASE
                uc.diploma_aa_type
            WHEN
                'DIPL'
            THEN
                uc.city
            ELSE
                TRIM(id_rec.city)
            END AS dipl_city,
            CASE
                uc.diploma_aa_type
            WHEN
                'DIPL'
            THEN
                uc.state
            ELSE
                TRIM(id_rec.st)
            END AS dipl_st,
            CASE
                uc.diploma_aa_type
            WHEN
                'DIPL'
            THEN
                uc.zip
            ELSE
                TRIM(id_rec.zip)
            END AS dipl_zip
        FROM
            cc_stg_undergrad_candidacy uc
        INNER JOIN
            id_rec
        ON
            uc.student_id = id_rec.id
        WHERE
    '''.format(student_id)

    try:
        sid = int(student_id)
        where = 'uc.student_id = {}'.format(student_id)
    except:
        where = 'uc.last_name = "{}"'.format(student_id)
    sql = '{} {}'.format(getStudentSQL, where)
    student = do_sql(sql, key=DEBUG, earl=EARL)

    # deal with funky characters
    stu = {}
    student = student.first()
    if student:
        for key, value in student.items():
            try:
                stu[key] = u'{}'.format(value.decode('utf-8').encode('cp1252'))
            except:
                try:
                    stu[key] = u'{}'.format(value.decode('latin-1'))
                except:
                    stu[key] = value
        student = stu

    # retrieves majors/minors full text
    getMajorMinorSQL = '''
        SELECT
            TRIM(major1.txt) AS major_txt1, TRIM(major2.txt) AS major_txt2,
            TRIM(major3.txt) AS major_txt3, TRIM(minor1.txt) AS minor_txt1,
            TRIM(minor2.txt) AS minor_txt2, TRIM(minor3.txt) AS minor_txt3
        FROM
            cc_stg_undergrad_candidacy uc
        LEFT JOIN
            major_table major1 ON uc.major1 = major1.major
        LEFT JOIN
            major_table major2 ON uc.major2 = major2.major
        LEFT JOIN
            major_table major3 ON uc.major3 = major3.major
        LEFT JOIN
            minor_table minor1 ON uc.minor1 = minor1.minor
        LEFT JOIN
            minor_table minor2 ON uc.minor2 = minor2.minor
        LEFT JOIN
            minor_table minor3 ON uc.minor3 = minor3.minor
        WHERE
    '''.format(student_id)

    try:
        sid = int(student_id)
        where = 'uc.student_id = {}'.format(student_id)
    except:
        where = 'uc.last_name = "{}"'.format(student_id)
    sql = '{} {}'.format(getStudentSQL, where)

    reqmajors = do_sql(sql, key=DEBUG, earl=EARL)

    return render(request, 'undergradcandidacy/details.html', {
        'student': student,
        'reqmajors': reqmajors.first(),
        'full_student_list': get_all_students(),
    })


@portal_auth_required(
    session_var='DJREGGIE_AUTH',
    group='Registrar',
    redirect_url=reverse_lazy('access_denied')
)
def search(request):
    '''
    admin details page accessed through search bar
    '''
    return student(request, request.POST.get('cid'))


@csrf_exempt
@portal_auth_required(
    session_var='DJREGGIE_AUTH',
    group='Registrar',
    redirect_url=reverse_lazy('access_denied')
)
def set_approved(request):
    '''
    set the approved column in database for entry
    '''

    updateCandidacySQL = '''
        UPDATE
            cc_stg_undergrad_candidacy
        SET
            approved="{}", datemodified=CURRENT
        WHERE
            undergradcandidacy_no = {}
    '''.format(request.POST['approved'], request.POST['id'])

    do_sql(updateCandidacySQL, key=DEBUG, earl=EARL)

    student_sql = '''
        SELECT
            student_id
        FROM
            cc_stg_undergrad_candidacy
        WHERE
            undergradcandidacy_no = {}
        '''.format(request.POST.get('id'))

    student_id = do_sql(
        student_sql, key=DEBUG, earl=EARL
    ).first()['student_id']

    if request.POST.get('approved') == 'Y':

        gradwalkExistsSQL = '''
            SELECT COUNT(*) AS entries
            FROM
                gradwalk_rec
            WHERE
                id = {}
        '''.format(student_id)
        record = do_sql(gradwalkExistsSQL, key=DEBUG, earl=EARL)
        record_exists = record.first()['entries']
        getCandidacyInfoSQL = '''
            SELECT
                *
            FROM
                cc_stg_undergrad_candidacy
            WHERE
                undergradcandidacy_no = {}
        '''.format(request.POST.get('id'))
        student = do_sql(getCandidacyInfoSQL, key=DEBUG, earl=EARL)
        student_data = student.first()

        # clean some data

        # If the aa type is DIPL, determine whether to insert or update
        # the address information
        if student_data['diploma_aa_type'] == 'DIPL':
            hasDiplAddressSQL = '''
                SELECT
                    aa_no
                FROM
                    aa_rec
                WHERE
                    id = {}
                AND
                    aa = 'DIPL'
                AND
                    TODAY BETWEEN aa_rec.beg_date
                AND
                    NVL(aa_rec.end_date, TODAY)
            '''.format(student_id)

            hasDiplAddress = do_sql(
                hasDiplAddressSQL, key=DEBUG, earl=EARL
            ).first()
            if hasDiplAddress:
                diplSQL = '''
                    UPDATE
                        aa_rec
                    SET
                        line1 = "{}",
                        city = "{}",
                        st = "{}",
                        zip = "{}",
                        beg_date = TODAY
                    WHERE
                        aa_no = {}
                '''.format(
                    student_data['address'],
                    student_data['city'],
                    student_data['state'],
                    student_data['zip'],
                    hasDiplAddress['aa_no']
                )
            else:
                diplSQL = '''
                    INSERT INTO aa_rec
                        (id, aa, beg_date, peren, line1, city, st, zip, ctry)
                    VALUES (
                        {}, 'DIPL', TODAY, 'N', '{}', '{}', '{}', '{}', 'USA'
                    )
                '''.format(
                    student_id, student_data['address'],
                    student_data['city'], student_data['state'],
                    student_data['zip']
                )
            do_sql(diplSQL, key=DEBUG, earl=EARL)

        if record_exists:
            updateGradWalkSQL = '''
                UPDATE
                    gradwalk_rec
                SET
                    grad_sess = "{grad_sess}",
                    grad_yr = "{grad_yr}",
                    name_on_diploma = (
                        CASE WHEN
                            "{middle_initial}" = "None"
                        THEN
                            "{first_name} {last_name}"
                        ELSE
                            "{first_name} {middle_initial} {last_name}"
                        END
                    ),
                    fname_pronounce = "{first_name_pronounce}",
                    mname_pronounce = "{middle_name_pronounce}",
                    lname_pronounce = "{last_name_pronounce}",
                    addr = "{diploma_aa_type}",
                    plan2walk = (
                        CASE
                             WHEN "{plan_to_walk}" = "t" THEN "Y"
                             WHEN "{plan_to_walk}" = "Y" THEN "Y"
                        ELSE
                            "N"
                        END
                    ),
                    major1 = (
                        CASE WHEN
                            "{major1}" = "None" THEN "" ELSE "{major1}"
                        END
                        ),
                    major2 = (
                        CASE WHEN
                            "{major2}" = "None" THEN "" ELSE "{major2}"
                        END
                    ),
                    major3 = (
                        CASE WHEN
                            "{major3}" = "None" THEN "" ELSE "{major3}"
                        END
                    ),
                    minor1 = (
                        CASE WHEN
                            "{minor1}" = "None" THEN "" ELSE "{minor1}"
                        END
                    ),
                    minor2 = (
                        CASE WHEN
                            "{minor2}" = "None" THEN "" ELSE "{minor2}"
                        END
                    ),
                    minor3 = (
                        CASE WHEN
                            "{minor3}" = "None" THEN "" ELSE "{minor3}"
                        END
                    )
                WHERE
                    id = {student_id}
            '''.format(**student_data)
            do_sql(updateGradWalkSQL, key=DEBUG, earl=EARL)
        else:
            insertGradWalkSQL = '''
              INSERT INTO gradwalk_rec (
                  id, prog, site, degree, grad_sess, grad_yr,
                  name_on_diploma, fname_pronounce, mname_pronounce,
                  lname_pronounce, addr, plan2walk, major1, major2,
                  major3, minor1, minor2, minor3
              )
              VALUES (
                {student_id}, "", "CART", "BA", "{grad_sess}",
                "{grad_yr}", (
                    CASE WHEN
                      "{middle_initial}" = "None"
                    THEN
                      "{first_name} {last_name}"
                    ELSE
                      "{first_name} {middle_initial} {last_name}"
                    END
                ),
                "{first_name_pronounce}", "{middle_name_pronounce}",
                "{last_name_pronounce}", "{diploma_aa_type}",
                (
                    CASE
                        WHEN "{plan_to_walk}" = "t" THEN "Y"
                        WHEN "{plan_to_walk}" = "Y" THEN "Y"
                    ELSE
                        "N"
                    END
                ),
                (CASE WHEN "{major1}" = "None" THEN "" ELSE "{major1}" END),
                (CASE WHEN "{major2}" = "None" THEN "" ELSE "{major2}" END),
                (CASE WHEN "{major3}" = "None" THEN "" ELSE "{major3}" END),
                (CASE WHEN "{minor1}" = "None" THEN "" ELSE "{minor1}" END),
                (CASE WHEN "{minor2}" = "None" THEN "" ELSE "{minor2}" END),
                (CASE WHEN "{minor3}" = "None" THEN "" ELSE "{minor3}" END)
              )
            '''.format(**student_data)
            do_sql(insertGradWalkSQL, key=DEBUG, earl=EARL)

        # send an email to the student
        if settings.DEBUG:
            to_list = [settings.SERVER_EMAIL]
        else:
            to_list = [get_email(student_id)]

        phile = '{}Degree_Audit_Instructions.pdf'.format(settings.MEDIA_ROOT)

        send_mail(
            request, to_list,
            "Congratulations: Graduation Candidacy Accepted",
            settings.REGISTRAR_EMAIL, 'undergradcandidacy/email_accepted.html',
            {'student':student_data,}, settings.MANAGERS, attach=phile
        )

    return HttpResponse('update successful')


def getPermAddress(cx_id):
    getPermAddressSQL = '''
      SELECT
        TRIM(addr_line1 || ' ' || addr_line2 || ' ' || addr_line3) AS address,
        TRIM(city) AS city, TRIM(st) AS st, TRIM(zip) AS zipcode
      FROM
        id_rec
      WHERE
        id = {}
    '''.format(cx_id)
    permAddress = do_sql(getPermAddressSQL, key=DEBUG, earl=EARL)

    return permAddress.first()
