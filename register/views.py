from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm


def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Successfully registered! ")
            redirect("home_page")
    else:
        form = RegisterForm()
    return render(request,"register/registration.html",{'form':form})
