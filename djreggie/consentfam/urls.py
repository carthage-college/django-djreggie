from django.conf.urls import patterns, include, url

#This is where you put all the 'views' associated with this form
urlpatterns = patterns('djreggie.consentfam.views', #Look in my 'views.py' file too
    url(r'^$', 'admin', name="admin"),
    url(r'^$', 'create', name="create"), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
)    
