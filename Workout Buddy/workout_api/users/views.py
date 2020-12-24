from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    #Check if entered information and grab it if so.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        #see if form is valid entries
        if form.is_valid():
            #save user and hash password
            form.save()
            #get username
            username = form.cleaned_data.get('username')
            #display a success message that the account was created for the username
            messages.success(request, f'Account creted for {username}.')
            #redirect user to given url.
            return redirect('register') #url name is name given in urlpatterns
            
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})
