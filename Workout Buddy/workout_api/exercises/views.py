from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
#from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
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

    #defining our own get_queryset method allows us to set a custom basename when routing.
    #This helps us seperate the API view from accidently popping up when user clicks to view their
    #exercise from their profile in the UI.
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
Detailed list view of exercises.
Will give a detail view of the exercise the user wants to view.
"""
class ExercisesDetailView(UserPassesTestMixin, DetailView):
    model = Exercises

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise pk
    #which would create an 'No exercise found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise we are viewing, exercisepk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(Exercises, pk=self.kwargs.get('exercisepk'))

    # see if user trying to view execise details is user logged in.
    def test_func(self):
        #exercise = Exercises.objects.get(pk=self.kwargs['exercisepk'])
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        #workout = exercise.workout_id
        if self.request.user == workout.username:
            return True
        else:
            return False


"""

"""
"""
class ExerciseAPIDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    #return the wanted exercise
    def get(self, request, format=None):
        exercise = Exercises.objects.all()

        return Response(exercise)
"""
    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise pk
    #which would create an 'No exercise found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise we are viewing, exercisepk from url.
 #   def get_object(self, queryset=None):
 #       return get_object_or_404(Exercises, pk=self.kwargs.get('exercisepk'))

    # see if user trying to view execise details is user logged in.
 #   def test_func(self):
        #exercise = Exercises.objects.get(pk=self.kwargs['exercisepk'])
 #       workout = Workouts.objects.get(pk=self.kwargs['pk'])
        #workout = exercise.workout_id
  #      if self.request.user == workout.username:
  #          return True
  #      else:
  #          return False


"""
Exercises creation functionality.
Allows user to add new exercises to the workout they just created.
"""
class ExercisesCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = ExercisesForm
    template_name = 'exercises/exercises_form.html'
    success_message = 'Exercise added to workout!'

    #overrride method so we can add the workout_pk to the context data.
    #Allows user to be redirected to their workout-exercises view when clicking 'Done' through the use of workout_pk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        context["workout_pk"] = workout.pk
        return context

    #redirect user to add more exercise details to the workout when user creates an exercise
    def get_success_url(self):
        return reverse_lazy('exercisesdetails-create', kwargs={'pk': self.kwargs['pk'], 'exercisepk': self.object.id})

    #override form valid method and provide the workout primary key
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



"""
The update view with authorization check.
Allow user to update the exercise, date, and if they did sameWeight or not.
"""
class ExercisesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercises
    fields = ['exercise', 'date', 'sameWeight']

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise pk
    #which would create an 'No exercise found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise we are viewing, exercisepk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(Exercises, pk=self.kwargs.get('exercisepk'))

    #redirect user back to their exercise view for that workout
    def get_success_url(self):
        return reverse_lazy('exercises-detail', kwargs={'pk': self.kwargs['pk'], 'exercisepk': self.kwargs['exercisepk']})

    #override form valid method and provide the workout primary key
    def form_valid(self, form):
        #get the workout object that matches the pk in the page
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        #fill in workout_id field with workout object matching the pk in the form instance
        form.instance.workout_id = workout #self.kwargs['pk'], use this if we make workout_id field an integer and not an instance of workout object.

        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)


    # see if user trying to add exercise is user logged in.
    def test_func(self):
        exercise = self.get_object()
        workout = exercise.workout_id
        if self.request.user == workout.username:
            return True
        else:
            return False



"""
The delete view with authorization
"""
class ExercisesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exercises

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise pk
    #which would create an 'No exercise found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise we are viewing, exercisepk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(Exercises, pk=self.kwargs.get('exercisepk'))

    #redirect user back to their exercise view list for that workout
    def get_success_url(self):
        return reverse_lazy('workout-exercises', kwargs={'pk': self.kwargs['pk']})
    
    # see if user trying to add exercise is user logged in.
    def test_func(self):
        exercise = self.get_object()
        workout = exercise.workout_id
        if self.request.user == workout.username:
            return True
        else:
            return False