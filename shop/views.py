from django.shortcuts import render, redirect
from django.views import View
from .models import *
from blog.models import Subscribe
from django.contrib import messages
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import Max, Min
from django.db.models import Count
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

class ShopNewestView(ListView):
    form_class = SearchForm
    def get(self, request, sort_by, category): 
        categories = Product.objects.filter().order_by('category').values('category__name').annotate(count=Count('category__name'))
        cats = {d['category__name']: d['count'] for d in categories}
                   
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        abs_max =  Product.objects.all().aggregate(Max('price'))['price__max']
        abs_min =  Product.objects.all().aggregate(Min('price'))['price__min']    
            
        form = self.form_class()
        
        if min_price and max_price:
            if category == 'all':
                product_list = Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
            else:
                cat = Category.objects.filter(name=category)[0]
                product_list = Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price), category=cat)
            
        else:
            min_price = abs_min
            max_price = abs_max 
            if request.GET.get('search_bar'):
                product_list = Product.objects.filter(Q(title__icontains=request.GET['search_bar']))
                
            elif sort_by== 'newest':
                if category == 'all':
                    product_list = Product.objects.filter().order_by('-created').reverse()
                else:
                    cat = Category.objects.filter(name=category)[0]
                    product_list = Product.objects.filter(category=cat)
                
            elif sort_by== 'most_rated':
                if category == 'all':
                    product_list = Product.objects.filter()
                else:
                    cat = Category.objects.filter(name=category)[0]
                    product_list = Product.objects.filter(category=cat)

                unsorted_results = product_list.all()
                product_list = sorted(unsorted_results, key= lambda t: t.rate())
                
            elif sort_by== 'most_seller':
                if category == 'all':
                    product_list = Product.objects.filter()
                else:
                    cat = Category.objects.filter(name=category)[0]
                    product_list = Product.objects.filter(category=cat)
                    
                unsorted_results = product_list.all()
                product_list = sorted(unsorted_results, key= lambda t: t.seller())
                    
            else:
                if category == 'all':
                    product_list = Product.objects.filter()
                else:
                    cat = Category.objects.filter(name=category)[0]
                    product_list = Product.objects.filter(category=cat)
            

        paginator = Paginator(list(reversed(product_list)), 9)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user)
            cartItems = cart.cart_items
        else:
            cartItems= '0'
            
        
        top_rating = Product.objects.filter()[:5]
        unsorted_results = top_rating.all()
        top_rating = sorted(unsorted_results, key= lambda t: t.rate())
        return render(request, 'shop/shop-newest.html', {"page_obj": page_obj, 'cartItems':cartItems, 'cats':cats,
                                                         'min_price':min_price, 'max_price':max_price, 'abs_max':abs_max, 'abs_min':abs_min,
                                                         'form':form, 'top_rating':top_rating, 'sort_by':sort_by})
        
        
    def post(self, request):
        email = request.POST['sub-email']
        user = request.user
        if user.is_authenticated:
            subscriber = Subscribe.objects.filter(email=email).exists()
            if subscriber:
                messages.warning(request, 'this email is already subscribed !')
            else:
                Subscribe.objects.create(user=user, email=email)
                messages.success(request, 'You are Subscribed !', 'alert alert-success')
            
        else:
            return redirect('accounts:login')
            
        return redirect('blog:blog')
  
  


class FilterPriceView(View):
    def post(self, request):
        slider_value = request.POST.get('slider')
        
        return render(request, 'your_template.html', {'slider_value': slider_value})


  
  
class ShopDetailView(View):
    form_class = SizeForm
    
    def get(self, request, product_id):
        form = self.form_class()
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(category = product.category)
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user)
            cartItems = cart.cart_items
        else:
            cartItems= '0'
            
        if request.user.is_authenticated:
            user = request.user
            cart, created = Cart.objects.get_or_create(customer=user)
            items = cart.items.all()
            item = items.filter(product=product)
        return render(request, 'shop/shop-detail.html', {'product':product, 'cartItems':cartItems,
                                                         'related_products':related_products, 'form':form})
        
    def post(self, request, product_id):
        form = self.form_class(request.POST)
        product = Product.objects.get(id=product_id)
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer = request.user)
            if form.is_valid():
                cd = form.cleaned_data
            if cd['size_L'] == True:
                if CartItem.objects.filter(product=product, cart=cart, size = 'L').exists():
                    item = CartItem.objects.get(product=product, cart=cart, size = 'L')
                    item.quantity+=1
                    item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, cart=cart, size = 'L')
                    
            if cd['size_M'] == True:
                if CartItem.objects.filter(product=product, cart=cart, size = 'M').exists():
                    item = CartItem.objects.get(product=product, cart=cart, size = 'M')
                    item.quantity+=1
                    item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, cart=cart, size = 'M')
                    
            if cd['size_S'] == True:
                if CartItem.objects.filter(product=product, cart=cart, size = 'S').exists():
                    item = CartItem.objects.get(product=product, cart=cart, size = 'S')
                    item.quantity+=1
                    item.save()
                else:
                    cart_item = CartItem.objects.create(product=product, cart=cart, size = 'S')
                    
            return redirect('shop:cart')
        
        return redirect('accounts:login')
    
    
