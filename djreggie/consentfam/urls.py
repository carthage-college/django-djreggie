from django.conf.urls import patterns, include, url

#This is where you put all the 'views' associated with this form
urlpatterns = patterns('djreggie.consentfam.views', #Look in my 'views.py' file too
    url(r'^admin/?$', 'admin', name="admincf"),
    url(r'^admin/student/(?P<student_id>[0-9]{5,7})/?$', 'student', name="studentcf"),
    url(r'^admin/search/?$', 'search', name="searchcf"),
    url(r'^advisorsearch/$', 'advisor_search', name='advisorsearch'),
    url(r'^msearch/$', 'msearch', name='msearch'),
    url(r'^mresults/$', 'advisor_results', name='mresults'),
    url(r'^set_approved/$', 'set_approved', name='cf_set_approved'),
    url(r'^family_set_approved/$', 'family_set_approved', name='cf_family_set_approved'),
    url(r'^$', 'create', name="create"), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
)    
