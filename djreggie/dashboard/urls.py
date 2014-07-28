from django.conf.urls import patterns, include, url #Need this
from djreggie.undergradcandidacy import views as uc_views
from djreggie.dashboard import views
#Where I put all the 'views' associated with this form
urlpatterns = [ #Look in my 'views.py' file too
    url(r'^admin/$', 'views.admin', name="admin"),
    url(r'^admin/undergradcandidacy/student/(?P<student_id>[0-9]{5,7})/$', 'djreggie.undergradcandidacy.views.student', name="undergrad_student"),
    url(r'^admin/search/$', 'djreggie.undergradcandidacy.views.search', name="undergrad_search"),
    url(r'^set_approved/$', 'set_approved', name='ug_set_approved'),
    url(r'^$', 'index', name='index'), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
]
