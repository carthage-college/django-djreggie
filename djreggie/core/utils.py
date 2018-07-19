from django.conf import settings

from djzbar.utils.informix import do_sql


def get_email(cx_id):
    '''
    accepts: user ID
    returns: user's email
    '''

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

    obj = do_sql(
        email_sql, key=settings.INFORMIX_DEBUG, earl=settings.INFORMIX_EARL
    )

    try:
        email = obj.first()['email']
    except:
        email = None

    return email
