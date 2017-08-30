from django.conf.urls import include, url
from django.views.generic import TemplateView

from djreggie.changemajor import views


urlpatterns = [
    url(
        r'^admin/?$', views.admin, name='admincm'
    ),
    url(
        r'^admin/student/(?P<changemajor_no>[0-9]+)/?$',
        views.student, name='studentcm'),
    url(
        r'^admin/search/?$',
        views.search, name='searchcm'
    ),
    url(
        r'^set_approved/$',
        views.set_approved, name='cm_set_approved'
    ),
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='changemajor/done.html'
        ),
        name='change_major_success'
    ),
    url(
        r'^$', views.create, name='change_major_form'
    )
]
