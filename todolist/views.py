from todolist.models import Tasklist
from django.shortcuts import render, redirect
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance = form.save()

        messages.success(request,"New Task was successfully added!")
        return redirect('todolist-home')    
    else:
        all_task = Tasklist.objects.filter(owner = request.user)
        paginator = Paginator(all_task, 5)
        page = request.GET.get('pg')
        all_task = paginator.get_page(page)

        return render(request, 'todolist.html' , {'all_task': all_task} )


@login_required
def delete(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
        return redirect('todolist-home')
    else:
       messages.error(request,("Access Restricted, You Are Not Allowed."))
       return redirect('todolist-home')

@login_required
def edit(request, task_id):
    if request.method == "POST":
        task = Tasklist.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        messages.success(request,"Task Edited!")
        return redirect('todolist-home')    
    else:
        task_obj = Tasklist.objects.get(pk=task_id) 
        return render(request, 'edit.html' , {'task_obj': task_obj})

@login_required
def complete(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
        return redirect('todolist-home')
    else:
        messages.error(request,("Access Restricted, You Are Not Allowed."))
        return redirect('todolist-home')

@login_required
def pending(request, task_id):
    task = Tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist-home')

def index(request):
    context = {
        'index_text':"Welcome to Home Page.",
    }    
    return render(request,'index.html',context)


def contact(request):
    context = {
        'contact_text':"Welcome to Contact Page.",
    }    
    return render(request,'contact.html',context)


def about(request):
    context = {
        'about_text':"Welcome to About Page.",
    }    
    return render(request,'about.html',context)
