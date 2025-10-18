from django.urls import path, include
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.home, name='home'),
    path('timetable/', views.timetable, name='timetable'),
    path('tasks/', views.tasks, name='tasks'),
    path('resources/', views.resources, name='resources'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
]