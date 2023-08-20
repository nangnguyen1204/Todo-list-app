from typing import Any, Dict
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import TaskSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html')



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains = search_input)
            
        context['search_input'] = search_input

        return context



class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


    def get_queryset(self):
        base_qs = super(TaskDetail, self).get_queryset()
        return base_qs.filter(user = self.request.user)



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        return super(TaskCreate, self).form_valid(form)
    



class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        messages.success(self.request, "The task was updated successfully.")
        return super(TaskUpdate, self).form_valid(form)
    

    def get_queryset(self):
        base_qs = super(TaskUpdate, self).get_queryset()
        return base_qs.filter(user = self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(TaskDelete, self).form_valid(form)
    

    def get_queryset(self):
        base_qs = super(TaskDelete, self).get_queryset()
        return base_qs.filter(user = self.request.user)
    

# API Views
class TaskListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # list all
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user = request.user.id)
        serializer = TaskSerializer(tasks, many = True)

        return Response(serializer.data, status= status.HTTP_200_OK)
    

    # Create
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'completed' : request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TaskSerializer(data = data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self, task_id, user_id):

        try: 

            return Task.objects.get(id = task_id, user = user_id)
        except Task.DoesNotExist:

            return None
        
    # retrive
    def get(self, request, task_id, *args, **kwargs):
        
        task_instance = self.get_object(task_id, request.user.id )
        if not task_instance:
            return Response(
                {"res" : "object with task id does not exists"},
                status= status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TaskSerializer(task_instance)

        return Response(serializer.data, status= status.HTTP_200_OK)
    


    # update
    def put(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, request.user.id )

        if not task_instance:
            return Response(
                {"res" : "object with task id does not exists"},
                status= status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title' : request.data.get('title'),
            'description': request.data.get('description'),
            'completed' : request.data.get('completed'),
            'user' : request.user.id
        }
        serializer = TaskSerializer(instance= task_instance, data= data, partial = True )
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    # delete
    def delete(self, request, task_id, *args, **kwargs):
        task_instance = self.get_object(task_id, request.user.id )

        if not task_instance:
            return Response(
                {"res" : "object with task id does not exists"},
                status= status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response(
            {"res" : "Object deleted "},
            status= status.HTTP_200_OK
        )
