from django.conf.urls import include, url

from djreggie.indepstudent import views

urlpatterns = [
    url(r'^$', views.create, name='create'),
]
