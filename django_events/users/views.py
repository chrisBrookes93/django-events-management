from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def view_register(request):
    """
    View to register a user

    :param request: Request
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
