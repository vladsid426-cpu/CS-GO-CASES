from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages

def home(request):
    return render(request, "home.html")

# def login_view(request):
#     form = AuthenticationForm(request, data=request.POST or None)

#     if request.method == 'POST' and form.is_valid():
#         user = authenticate(
#             username=form.cleaned_data.get('username'),
#             password=form.cleaned_data.get('password'),
#         )

#         if user is not None:
#             login(request, user)
#             next_url = request.POST.get('next') or request.GET.get('next') or '/'
#             return redirect(next_url)

#     return render(request, 'login.html', {'form': form})



def register_view(request):
    success_url = reverse_lazy('home')
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(
            request,
            'Registration successful!'
        )

        return redirect(success_url)

    return render(request, 'register.html', {'form': form})