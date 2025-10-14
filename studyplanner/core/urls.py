from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('timetable/', views.timetable, name='timetable'),
    path('tasks/', views.tasks, name='tasks'),
    path('resources/', views.resources, name='resources'),
]
