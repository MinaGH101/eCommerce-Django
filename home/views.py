from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product, Project
from blog.models import Post
from blog.models import Subscribe
from django.contrib import messages
from django.db.models import Count
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    form_message_class = MessageForm
    def get(self, request):
        products = Product.objects.filter().order_by('-id')[:4]
        projects = Project.objects.filter().order_by('-id')[:5]
        categories = Product.objects.filter().order_by('category').values('category__name').annotate(count=Count('category__name'))
        cats = {d['category__name']: d['count'] for d in categories}
        
        project1 = Project.objects.filter().order_by('-id')[:1]
        project2 = Project.objects.filter().order_by('-id')[1:2]
        project3 = Project.objects.filter().order_by('-id')[2:3]
        project4 = Project.objects.filter().order_by('-id')[3:4]
        project5 = Project.objects.filter().order_by('-id')[4:5]
        # if request.user.is_authenticated:
        #     cart, created = Cart.objects.get_or_create(customer=request.user)
        #     cartItems = cart.cart_items
        # else:
        #     cartItems= '0'

        titles = []
        for p in projects:
            titles.append(p.title)
            
        posts = Post.objects.filter().order_by('-id')[:3]
        
        product_list = Product.objects.filter()[:4]
        unsorted_results = product_list.all()
        # product_list = sorted(unsorted_results, key= lambda t: t.seller())
        print(titles[2])
        context = {'products':products, 'posts':posts, 'cats':cats, 'projects':projects, 'titles':titles
                   , 'project1':project1
                   , 'project2':project2
                   , 'project3':project3
                   , 'project4':project4
                   , 'project5':project5,
                   'message_form':self.form_message_class,}
        return render(request, 'home/home2.html', context)
    
    def post(self, request):
        message_form = self.form_message_class(request.POST)
        
        if request.user.is_authenticated:
        
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.user = request.user
                message.save()
                messages.success(request, 'Your message saved successfully.', 'alert alert-success')
                return redirect('home:home')
            
        else:
            return redirect('accounts:login')

        return redirect('home:home')

    
class ContactView(View):
    form_message_class = MessageForm
    def get(self, request):
        
        return render(request, 'home/contact-us.html', {'message_form':self.form_message_class,})
    
        
    def post(self, request):
        message_form = self.form_message_class(request.POST)
        
        if request.user.is_authenticated:
        
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.user = request.user
                message.save()
                messages.success(request, 'Your message saved successfully.', 'alert alert-success')
                return redirect('home:contact')
            
        else:
            return redirect('accounts:login')

        return redirect('home:contact')


class AboutView(View):
    form_message_class = MessageForm
    def get(self, request):
        
        return render(request, 'home/about-us.html',
                      {'message_form':self.form_message_class})
    
    def post(self, request):
        message_form = self.form_message_class(request.POST)

        if request.user.is_authenticated:
        
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.user = request.user
                message.save()
                messages.success(request, 'Your message saved successfully.', 'alert alert-success')
                return redirect('home:about')
            
        else:
            return redirect('accounts:login')
                
        return redirect('blog:blog')


class MessageView(View):
    form_class = MessageForm
    def get(self, request, cart_id):
        form = self.form_class()
        
        return render(request, 'blog/blog-detail.html', {'form2':form,})
    
    def post(self, request, cart_id):
        form = self.form_class(request.POST)


        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            message.success(request, 'Your information saved successfully.', 'alert alert-success')

        return redirect('home:home')
