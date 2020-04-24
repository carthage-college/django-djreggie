# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView

from djreggie.survey import views


urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='survey/done.html'
        ),
        name='survey_success',
    ),
    url(r'^courses/$', views.courses, name='survey_courses_form'),
]
