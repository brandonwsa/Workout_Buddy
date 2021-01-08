from django.shortcuts import render
from django.views.generic import ListView
from exercises.models import Exercises
from workouts.models import Workouts
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#home screen view
def home(request):
    return render(request, 'main/home.html')


#about page view
def about(request):
    return render(request, 'main/about.html')


#contact page view
def contact(request):
    return render(request, 'main/contact.html')


"""
View to display exercises associated with workouts. Seperated from exercises app and workouts app to keep the two pps seperate form one another.
"""
class WorkoutExercisesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Exercises
    template_name = '/exercises/templates/exercises/exercises.html'
    context_object_name = 'exercises'

    #override queryset method from ListView to get signed in users exercises only
    def get_queryset(self):
        #get primary key from the workout from url
        workoutpk = self.kwargs['pk']
        #get the workout associated with that pk
        workout = Workouts.objects.get(pk=workoutpk)
        #get query that is the exercises that are from that workout, based on date and current user.
        # can probably just get the exercises based of of the workout PK if we make a fk in exercises table from workouts id. Wont need username info.
        queryset = Exercises.objects.filter(workout_id=workoutpk) #date=workout.date
        return queryset.order_by('-date') #order by newest date to oldest.


    # see if user trying to add exercise is user logged in.
    def test_func(self):
        workout = Workouts.objects.get(pk=self.kwargs['pk'])
        if self.request.user == workout.username:
            return True
        else:
            return False



    