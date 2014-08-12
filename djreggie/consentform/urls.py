from django.conf.urls import patterns, include, url #Need this

#Where I put all the 'views' associated with this form
urlpatterns = patterns('djreggie.consentform.views', #Look in my 'views.py' file too
    url(r'^admin/?$', 'admin', name="admincform"),
    url(r'^admin/student/(?P<student_id>[0-9]{5,7})/?$', 'student', name="studentcform"),
    url(r'^admin/search/?$', 'search', name="searchcform"),    
    url(r'^mobile/?$', 'mobile', name="mobileform"),
    url(r'^$', 'create', name="createcform"), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'create' function
)    
