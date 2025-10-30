from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timetable, Task, Resource
from .forms import TimetableForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'core/home.html')

@login_required
def dashboard_redirect(request):
    # This is a placeholder for role-based redirection.
    # You would implement logic here to check user roles and redirect accordingly.
    # For now, it redirects all logged-in users to the 'home' page.
    # Example:
    # if request.user.is_staff: # Assuming staff are admins/teachers
    #     return redirect('admin_dashboard')
    # else: # Assuming regular users are students
    #     return redirect('student_dashboard')
    return redirect('home')

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
    
    entries = Timetable.objects.filter(user=request.user).order_by('start_time')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = sorted(list(set((e.start_time, e.end_time) for e in entries)))
    
    timetable_data = []
    for start, end in time_slots:
        slot_str = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        subjects_for_slot = [''] * len(days)
        
        slot_entries = entries.filter(start_time=start, end_time=end)
        for entry in slot_entries:
            if entry.day in days:
                day_index = days.index(entry.day)
                subjects_for_slot[day_index] = entry.subject
        
        timetable_data.append({
            'time': slot_str,
            'subjects': subjects_for_slot
        })

    context = {
        'timetable_data': timetable_data,
        'form': form,
        'days': days
    }
    return render(request, 'core/timetable.html', context)

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