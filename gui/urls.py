from django.urls import path

from . import views

urlpatterns = [
    path('sgn', views.sgn, name='sgn'),
    path('dockerRun', views.dockerRun, name='dockerRun'),
    path('', views.index, name='index'),
]