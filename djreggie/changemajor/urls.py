#Need this
from django.conf.urls import patterns, include, url

#Where I put all the 'views' associated with this form
urlpatterns = patterns('djreggie.changemajor.views',#Look in my 'views.py' file too
    url(r'^admin/?$', 'admin', name="admincm"),
    url(r'^admin/student/(?P<student_id>[0-9]{5,7})/?$', 'student', name="studentcm"),
    url(r'^admin/search/?$', 'search', name="searchcm"),
    url(r'^set_approved/$', 'set_approved', name='cm_set_approved'),    
    url(r'^$', 'create'), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
    
)
#test comment
