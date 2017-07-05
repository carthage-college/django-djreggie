from django.conf.urls import include, url

from djreggie.undergradcandidacy import views

urlpatterns = [
    url(
        r'^contactinfo',
        views.contact, name='contact'
    ),
    url(
        r'^admin/$',
        views.admin, name='undergrad_admin'
    ),
    url(
        r'^admin/student/(?P<student_id>[0-9]{5,7})/$',
        views.student, name='undergrad_student'

    ),
    url(
        r'^admin/search/$',
        views.search, name='undergrad_search'
    ),
    url(
        r'^set_approved/$',
        views.set_approved, name='ug_set_approved'
    ),
    url(
        r'^$',
        views.index, name='index'
    )
]
