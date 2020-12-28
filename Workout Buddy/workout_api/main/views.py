from django.shortcuts import render
from workouts.models import Workouts
from workouts.views import workouts as workouts_view

#home screen view
def home(request):

    # utilize workouts app api to display workouts on home.html
    return workouts_view(request, 'main/home.html')

"""
    content = {
        'workouts' : Workouts.objects.all()
    }

    return render(request, 'main/home.html', content) """
  #  return render(request, 'main/home.html')


#about page view
def about(request):
    return render(request, 'main/about.html')


#used to get workouts info for view
#def workouts(request):
    