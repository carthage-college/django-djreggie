from django.conf.urls import include, url

from djreggie.dashboard import views as dash_views
from djreggie.undergradcandidacy import views as ugc_views

urlpatterns = [
    url(
        r'^admin/$',
        dash_views.admin, name='admin'
    ),
    url(
        r'^admin/undergradcandidacy/student/(?P<student_id>[0-9]{5,7})/$',
        ugc_views.student, name='undergrad_student'
    ),
    url(
        r'^admin/search/$',
        ugc_views.search, name='dashboard_undergrad_search'
    ),
    url(
        r'^set_approved/$',
        dash_views.set_approved, name='ug_set_approved'
    ),
    url(
        r'^$', dash_views.index, name='index'
    )
]
