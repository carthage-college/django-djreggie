from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^systemaccess/', include('djreggie.systemaccess.urls')),
    url(r'^undergradcandidacy/', include('djreggie.undergradcandidacy.urls')),
    url(r'^changemajor/', include('djreggie.changemajor.urls')),
    url(r'^consentfam/', include('djreggie.consentfam.urls')),
    url(r'^consentform/', include('djreggie.consentform.urls')),
    url(r'^createemail/', include('djreggie.createemail.urls')),
    url(r'^depstudent/', include('djreggie.depstudent.urls')),
    url(r'^indepstudent/', include('djreggie.indepstudent.urls')),
    url(r'^$', RedirectView.as_view(url="/registrar/")),
]
