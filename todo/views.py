from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from .models import Todo
from .forms import TodoForm


@login_required
def index(request):
    tasks = Todo.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user  # 🔥 Assign the task to the logged-in user
            todo.save()
            return redirect('todo')
    else:
        form = TodoForm()
    return render(request, 'todo/index.html', {'forms': form, 'list': tasks, 'title': 'TODO LIST'})


@login_required
def edit(request, item_id):
    task = get_object_or_404(Todo, id=item_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('todo')
    else:
        form = TodoForm(instance=task)
    return render(request, 'todo/edit.html', {'form': form})


@login_required
def toggle_complete(request, item_id):
    task = get_object_or_404(Todo, id=item_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('todo')


@login_required
def remove(request, item_id):
    task = get_object_or_404(Todo, id=item_id, user=request.user)
    task.delete()
    messages.info(request, "Task removed!")
    return redirect('todo')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('todo')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('todo')
        else:
            print(form.errors)  # Debugging output
            messages.error(request, "Registration failed.")
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@staff_member_required
def dashboard(request):
    users = User.objects.all()
    todos_by_user = {user: Todo.objects.filter(user=user) for user in users}
    return render(request, 'todo/dashboard.html', {'todos_by_user': todos_by_user})
