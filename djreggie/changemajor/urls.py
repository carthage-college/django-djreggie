from django.conf.urls import patterns, include, url

urlpatterns = patterns('djreggie.changemajor.views',
    url(r'^admin/?$', 'admin', name="admincm"),
    url(r'^admin/student/(?P<changemajor_no>[0-9]+)/?$', 'student', name="studentcm"),
    url(r'^admin/search/?$', 'search', name="searchcm"),
    url(r'^set_approved/$', 'set_approved', name='cm_set_approved'),
    url(r'^$', 'create'),
)
