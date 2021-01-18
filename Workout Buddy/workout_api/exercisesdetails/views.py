from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
#from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from .serializers import ExercisesDetailsSerializer
from .forms import ExercisesDetailsForm
from .models import ExercisesDetails
from exercises.models import Exercises
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
Rest framework api for exercises_details. Will display exercise details in json using GET and provide a way to view the options for the objects.
"""
class ExercisesDetailsViewSet(viewsets.ModelViewSet):
   # queryset = ExercisesDetails.objects.all()
    serializer_class = ExercisesDetailsSerializer

    #defining our own get_queryset method allows us to set a custom basename when routing.
    #This helps us seperate the API view from accidently popping up when user clicks to view their
    #exercise details from their profile in the UI.
    def get_queryset(self):
        return ExercisesDetails.objects.all()


"""
View to display exercise details associated with the exercise.
"""
class ExercisesDetailsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ExercisesDetails
    template_name = 'exercisesdetails/exercisesdetails.html'
    context_object_name = 'exercisesdetails'

    #override queryset method from ListView to get signed in users exercises details only
    def get_queryset(self):
        #get primary key from the exercise from url
        exercisepk = self.kwargs['exercisepk']
        #get the exercise associated with that pk
        exercise = Exercises.objects.get(pk=exercisepk)
        #get query that is the exercises details that are from that exercise.
        queryset = ExercisesDetails.objects.filter(exercise_id=exercisepk)
        return queryset.order_by('-weight') #order by heaviest weight


     # see if user trying to add exercise is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False


"""
Detailed list view of exercises details.
Will give a detail view of the exercise details the user wants to view.
"""
class ExercisesDetailsDetailView(UserPassesTestMixin, DetailView):
    model = ExercisesDetails

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercisedetails pk
    #which would create an 'No exercise found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise details we are viewing, exercisedetailspk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(ExercisesDetails, pk=self.kwargs.get('exercisedetailpk'))

     # see if user trying to add exercise is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False


"""
Exercises_Details creation functionality.
Allows user to add new exercise etails to the exercise they just created.
"""
class ExercisesDetailsCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = ExercisesDetailsForm
    template_name = 'exercisesdetails/exercisesdetails_form.html'
    success_message = 'Exercise details added to exercise!'


    #redirect user to add more exercises to the workout when user creates an exercise details
    def get_success_url(self):
        return reverse_lazy('exercises-add', kwargs={'pk': self.kwargs['pk']})

    #override form valid method and provide the exercise primary key to fill in foreignkey field in the exercisesdetails model
    def form_valid(self, form):
        #get the exercise object that matches the pk in the page
        exercise = Exercises.objects.get(pk=self.kwargs['exercisepk'])
        #fill in exercise_id field with exercise object matching the pk in the form instance
        form.instance.exercise_id = exercise #self.kwargs['pk'], use this if we make workout_id field an integer and not an instance of workout object.

        #fill in the volume for the exercise details.
        #Takes (reps * sets) * weight. IE: (3*10)*100 = 3000 volume.
        form.instance.volume = (form.instance.total_reps * form.instance.set_amount) * form.instance.weight

        #add total volume to exercise, if the form is valid
        if form.is_valid():
            Exercises.objects.filter(pk=exercise.pk).update(totalVolume=exercise.totalVolume + form.instance.volume)

        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)


    # see if user trying to add exercise is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False



#will have to subtrct volume off of exer.totalVolume when deleting an exercise detail.