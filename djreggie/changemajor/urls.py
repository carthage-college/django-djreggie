from django.conf.urls import include, url

from djreggie.changemajor import views

urlpatterns = [
    url(
        r'^admin/?$', views.admin, name='admincm'
    ),
    url(
        r'^admin/student/(?P<changemajor_no>[0-9]+)/?$',
        views.student, name='studentcm'),
    url(
        r'^admin/search/?$',
        views.search, name='searchcm'
    ),
    url(
        r'^set_approved/$',
        views.set_approved, name='cm_set_approved'
    ),
    url(r'^$', views.create)
]
