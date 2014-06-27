#Need this
from django.conf.urls import patterns, include, url

#Where I put all the 'views' associated with this form
urlpatterns = patterns('djreggie.changemajor.views', #Look in my 'views.py' file too
    url(r'^$', 'create'), #If I have nothing else appended to my url, I go into my 'views.py' file and call the 'index' function
    
)
#test comment
