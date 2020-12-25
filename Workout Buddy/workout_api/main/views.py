from django.shortcuts import render
from workouts.models import Workouts

#home screen view
def home(request):
    content = {
        'workouts' : Workouts.objects.all()
    }

    return render(request, 'main/home.html', content)
  #  return render(request, 'main/home.html')


#about page view
def about(request):
    return render(request, 'main/about.html')


#used to get workouts info for view
#def workouts(request):
    