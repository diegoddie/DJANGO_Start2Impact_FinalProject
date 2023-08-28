from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib import messages
# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered, log in to continue.")
            return redirect('accounts:login')
    else:
        form = SignupForm()
        return render(request, 'sign_up.html', {'form':form})
    return render(request, 'sign_up.html', {'form':form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('home')