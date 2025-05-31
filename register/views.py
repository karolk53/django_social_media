from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered! Please log in.")
            return redirect("login")  # use your actual login URL name here
    else:
        form = RegisterForm()
    return render(request, "register/registration.html", {'form': form})
