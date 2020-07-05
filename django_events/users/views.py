from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from .forms import CustomUserCreationForm


class RegisterView(FormView):

    def get(self, request):
        """
        Handles a GET request by rendering the register form
        """
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        """
        Handles a POST request from the register form. If form is valid the User is created, logged in and redirected
        to the events list. If the form is not valid then the form is re-rendered with error messages
        """
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(reverse('events_list'))
        return render(request, 'users/register.html', {'form': form})
