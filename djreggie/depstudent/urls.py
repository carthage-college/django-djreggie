from django.conf.urls import patterns, include, url


urlpatterns = patterns('djreggie.depstudent.views',
    url(r'^$', 'create', name="create"),
)
