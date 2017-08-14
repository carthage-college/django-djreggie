from __future__ import unicode_literals

from django.db import models

class AaRec(models.Model):
    id_int = models.IntegerField(primary_key=True, db_column='id int') # Field renamed to remove unsuitable characters.
    aa_char = models.CharField(max_length=4L, db_column='aa char', blank=True) # Field renamed to remove unsuitable characters.
    beg_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    peren = models.CharField(max_length=1L, blank=True)
    line1 = models.CharField(max_length=64L, blank=True)
    line2 = models.CharField(max_length=64L, blank=True)
    line3 = models.CharField(max_length=64L, blank=True)
    city = models.CharField(max_length=50L, blank=True)
    st = models.CharField(max_length=2L, blank=True)
    zip = models.CharField(max_length=10L, blank=True)
    ctry = models.CharField(max_length=3L, blank=True)
    phone = models.CharField(max_length=12L, blank=True)
    phone_ext = models.CharField(max_length=4L, blank=True)
    ofc_add_by = models.CharField(max_length=4L, blank=True)
    cass_cert_date = models.DateField(null=True, blank=True)
    cell_carrier = models.CharField(max_length=4L, blank=True)
    opt_out = models.CharField(max_length=1L, blank=True)
    class Meta:
        db_table = 'aa_rec'

class FinprivRec(models.Model):
    priv_no = models.IntegerField(primary_key=True, unique=True)
    id = models.IntegerField(null=True, blank=True)
    code_name = models.CharField(max_length=64L, blank=True)
    code = models.CharField(max_length=4L, blank=True)
    comment = models.CharField(max_length=50L, blank=True)
    add_date = models.DateField(null=True, blank=True)
    fullname = models.CharField(max_length=64L, blank=True)
    class Meta:
        db_table = 'finpriv_rec'

class IdRec(models.Model):
    id = models.IntegerField(primary_key=True)
    prsp_no = models.IntegerField(null=True, blank=True)
    fullname = models.CharField(max_length=32L, blank=True)
    name_sndx = models.CharField(max_length=4L, blank=True)
    lastname = models.CharField(max_length=50L, blank=True)
    firstname = models.CharField(max_length=32L, blank=True)
    middlename = models.CharField(max_length=32L, blank=True)
    suffixname = models.CharField(max_length=10L, blank=True)
    addr_line1 = models.CharField(max_length=64L, blank=True)
    addr_line2 = models.CharField(max_length=64L, blank=True)
    addr_line3 = models.CharField(max_length=64L, blank=True)
    city = models.CharField(max_length=50L, blank=True)
    st = models.CharField(max_length=2L, blank=True)
    zip = models.CharField(max_length=10L, blank=True)
    ctry = models.CharField(max_length=3L, blank=True)
    aa = models.CharField(max_length=4L, blank=True)
    title = models.CharField(max_length=4L, blank=True)
    suffix = models.CharField(max_length=4L, blank=True)
    ss_no = models.CharField(max_length=11L, blank=True)
    phone = models.CharField(max_length=12L, blank=True)
    phone_ext = models.CharField(max_length=4L, blank=True)
    prev_name_id = models.IntegerField(null=True, blank=True)
    mail = models.CharField(max_length=1L, blank=True)
    sol = models.CharField(max_length=1L, blank=True)
    pub = models.CharField(max_length=1L, blank=True)
    correct_addr = models.CharField(max_length=1L, blank=True)
    decsd = models.CharField(max_length=1L, blank=True)
    add_date = models.DateField(null=True, blank=True)
    ofc_add_by = models.CharField(max_length=4L, blank=True)
    upd_date = models.DateField(null=True, blank=True)
    valid = models.CharField(max_length=1L, blank=True)
    purge_date = models.DateField(null=True, blank=True)
    cass_cert_date = models.DateField(null=True, blank=True)
    cc_username = models.CharField(max_length=250L, blank=True)
    cc_password = models.CharField(max_length=250L, blank=True)
    inquiry_no = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'id_rec'

class Majorminor(models.Model):
    id = models.IntegerField(primary_key=True)
    prog = models.CharField(max_length=4L, blank=True)
    subprog = models.CharField(max_length=4L, blank=True)
    major1 = models.CharField(max_length=4L, blank=True)
    major2 = models.CharField(max_length=4L, blank=True)
    major3 = models.CharField(max_length=4L, blank=True)
    minor1 = models.CharField(max_length=4L, blank=True)
    minor2 = models.CharField(max_length=4L, blank=True)
    minor3 = models.CharField(max_length=4L, blank=True)
    class Meta:
        db_table = 'majorminor'


