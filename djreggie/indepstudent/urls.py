from django.conf.urls import patterns, include, url

urlpatterns = patterns('djreggie.indepstudent.views',
    url(r'^$', 'create', name="create"),
)    
