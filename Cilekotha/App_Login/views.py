from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from App_Login.models import Profile
from App_Login.forms import SignUpForm, ProfileForm

# Create your views here.
def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successfully.")
            return HttpResponseRedirect(reverse('App_Login:log_in'))
    
    return render(request, 'App_Login/sign_up.html', {'form':form})

def log_in(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Shop:home'))
                    
    return render(request, 'App_Login/log_in.html', {'form':form})

@login_required
def change_profile(request):
    user = Profile.objects.get(user=request.user)

    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Change saved!")
            return HttpResponseRedirect(reverse("App_Login:change_profile"))
    
    return render(request, 'App_Login/change_profile.html', {'form':form})

@login_required
def log_out(request):
    logout(request)
    messages.warning(request, "You are logged out!")
    return HttpResponseRedirect(reverse('App_Login:log_in'))