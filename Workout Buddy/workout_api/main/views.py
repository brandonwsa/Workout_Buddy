from django.shortcuts import render

#home screen view
def home(request):
    return render(request, 'main/home.html')


#about page view
def about(request):
    return render(request, 'main/about.html')
