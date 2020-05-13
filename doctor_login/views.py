from django.shortcuts import render,redirect

from doctor_login.forms import UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required 
def special(request):
    return HttpResponse("You are logged in !")

def index(request):
	return render(request, 'index.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('survey_list'))



def register(request):
    if request.method == 'POST':
        import pdb

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponse('A new user has been successfully registered!')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form,'errors':form.errors})
    #return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('survey_list'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return render(request, 'login.html', {'errors':{'error':'Invalid Username or Password'}})
    else:
        return render(request, 'login.html', {})