"""workout_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User #for restapi framework
from rest_framework import routers, serializers, viewsets #for restapi framework
from users import views as user_views
from main import views as main_views
from workouts import views as workouts_views
from workouts.views import (
    WorkoutsListView,
    WorkoutsDetailView, 
    WorkoutsCreateView,
    WorkoutsUpdateView,
    WorkoutsDeleteView
)
from exercises import views as exercises_views
from exercises.views import (
    ExercisesDetailView,
    ExercisesCreateView,
    ExercisesUpdateView,
    ExercisesDeleteView
)


# router for the rest api to be displayed.
router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet)
router.register(r'workouts_api', workouts_views.WorkoutsViewSet, basename='workouts_api') #having basename='workouts_api' instead of 'workouts' allows user to not be redirected to api page
                                                                                          #when clicking on their workout they want to view. This seperates the API view (which user shouldnt have access to) 
                                                                                          #from UI view.
router.register(r'exercises_api', exercises_views.ExercisesViewSet, basename='exercises_api')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    #path('home/', main_views.home, name='home'),
    path('', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
    path('workouts/', WorkoutsListView.as_view(), name='workouts'),
    path('workouts/<int:pk>/', WorkoutsDetailView.as_view(), name='workouts-detail'), #should auto route to workouts_details.html
    path('workouts/new/', WorkoutsCreateView.as_view(), name='workouts-create'), #workouts_form.html is naming convention
    path('workouts/<int:pk>/update/', WorkoutsUpdateView.as_view(), name='workouts-update'), #auto routes to workouts_form
    path('workouts/<int:pk>/delete/', WorkoutsDeleteView.as_view(), name='workouts-delete'),
    path('workouts/<int:pk>/exercises/', main_views.WorkoutExercisesListView.as_view(), name='workout-exercises'), #use view from exercises.
#    path('exercises/new/', ExercisesCreateView.as_view(), name='exercises-create'), #exercises_form.html is naming convention
    path('workouts/<int:pk>/exercises/new/', ExercisesCreateView.as_view(), name='exercises-add'), #exercises_form.html is naming convention
    path('workouts/<int:pk>/exercises/<int:exercisepk>/', ExercisesDetailView.as_view(), name='exercises-detail'), #exercises_details.html is naming convention
    path('workouts/<int:pk>/exercises/<int:exercisepk>/update/', ExercisesUpdateView.as_view(), name='exercises-update'), #exercises_form.html is naming convention
    path('workouts/<int:pk>/exercises/<int:exercisepk>/delete/', ExercisesDeleteView.as_view(), name='exercises-delete'), #exercises_confirm_delete.html is naming convention
    path('api/', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

