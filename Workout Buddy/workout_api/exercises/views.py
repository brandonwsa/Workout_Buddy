from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .serializers import ExercisesSerializer
from .forms import ExercisesForm
from .models import Exercises
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)




"""
Rest framework api for exercises. Will display exercises in json using GET and provide a way to view the options for the objects.
"""
class ExercisesViewSet(viewsets.ModelViewSet):
   # queryset = Exercises.objects.all()
    serializer_class = ExercisesSerializer

    #defining out own get_queryset method allows us to set a custom basename when routing.
    #This helps us seperate the API view from accidently popping up when user clicks to view their
    #workout from their profile in the UI.
    def get_queryset(self):
        return Exercises.objects.all()



"""
List view class to display exercises as a list organized based on date for a specific workout.
"""
class ExercisesListView(ListView):
    template_name = 'exercises/exercises.html'
    context_object_name = 'exercises'

    #override queryset method from ListView to get signed in users exercises only
    def get_queryset(self):
        queryset = Exercises.objects.filter(username=self.request.user)
        return queryset.order_by('-date') #order by newest date to oldest.


"""
Exercises creation functionality
"""
class ExercisesCreateView(LoginRequiredMixin, CreateView):
    form_class = ExercisesForm
    template_name = 'exercises/exercises_form.html'
    success_url = '/exercises/new'


    #override form valid method and provide username
    def form_valid(self, form):
        form.instance.username = self.request.user
        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)


