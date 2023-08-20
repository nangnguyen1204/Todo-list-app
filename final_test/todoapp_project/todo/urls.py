from django.urls import path, include
from . import views
from .views import (
    home, 
    TaskList, 
    TaskDetail, 
    TaskCreate,
    TaskUpdate,
    TaskDelete,

    TaskListApiView,
    TaskDetailApiView,
    )

urlpatterns = [
    path('', views.home, name= 'home'),
    path('tasks/', TaskList.as_view(template_name = 'task_list.html'), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(template_name = 'task_detail.html'), name= 'task'),
    path('task/create/', TaskCreate.as_view(template_name = 'task_form.html'), name= 'task-create'),
    path('task/update/<int:pk>/', TaskUpdate.as_view(template_name = 'task_form.html'), name= 'task-update'),
    path('task/delete/<int:pk>', TaskDelete.as_view(template_name = 'task_confirm_delete.html'), name= 'task-delete'),

    path('api/',TaskListApiView.as_view()),
    path('api/<int:task_id>', TaskDetailApiView.as_view()),

]