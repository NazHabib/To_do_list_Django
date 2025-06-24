from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Todo
from .forms import TodoForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def todo_list(request):
    search_query = request.GET.get('search', '')
    filter_status = request.GET.get('status', 'all')
    filter_priority = request.GET.get('priority', 'all')
    
    todos = Todo.objects.filter(user=request.user)
    
    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if filter_status == 'completed':
        todos = todos.filter(completed=True)
    elif filter_status == 'pending':
        todos = todos.filter(completed=False)
    
    if filter_priority != 'all':
        todos = todos.filter(priority=filter_priority)
    
    context = {
        'todos': todos,
        'search_query': search_query,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
    }
    return render(request, 'todo/todo_list.html', context)

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task added successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/add_todo.html', {'form': form})

@login_required
def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/edit_todo.html', {'form': form, 'todo': todo})

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted successfully!')
    return redirect('todo_list')

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    status = 'completed' if todo.completed else 'pending'
    messages.success(request, f'Task marked as {status}!')
    return redirect('todo_list')
