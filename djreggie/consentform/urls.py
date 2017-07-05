from django.conf.urls import include, url #Need this

from djreggie.consentform import views

urlpatterns = [
    url(
        r'^admin/?$', views.admin, name='admincform'
    ),
    url(
        r'^admin/student/(?P<student_id>[0-9]{5,7})/?$',
        views.student, name='studentcform'
    ),
    url(
        r'^admin/search/?$',
        views.search, name='searchcform'
    ),
    url(
        r'^mobile/?$',
        views.mobile, name='mobileform'
    ),
    url(
        r'^$', views.create, name='createcform'
    )
]
