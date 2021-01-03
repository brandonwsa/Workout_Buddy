from django.shortcuts import render, redirect
from django.contrib import messages
#from rest_framework import viewsets
#from .serializers import UserSerializer
from .forms import ExercisesForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



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

    """
    #Check if entered information and grab it if so.
    if request.method == 'POST':
        form = ExercisesForm(request.POST)

        #see if form is valid entries
        if form.is_valid():
            #save exercise
            form.save()
            #get username
            username = form.cleaned_data.get('username')
            #display a success message that the exercise was created for the username
            messages.success(request, f'Exercises created for {username}!')
            #redirect user to given url.
            return redirect('login') #url name is name given in urlpatterns
                            #will be exercises detail url
       """     
#    else:
#        form = ExercisesForm()
    
 #   return render(request, 'exercises/exercises_form.html', {'form': form})