from django.urls import path
from todolist import views

urlpatterns = [
    path('', views.todolist, name='todolist-home'),
    path('delete/<task_id>', views.delete, name='todolist-delete'),
    path('edit/<task_id>', views.edit, name='todolist-edit'),
    path('complete/<task_id>', views.complete, name='todolist-complete'),
    path('pending/<task_id>', views.pending, name='todolist-pending'),
]
