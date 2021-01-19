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


    # see if user trying to view exercises details list is user logged in.
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

    # see if user trying to view exercise details detail is user logged in.
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

    #overrride method so we can add the workout_pk to the context data.
    #Doing this makes it so when user clicks 'Add another exercise', they are able to be redirected to create another exercise, which we need the workout pk for.
    #Also allows user to be redirected to their workout-exercises view when clicking 'Done' through the use of workout_pk
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise = Exercises.objects.get(pk=self.kwargs['exercisepk'])
        context["workout_pk"] = exercise.workout_id.pk
        return context

    #redirect user to add more exercises to the workout when user creates an exercise details
    def get_success_url(self):
        return reverse_lazy('exercisesdetails-create', kwargs={'pk': self.kwargs['pk'], 'exercisepk': self.kwargs['exercisepk']})

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


    # see if user trying to create exercise details is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False



"""
The update view with authorization check.
Allow user to update the exercise details, weight, set amount, and total reps.
"""
class ExercisesDetailsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExercisesDetails
    fields = ['weight', 'set_amount', 'total_reps']

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise details pk
    #which would create an 'No exercisedetails found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise details we are viewing, exercisedetailpk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(ExercisesDetails, pk=self.kwargs.get('exercisedetailpk'))

    #redirect user back to their exercise detail view for that workout
    def get_success_url(self):
        return reverse_lazy('exercisesdetails-detail', kwargs={'pk': self.kwargs['pk'], 'exercisepk': self.kwargs['exercisepk'], 'exercisedetailpk': self.kwargs['exercisedetailpk']})

    #override form valid method and provide the exercise primary key
    def form_valid(self, form):
        #get the exercise object that matches the pk in the page
        exercise = Exercises.objects.get(pk=self.kwargs['exercisepk'])
        #fill in exercise_id field with exercise object matching the exercisepk in the form instance
        form.instance.exercise_id = exercise #self.kwargs['exercisepk'], use this if we make exercise_id field an integer and not an instance of exercise object.

        #update the volume for the exercise details.
        #Takes (reps * sets) * weight. IE: (3*10)*100 = 3000 volume.
        form.instance.volume = (form.instance.total_reps * form.instance.set_amount) * form.instance.weight

        #update total volume to exercise, if the form is valid
        #subtracts off old exercise details volume from exercise totalvolume then add new exercise details volume
        if form.is_valid():
            # get exercise details currect object volume
            currentVolume = ExercisesDetails.objects.get(pk=self.kwargs['exercisedetailpk']).volume
            Exercises.objects.filter(pk=exercise.pk).update(totalVolume=(exercise.totalVolume - currentVolume) + form.instance.volume)

        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)


    # see if user trying to update exercise details is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False



"""
The delete view with authorization
"""
class ExercisesDetailsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ExercisesDetails

    #needed to override since this method default looks for pk_url_kwarg which was getting the workout pk instead of exercise details pk
    #which would create an 'No exercisedetails found matching the query' error.
    #We now supply a pk that is the correct pk of the exercise details we are viewing, exercisedetailpk from url.
    def get_object(self, queryset=None):
        return get_object_or_404(ExercisesDetails, pk=self.kwargs.get('exercisedetailpk'))


    #redirect user back to their exercises details view list for that exercise
    def get_success_url(self):
        return reverse_lazy('exercise-exercisesdetails', kwargs={'pk': self.kwargs['pk'], 'exercisepk': self.kwargs['exercisepk']})


    #override the delete method to remove the volume of the exercisedetails from the total volume for that exercise when deleted.
    def delete(self, request, *args, **kwargs):
        #try to get exercise and exercise details, if either fails, will continue to the deletion which will display page not found 404
        try: 
            #get the exercise object that matches the pk in the page
            exercise = Exercises.objects.get(pk=kwargs['exercisepk'])

            #remove the volume from total volume.
            currentVolume = ExercisesDetails.objects.get(pk=kwargs['exercisedetailpk']).volume
            Exercises.objects.filter(pk=exercise.pk).update(totalVolume=exercise.totalVolume - currentVolume)
        except:
            return super().delete(request, *args, **kwargs)

        #call original method to handle the actual deletion portion of the exercisedetails object.
        return super().delete(request, *args, **kwargs)


    # see if user trying to update exercise details is user logged in.
    def test_func(self):
        #gets username from workout associated with the exercise
        username = Exercises.objects.get(pk=self.kwargs['exercisepk']).workout_id.username
    #    workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == username:
            return True
        else:
            return False




#will have to subtrct volume off of exer.totalVolume when deleting an exercise detail.