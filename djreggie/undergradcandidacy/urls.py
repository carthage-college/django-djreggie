from django.conf.urls import patterns, include, url #Need this

#Where I put all the 'views' associated with this form
urlpatterns = patterns('djreggie.undergradcandidacy.views', #Look in my 'views.py' file too
    url(r'^contactinfo', 'contact', name='contact'),
    url(r'^admin/$', 'admin', name="undergrad_admin"),
    url(r'^admin/student/(?P<student_id>[0-9]{5,7})/$', 'student', name="undergrad_student"),
    url(r'^admin/search/$', 'search', name="undergrad_search"),
    url(r'^set_approved/$', 'set_approved', name='set_approved'),
    url(r'^$', 'index', name='index'), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
)
