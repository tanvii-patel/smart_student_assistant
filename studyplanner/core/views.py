from django.shortcuts import render
from .models import Timetable, Task, Resource

def home(request):
    return render(request, 'core/home.html')

def timetable(request):
    data = Timetable.objects.all()
    return render(request, 'core/timetable.html', {'data': data})

def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'core/tasks.html', {'tasks': tasks})

def resources(request):
    res = Resource.objects.all()
    return render(request, 'core/resources.html', {'res': res})

def task_list(request):
    tasks = Task.objects.all()  # fetch all tasks
    return render(request, 'tasks.html', {'tasks': tasks})
