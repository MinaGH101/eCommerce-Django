from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *


class RegisterView(View):
    
    form_class = RegisterForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, 'accounts/register.html', context={'form':self.form_class()})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            login(request, user)
            return redirect('home:home')
        
        return render(request, 'accounts/register.html', context={'form': form})
    
    
class LoginView(View):

    form_class = LoginForm
    
    def setup(self, request, *args, **kwargs):      
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                # messages.success(request, 'You are in !!', 'alert alert-success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            else:
                messages.error(request, 'username or password is wrong !!', 'alert alert-danger')
        return render(request, 'accounts/login.html', context={'form': form})


class LogoutView(LoginRequiredMixin ,View):
    def get(self, request):
        logout(request)
        messages.success(request, "you are out !", 'alert alert-warning')
        return redirect('home:home')
    
    
    
class ProfileView(LoginRequiredMixin, View):
    form_class = UserProfileForm
    
    def get(self, request):
        profile = Profile.objects.filter(user = request.user)[0]
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email, 'username':request.user.username})
        
        
        return render(request, 'accounts/profile.html', {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user = User.objects.get(id = request.user.id)
            user.username = cd['username']
            user.email = cd['email']
            user.save()

            messages.success(request, 'profile saved successfully.', 'alert alert-success')
            
        return redirect('accounts:profile')
