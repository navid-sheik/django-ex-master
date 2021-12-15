from django.shortcuts import render
from django.http import HttpResponse, request
from .forms import HobbiesMultiForm, ProfileForm, ProfilePicForm, UpdateUserEmailForm, UserRegisterForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from mainapp import forms
# Create your views here.


@login_required(login_url='/login/')
def profile(request):
    # user =  request.user
    # profile =  user.get_profile()
    form =  HobbiesMultiForm()
    emailForm  =  UpdateUserEmailForm(instance=request.user)
    profile_form =  ProfilePicForm(instance=request.user.profile)
    
    return render(request, 'mainapp/pages/profile.html' , {'form':  form, 'email_form' :  emailForm, 'profile_form' :  profile_form})

@login_required(login_url='/login/')
def friends(request):
    return render(request, 'mainapp/pages/friends.html' )

@login_required(login_url='/login/')    
def friends_requests(request):
    current_user   = request.user

    requests  =  current_user.request_received.all()
    

    return render(request, 'mainapp/pages/friends_requests.html', {"requests" :  requests} )
  


def register_auth(request):
    form   =  UserRegisterForm()
    profile_form  =  ProfileForm()
    if request.method  == 'POST':
        form =  UserRegisterForm(request.POST)
        profile_form =  ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
     
            user =  form.save()
            profile =  profile_form.save(commit=False)
            profile.user =  user
            profile.save()

            username  =  form.cleaned_data.get('username')
            email =  form.cleaned_data.get('email')
            login(request, user)
            messages.success(request, f'Registration comple!')
            return redirect('mainapp:profile')
           
    
    return render(request, 'mainapp/auth/signup.html', {'form' :  form, 'p_form' :  profile_form})


def logout_auth(request):
    logout(request)
    messages.info(request, "You are now logged out from  the system ")
    return redirect('mainapp:login')


def login_auth(request):

    if request.method  ==  "POST" : 
        login_form =  AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username   = login_form.cleaned_data.get('username')
            password   = login_form.cleaned_data.get('password')
            user =  authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("mainapp:profile")
                else:
                  messages.error(request, 'User Inactive')
                  return render(request, 'mainapp/auth/login.html')

            else:
                messages.error(request, "Invalid username or password")
        else :
            messages.error(request, "invalid username and password ")
    login_form  =  AuthenticationForm()

    return render(request  ,'mainapp/auth/login.html', {'form' :  login_form} )
    # if request.method  == 'POST':
    #     form =  AuthenticationForm (request, data =  request.POST)

