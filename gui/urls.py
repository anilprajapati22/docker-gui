from django.urls import path

from . import views

urlpatterns = [
    path('sgn', views.sgn, name='sgn'),
    path('', views.dockerRun, name='dockerRun'),
    path('<str:container_id>/', views.containerDetails, name='containerDetails'),
    path('<str:container_id>/containerRemove', views.containerRemove, name='containerRemove'),
    
    path('', views.index, name='index'),
]