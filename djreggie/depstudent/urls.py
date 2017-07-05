from django.conf.urls import include, url


from djreggie.depstudent import views

urlpatterns = [
    url(r'^$', views.create, name='create'),
]
