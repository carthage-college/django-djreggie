from django.conf.urls import include, url

from djreggie.systemaccess import views

urlpatterns = [
    url(r'$', views.index, name='index'),
]
