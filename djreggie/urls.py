from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from djauth.views import loggedout

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^systemaccess/', include('djreggie.systemaccess.urls')),
    url(r'^undergradcandidacy/', include('djreggie.undergradcandidacy.urls')),
    url(r'^changemajor/', include('djreggie.changemajor.urls')),
    url(r'^consentfam/', include('djreggie.consentfam.urls')),
    url(r'^consentform/', include('djreggie.consentform.urls')),
    #url(r'^createemail/', include('djreggie.createemail.urls')),
    url(r'^depstudent/', include('djreggie.depstudent.urls')),
    url(r'^indepstudent/', include('djreggie.indepstudent.urls')),
    # survey
    url(r'^survey/', include('djreggie.survey.urls')),
    # auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout/$', loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(r'^accounts/$', RedirectView.as_view(url=reverse_lazy('auth_login'))),
    url(
        r'^denied/$',
        TemplateView.as_view(
            template_name='denied.html'
        ),
        name='access_denied',
    ),
    # everything goes to registrar page
    url(r'^$', RedirectView.as_view(url=reverse_lazy('undergrad_admin'))),
]
