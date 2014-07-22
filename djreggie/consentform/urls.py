from django.conf.urls import patterns, include, url #Need this

#Where I put all the 'views' associated with this form
urlpatterns = patterns('djreggie.consentform.views', #Look in my 'views.py' file too
    url(r'^admin/$', 'admin', name="admin"),
    url(r'^admin/student/(?P<student_id>[0-9]{5,7})/$', 'student', name="student"),
    url(r'^admin/search/$', 'search', name="search"),
    url(r'^', 'create', name="create"), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'create' function
)    
