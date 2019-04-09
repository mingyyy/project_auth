from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .forms import SignInForm, UserForm, ProfileForm

from pprint import pprint
import json
import requests

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
    context = {'form': form}
    return render(request, 'register.html', context)


# def register(request):
#     '''Register a new user with api_key'''
#
#     if request.method != 'POST':
#         form = RegisterForm()
#     else:
#         form = RegisterForm(data=request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             messages.success(request, f'Account has created for {new_user.username}!')
#             authenticated_user = authenticate(username=new_user.username,
#                                               password=request.POST['password1'])
#             login(request, authenticated_user)
#             if len(new_user.api_key) != 42:
#                 messages.info(request, "API key is not correct.")
#             return HttpResponseRedirect(reverse('users:profile'))
#     return render(request, 'register.html', {'form':form})


# def register_one2one(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             new_user=user_form.save()
#             # profile = profile_form.save(commit=False)
#             # profile.user = request.user
#             profile.save()
#
#             messages.success(request, 'Your profile was successfully created!')
#             authenticated_user = authenticate(username=new_user.username,
#                                               password=new_user.password)
#             login(request, authenticated_user)
#             return redirect('users:profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm()
#         profile_form = ProfileForm()
#     return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def logout_view(request):
    logout(request)
    return render(request, "frontpage.html")


def frontpage(request):
    form = SignInForm(request.POST or None )
    if request.method == 'POST' and form.is_valid:
        username = request.POST['username'] # form.cleaned_data["username"] ???
        password = request.POST['password']
        sum = request.POST["summation"]
        if form.verification() != int(sum):
            print(sum, form.verification())
            messages.warning(request, "Are you a robot that can't count?")
            # redirect("frontpage")
        else:
            authenticated_user = authenticate(username=username,
                                          password=password)
            try:
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse("users:frontpage"))
            except AttributeError:
                messages.info(request, "Sorry, your username and password don't match.")
            except TypeError:
                messages.info(request, "Sorry, not working.Try again.")
    else:
        form = SignInForm()

    context = {"form": form}
    return render(request, 'frontpage.html', context)

@ login_required()
def profile(request):
    if len(request.user.profile.api_key) != 32:
        messages.warning(request, "Sorry, you don't have a valid API key. Please update your profile")
    else:
        sections = ['arts', 'automobiles', 'books', 'business', 'fashion', 'food', 'health', 'home',
                  'insider', 'magazine', 'movies', 'national', 'nyregion', 'obituaries', 'opinion',
                  'politics', 'realestate', 'science', 'sports', 'sundayreview', 'technology',
                  'theater', 'tmagazine', 'travel', 'upshot', 'world']
        ans="arts" # default session
        if request.method == 'POST':
            ans=request.POST.get("sections")
            messages.success(request, f"You have chosen {ans}. Here are the articles for you.")
        prof=Profile.objects.get(id=request.user.id)
        key=prof.api_key.strip()
        path = "https://api.nytimes.com/svc/topstories/v2/" + ans + ".json?api-key="+key
        download = requests.get(path).json()

        articles=[]
        for k, v in download.items():
            if k == "results":
                for l in v:
                    item = {}
                    for key, val in l.items():
                        if key in ["title", "abstract", "url"]:
                            item[key]=val
                    articles.append(item)

        context = {"sections": sections, "articles":articles}
    return render(request, "profile.html", context)


@login_required
@transaction.atomic
def update(request):
    if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                new_user=user_form.save()
                profile_form.save()
                messages.success(request, 'Your api key has been added!')
                return redirect('users:profile')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def about(request):
    profile=Profile.objects.all()

    return render(request, "about.html", {"profile": profile})



