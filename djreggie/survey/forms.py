# -*- coding: utf-8 -*-

from django import forms

from djreggie.survey.models import OnlineCourse


class OnlineCourseForm(forms.ModelForm):
    """Courses that the student might be of interest for online learning."""

    class Meta:
        """Attributes about the form class."""

        model = OnlineCourse
        exclude = (
            'created_by', 'created_on', 'updated_by', 'updated_on',
        )
