from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
    '''Register a new user.'''
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('users:frontpage'))
    context = {'form':form}
    return render(request, 'register.html', context)


def profile(request):
    return render(request, "profile.html")


def frontpage(request):
    return render(request, "frontpage.html")


def about(request):
    return render(request, "about.html")


def logout_view(request):
    '''log the user out.'''
    logout(request)
    return HttpResponseRedirect(reverse('logs:index'))