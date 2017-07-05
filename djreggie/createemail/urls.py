from django.conf.urls import include, url

from djreggie.createemail import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