class CartView(LoginRequiredMixin,View):
    form_class = NoteForm
    def get(self, request):
        form = self.form_class()
        user = request.user
        cart, created = Cart.objects.get_or_create(customer=user)
        items = cart.items.all()
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(customer=request.user)
            cartItems = cart.cart_items
        else:
            cartItems= '0'
        return render(request, 'shop/cart-page.html', {'cart':cart, 'items':items, 'cartItems':cartItems, 'form':form})
    
    
class RateView(LoginRequiredMixin ,View):
    def get(self, request, product_id, rating):
        product = Product.objects.get(id=product_id)
        user = request.user
        
        # if Cart.objects.filter(customer=user).items.product == product:
        if Vote.objects.filter(product=product, user=user).exists():
            Vote.objects.filter(product=product, user=user).delete()
        Vote.objects.create(product=product, user=user, rating=rating)

        return redirect('shop:shop-detail', product_id)


class AddToCartView(LoginRequiredMixin ,View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(customer=request.user)
        if CartItem.objects.filter(product=product, cart=cart).exists():
            item = CartItem.objects.get(product=product, cart=cart)
            item.quantity+=1
            item.save()
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart)
        
        return redirect('shop:shop-detail', product_id)


class DeleteItemView(LoginRequiredMixin ,View):
    def get(self, request, product_id):
        cart = Cart.objects.get(customer=request.user)
        product= Product.objects.get(id=product_id)
        item = CartItem.objects.filter(cart=cart, product=product)[0]
        item.delete()
        return redirect('shop:cart')
    
    
class CheckOutView(LoginRequiredMixin ,View):
    form_class = ShippingForm
    def get(self, request, cart_id):
        cart = Cart.objects.get(id = cart_id)
        items = cart.items.all()
        form = self.form_class(instance=request.user.profile)
        
        return render(request, 'shop/checkout.html', {'form':form, 'cart':cart, 'items':items})
    
    def post(self, request, cart_id):
        form = self.form_class(request.POST)
        cart = Cart.objects.get(id=cart_id)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.cart = cart
            shipping.save()
            
        for item in cart.items:
            product_seller = Seller.objects.get_or_create(product=item.product)
            product_seller.seller += 1
            product_seller.save()
            
            
        return redirect('home:home')
        
        
        
        
def deleteItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    size= data['Size']
    print('Product:', productId)
    
    if action == "delete":
        cart = Cart.objects.get(customer=request.user)
        product= Product.objects.get(id=productId)
        item = CartItem.objects.filter(cart=cart, product=product, size=size)[0]
        item.delete()
    
    return JsonResponse('Item was deleted', safe=False)
    



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    size = data['Size']
    
    customer = request.user
    product = Product.objects.get(id=productId)
    cart, created = Cart.objects.get_or_create(customer=customer, completed=False)
    
    orderItem, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)


def addToCart(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        product = Product.objects.get(id=productId)
        if action == "add":
            cart, created = Cart.objects.get_or_create(customer=request.user)
            if CartItem.objects.filter(product=product, cart=cart).exists():
                item = CartItem.objects.get(product=product, cart=cart)
                item.quantity+=1
                item.save()
            else:
                cart_item = CartItem.objects.create(product=product, cart=cart)
                
    else:
        redirect('accounts:login')
        
    return JsonResponse('Item was added', safe=False)

def Discount(request):
    data = json.loads(request.body)
    value = data['value']
    cartId = data['cartId']
    action = data['action']
    if action == "compute":
        cart = Cart.objects.get(id=cartId)
        cart.discount = value
        cart.save()
        
    
    return JsonResponse('Item was added', safe=False)

