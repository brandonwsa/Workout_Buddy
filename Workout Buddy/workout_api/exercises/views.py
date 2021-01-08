from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
#from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from .serializers import ExercisesSerializer
from .forms import ExercisesForm
from .models import Exercises
from workouts.models import Workouts
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
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
CURRENTLY NOT USED ANYWHERE
"""
"""
class ExercisesListView(ListView):
    template_name = 'exercises/exercises.html'
    context_object_name = 'exercises'

    #override queryset method from ListView to get signed in users exercises only
    def get_queryset(self):
        queryset = Exercises.objects.filter(username=self.request.user)
        return queryset.order_by('-date') #order by newest date to oldest.
"""

"""
Exercises creation functionality.
Allows user to add new exercises to the workout they just created.
"""
class ExercisesCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = ExercisesForm
    template_name = 'exercises/exercises_form.html'
    success_message = 'Exercise added to workout!'


    #redirect user to add more exercises to the workout when user creates an exercise
    def get_success_url(self):
        return reverse_lazy('exercises-add', kwargs={'pk': self.kwargs['pk']})

    #override form valid method and provide username
    def form_valid(self, form):
        #get the workout object that matches the pk in the page
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        #fill in workout_id field with workout object matching the pk in the form instance
        form.instance.workout_id = workout #self.kwargs['pk'], use this if we make workout_id field an integer and not an instance of workout object.
        #fill in date field with the workout object matching the pk in the form instance
        form.instance.date = workout.date
        #see if form is valid, have to do again since overriding.

        return super().form_valid(form)


    # see if user trying to add exercise is user logged in.
    def test_func(self):
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == workout.username:
            return True
        else:
            return False


