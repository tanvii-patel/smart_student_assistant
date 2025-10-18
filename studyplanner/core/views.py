from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timetable, Task, Resource
from .forms import TimetableForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def home(request):
    return render(request, 'core/home.html')

@login_required
def timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            timetable = form.save(commit=False)
            timetable.user = request.user
            timetable.save()
            return redirect('timetable')
    else:
        form = TimetableForm()
    
    data = Timetable.objects.filter(user=request.user)
    return render(request, 'core/timetable.html', {'data': data, 'form': form})

@login_required
def tasks(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        Task.objects.create(user=request.user, title=title, description=description, deadline=deadline)
        return redirect('tasks')
    
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'core/tasks.html', {'tasks': tasks})

@login_required
def resources(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        Resource.objects.create(user=request.user, title=title, file=file)
        return redirect('resources')

    res = Resource.objects.filter(user=request.user)
    return render(request, 'core/resources.html', {'res': res})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'