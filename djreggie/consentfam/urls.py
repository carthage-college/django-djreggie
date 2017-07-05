from django.conf.urls import include, url

from djreggie.consentfam import views

urlpatterns = [
    url(
        r'^admin/?$',
        views.admin, name='admincf'
    ),
    url(
        r'^admin/student/(?P<student_id>[0-9]{5,7})/?$',
        views.student, name='studentcf'
    ),
    url(
        r'^admin/search/$',
        views.search, name='searchcf'
    ),
    url(
        r'^advisorsearch/$',
        views.advisor_search, name='advisorsearch'
    ),
    url(
        r'^set_approved/$',
        views.set_approved, name='cf_set_approved'
    ),
    url(
        r'^family_set_approved/$',
        views.family_set_approved, name='cf_family_set_approved'
    ),
    url(
        r'^$', views.create, name='create'
    )
]
