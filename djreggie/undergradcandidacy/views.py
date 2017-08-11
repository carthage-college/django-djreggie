from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from djzbar import settings
from djreggie import settings
from sqlalchemy import create_engine
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_exempt
from djreggie.undergradcandidacy.forms import UndergradForm
from djzbar.utils.mssql import get_userid
from djzbar.utils.informix import do_sql

import re


def index(request):
    valid_class = 'Y'
    year = date.today().year
    if date.today().month <= 5:
        year = year - 1
    perm = None
    if request.POST:
        form = UndergradForm(request.POST)

        perm = getPermAddress(int(request.POST['student_id']))
        if form.is_valid(): #If the form is valid
            form.save()
            #email on valid submit
            studentEmail = getEmailById(request.POST['student_id'])
            body = '''
                Thank you for submitting your Candidacy Form for
                potential graduation this school year. Your submission
                has been received and is pending acceptance.
                Please keep an eye on your Carthage email for
                further correspondence regarding your eligibility
                for graduation.
            ''',
            send_mail(
                "Candidacy Received and Pending Approval",
                body, 'Brigid Patterson <bpatterson@carthage.edu>',
                [studentEmail], fail_silently=False
            )

            #form = UndergradForm()
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
            if get_userid(request.GET['student_id']) == None:
                return render(
                    request, 'undergradcandidacy/no_access.html'
                )

            cxID = int(get_userid(request.GET['student_id']))
            """
            # student's id, name, and majors/minors
            getStudentSQL = '''
                SELECT
                    IDrec.id, TRIM(IDrec.firstname) AS firstname,
                    TRIM(IDrec.middlename) AS middlename,
                    TRIM(IDrec.lastname) AS lastname,
                    TRIM(major1.major) AS major1code,
                    TRIM(major2.major) AS major2code,
                    TRIM(major3.major) AS major3code,
                    TRIM(minor1.minor) AS minor1code,
                    TRIM(minor2.minor) AS minor2code,
                    TRIM(minor3.minor) AS minor3code
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
            '''.format(cxID)
            student = do_sql(
                getStudentSQL,
                key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            )

            for row in student: #set student's initial data
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
            """

            form = populateForm(cxID)

            """
            #check if student is a junior/senior or not
            getClassStandingSQL = '''
            SELECT
                CASE
                    prog_enr_rec.cl
                WHEN 'JR' THEN 'Y'
                WHEN 'SR' THEN 'Y'
                ELSE 'N'
                END AS valid_class
            FROM
                prog_enr_rec
            WHERE
                prog_enr_rec.id = {}
            '''.format(cxID)
            class_standing = do_sql(
                getClassStandingSQL,
                key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            )
            valid_class = class_standing.first()['valid_class']
            """
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
        'userid': request.GET['student_id'],
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

    student = do_sql(
        getStudentSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

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
    class_standing = do_sql(
        getClassStandingSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    return class_standing.first()['valid_class']

def submitted(request):
    return render(request, 'undergradcandidacy/form.html')

def contact(request):
    '''
    retriews student's contact info from form through ajax call
    '''

    getContactSQL = '''
        SELECT
            *
        FROM
            aa_rec
        WHERE
            id = {'id'}
        AND
            aa = "{'aa'}"
        AND
            TODAY BETWEEN beg_date AND NVL(end_date, TODAY)
    '''.format(request.GET)
    contactinfo = do_sql(
        getContactSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
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
    return do_sql(
        sql,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
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
        do_sql(
            deleteRowSQL,
            key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
        )
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
    student = do_sql(
        getMajorMinorSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    return render(request, 'undergradcandidacy/home.html', {
        'student': student,
        'full_student_list': get_all_students(),
    })


def student(request, student_id): #admin details page
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
            uc.student_id = {}
    '''.format(student_id)

    student = do_sql(
        getStudentSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

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
            uc.student_id = {}
    '''.format(student_id)

    reqmajors = do_sql(
        getMajorMinorSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    return render(request, 'undergradcandidacy/details.html', {
        'student': student.first(),
        'reqmajors': reqmajors.first(),
        'full_student_list': get_all_students(),
    })


def search(request):
    '''
    admin details page accessed through search bar
    '''
    return student(request, request.POST['cid'])


@csrf_exempt
def set_approved(request):
    '''
    set the approved column in database for entry
    '''

    updateCandidacySQL = '''
        UPDATE
            cc_stg_undergrad_candidacy
        SET
            approved="{'approved'}", datemodified=CURRENT
        WHERE
            undergradcandidacy_no = {'id'}
    '''.format(request.POST)

    do_sql(
        updateCandidacySQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    student_sql = '''
        SELECT
            student_id
        FROM
            cc_stg_undergrad_candidacy
        WHERE
            undergradcandidacy_no = {}
        '''.format(request.POST.get('id'))

    student_id = do_sql(
        student_sql,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    ).first()['student_id']

    if request.POST.get('approved') == "Y":
        studentEmail = getEmailById(student_id)
        headers = {
            'Reply-To':'bpatterson@carthage.edu',
            'From':'Brigid Patterson <bpatterson@carthage.edu>'
        }
        body = '''
            Congratulations!
            Your Candidacy Form for graduation has been accepted!\n\n
            Please be sure to keep an eye on your Carthage email,
            as this is where communications regarding your graduation
            requirements and graduating senior activities will be sent.
            You will need to check your Degree Audit
            (available on the Carthage Portal - my.carthage.edu)
            to ensure that you are on track for meeting all degree
            requirements. If you have any questions about your Degree Audit,
            please contact the Associate Registrar, Brigid Patterson.\n\n
            ** Note:  Acceptance of your Candidacy Form is based upon
            current information. If there are any changes,
            the Registrar's Office will need to be notified immediately
            and acceptance of the Candidacy Form may change.
        '''
        email = EmailMessage(
            "Congratulations - Graduation Candidacy Accepted", body,
            'Brigid Patterson <bpatterson@carthage.edu>',
             [studentEmail], [settings.SERVER_EMAIL], headers=headers
        )
        email.attach_file(
            "{}Degree_Audit_Instructions.pdf".format(settings.MEDIA_ROOT)
        )
        email.send()
        gradwalkExistsSQL = '''
            SELECT COUNT(*) AS entries
            FROM
                gradwalk_rec
            WHERE
                id = {}
        '''.format(student_id)
        record = do_sql(
            gradwalkExistsSQL,
            key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
        )
        record_exists = record.first()['entries']
        getCandidacyInfoSQL = '''
            SELECT
                *
            FROM
                cc_stg_undergrad_candidacy
            WHERE
                undergradcandidacy_no = {}
        '''.format(request.POST.get('id'))
        student = do_sql(
            getCandidacyInfoSQL,
            key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
        )
        student_data = student.first()

        # If the aa type is DIPL, determine whether to insert or update
        # the address information
        if student_data["diploma_aa_type"] == "DIPL":
            hasDiplAddressSQL = """
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
            """.format(student_id)

            hasDiplAddress = do_sql(
                hasDiplAddressSQL,
                key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            ).first()

            if hasDiplAddress:
                diplSQL = '''
                    UPDATE
                        aa_rec
                    SET
                        line1 = "{'address'}",
                        city = "{'city'}",
                        st = "{'state'}",
                        zip = "{'zip'}",
                        beg_date = TODAY
                    WHERE
                        aa_no = {}
                '''.format(student_data, hasDiplAddress["aa_no"])
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
            do_sql(
                diplSQL,
                key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            )

        if record_exists:
            updateGradWalkSQL = '''
                UPDATE
                    gradwalk_rec
                SET
                    grad_sess = "{'grad_sess'}",
                    grad_yr = "{'grad_yr'}",
                    name_on_diploma = (
                        CASE WHEN
                            "{'middle_initial'}" = "None"
                        THEN
                            "{'first_name'} {'last_name'}"
                        ELSE
                            "{'first_name'} {'middle_initial'} {'last_name'}"
                        END
                    ),
                    fname_pronounce = "{'first_name_pronounce'}",
                    mname_pronounce = "{'middle_name_pronounce'}",
                    lname_pronounce = "{'last_name_pronounce'}",
                    addr = "{'diploma_aa_type'}",
                    plan2walk = (
                        CASE WHEN
                            "{'plan_to_walk'}" = "t"
                        THEN
                            "Y"
                        ELSE
                            "N"
                        END
                    ),
                    major1 = (
                        CASE WHEN
                            "{'major1'}" = "None" THEN "" ELSE "{'major1'}"
                        END
                        ),
                    major2 = (
                        CASE WHEN
                            "{'major2'}" = "None" THEN "" ELSE "{'major2'}"
                        END
                    ),
                    major3 = (
                        CASE WHEN
                            "{'major3'}" = "None" THEN "" ELSE "{'major3'}"
                        END
                    ),
                    minor1 = (
                        CASE WHEN
                            "{'minor1'}" = "None" THEN "" ELSE "{'minor1'}"
                        END
                    ),
                    minor2 = (
                        CASE WHEN
                            "{'minor2'}" = "None" THEN "" ELSE "{'minor2'}"
                        END
                    ),
                    minor3 = (
                        CASE WHEN
                            "{'minor3'}" = "None" THEN "" ELSE "{'minor3'}"
                        END
                    )
                WHERE
                    id = {'student_id'}
            '''.format(student_data)
            do_sql(
                updateGradWalkSQL,
                key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
            )
        else:
            insertGradWalkSQL = '''
              INSERT INTO gradwalk_rec (
                  id, prog, site, degree, grad_sess, grad_yr,
                  name_on_diploma, fname_pronounce, mname_pronounce,
                  lname_pronounce, addr, plan2walk, major1, major2,
                  major3, minor1, minor2, minor3
              )
              VALUES (
                {'student_id'}, "", "CART", "BA", "'{grad_sess'}",
                "{'grad_yr'}", (
                    CASE WHEN
                      "'{middle_initial'}" = "None"
                    THEN
                      "{'first_name'} {'last_name'}"
                    ELSE
                      "{'first_name'} {'middle_initial'} {'last_name'}"
                    END
                ),
                "{'first_name_pronounce'}", "{'middle_name_pronounce'}",
                "{'last_name_pronounce'}", "{'diploma_aa_type'}",
                (CASE WHEN "{'plan_to_walk'}" = "t" THEN "Y" ELSE "N" END),
                (CASE WHEN "{'major1'}" = "None" THEN "" ELSE "{'major1'}" END),
                (CASE WHEN "{'major2'}" = "None" THEN "" ELSE "{'major2'}" END),
                (CASE WHEN "{'major3'}" = "None" THEN "" ELSE "{'major3'}" END),
                (CASE WHEN "{'minor1'}" = "None" THEN "" ELSE "{'minor1'}" END),
                (CASE WHEN "{'minor2'}" = "None" THEN "" ELSE "{'minor2'}" END),
                (CASE WHEN "{'minor3'}" = "None" THEN "" ELSE "{'minor3'}" END)
              )
            '''.format(student_data)
            do_sql(
                insertGradWalkSQL,
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
        email_sql,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    return email.first()['email']


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
    permAddress = do_sql(
        getPermAddressSQL,
        key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )
    return permAddress.first()
