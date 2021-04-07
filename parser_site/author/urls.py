from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:author_id>/publications/', views.publications, name='publications')
]
