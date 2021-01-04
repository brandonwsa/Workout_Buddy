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