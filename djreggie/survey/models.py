# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class OnlineCourse(models.Model):
    """Data model for the online courses survey."""

    # dates
    created_on = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_on = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # owners
    created_by = models.ForeignKey(
        User, verbose_name="Applicant",
        related_name='prehealth_committee_letter_applicant_created_by'
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name='prehealth_committee_letter_applicant_updated_by'
    )
    # core
    course1 = models.CharField(max_length=128, null=True, blank=True)
    course2 = models.CharField(max_length=128, null=True, blank=True)
    course3 = models.CharField(max_length=128, null=True, blank=True)
    course4 = models.CharField(max_length=128, null=True, blank=True)
    course5 = models.CharField(max_length=128, null=True, blank=True)
    course6 = models.CharField(max_length=128, null=True, blank=True)
    course7 = models.CharField(max_length=128, null=True, blank=True)
    course8 = models.CharField(max_length=128, null=True, blank=True)

    def first_name(self):
        return self.created_by.first_name

    def last_name(self):
        return self.created_by.last_name

    def email(self):
        return self.created_by.email

    def __unicode__(self):
        return u'{0}, {0}'.format(
            self.created_by.last_name, self.created_by.first_name,
        )
