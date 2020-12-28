from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Workouts
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

"""
Takes a request and URL to the page you want to show the workouts on.
Method overloading, can supply a custom URL you want the workouts to be displayed on
Or have it be the default view of displaying workouts in the workouts.html in workouts app.
Usually this is done by calling from your controller class views.py, in this case, main.views calls this w/ custom url
"""
def workouts(request, url=None):
    #query to get only the current users workouts
    querySet = Workouts.objects.filter(
        username = request.user
    )

    context = {
        'workouts' : querySet
    }

    #checks to see if url was provided.
    if url is not None:
        return render(request, url, context)
    else:
        return render(request, 'workouts/workouts.html', context)


"""
List view class to display workouts as a list organized based on date.
"""
class WorkoutsListView(ListView):
    template_name = 'workouts/workouts.html'
    context_object_name = 'workouts'

    #override queryset method from ListView to get signed in users workouts only
    def get_queryset(self):
        queryset = Workouts.objects.filter(username=self.request.user)
        return queryset.order_by('-date') #order by newest date to oldest.


"""
Detailed list view of workouts
"""
class WorkoutsDetailView(UserPassesTestMixin, DetailView):
    model = Workouts

    # see if user trying to view workout details is user logged in.
    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.username:
            return True
        else:
            return False


"""
The create workout view with authorization check
"""
class WorkoutsCreateView(LoginRequiredMixin, CreateView):
    model = Workouts
    fields = ['WName']
    success_url = '/home/' # redirect back to home page

    #override form valid method and provide username
    def form_valid(self, form):
        form.instance.username = self.request.user
        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)



"""
The update view with authorization check
"""
class WorkoutsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workouts
    fields = ['WName']
    success_url = '/home/' # redirect back to home page

    #override form valid method and provide username
    def form_valid(self, form):
        form.instance.username = self.request.user
        #see if form is valid, have to do again since overriding.
        return super().form_valid(form)


    # see if user trying to update workout is user logged in.
    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.username:
            return True
        else:
            return False



"""
The delete view with authorization
"""
class WorkoutsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workouts
    success_url = '/workouts/'
    
    # see if user trying to delete workout is user logged in.
    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.username:
            return True
        else:
            return False

