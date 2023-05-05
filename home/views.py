from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product, Cart
from blog.models import Post
from blog.models import Subscribe
from django.contrib import messages
from django.db.models import Count

class HomeView(View):
    def get(self, request):
        products = Product.objects.filter().order_by('-id')[:4]
        categories = Product.objects.filter().order_by('category').values('category__name').annotate(count=Count('category__name'))
        cats = {d['category__name']: d['count'] for d in categories}
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user)
            cartItems = cart.cart_items
        else:
            cartItems= '0'
            
        posts = Post.objects.filter().order_by('-id')[:3]
        
        product_list = Product.objects.filter()[:4]
        unsorted_results = product_list.all()
        product_list = sorted(unsorted_results, key= lambda t: t.seller())
        
        context = {'products':products, 'cartItems':cartItems, 'posts':posts, 'product_list':product_list, 'cats':cats}
        return render(request, 'home/home2.html', context)
    
    
class ContactView(View):
    def get(self, request):
        
        return render(request, 'home/contact-us.html')
    

class AboutView(View):
    def get(self, request):
        
        return render(request, 'home/about-us.html')
    
    def post(self, request):
        email = request.POST['sub-email']
        user = request.user
        if user.is_authenticated:
            subscriber = Subscribe.objects.filter(email=email).exists()
            if subscriber:
                messages.warning(request, 'this email is already subscribed !')
            else:
                Subscribe.objects.create(user=user, email=email)
                messages.success(request, 'You are Subscribed !', 'success')
            
        else:
            return redirect('accounts:login')
            
        return redirect('blog:blog')
