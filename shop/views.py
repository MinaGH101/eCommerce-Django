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
from datetime import datetime



class ProjectDetailView(View):
    
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        
        return render(request, 'shop/project-detail.html', {'project':project, })
  
  
class ShopDetailView(View):
    form_class = SizeForm
    
    def get(self, request, product_id):
        form = self.form_class()
        product = Product.objects.get(id=product_id)
        related_products = Product.objects.filter(category = product.category)
        
        # if request.user.is_authenticated:
        #     cart, created = Cart.objects.get_or_create(customer=request.user)
        #     cartItems = cart.cart_items
        # else:
        #     cartItems= '0'
            
        # if request.user.is_authenticated:
        #     user = request.user
        #     cart, created = Cart.objects.get_or_create(customer=user)
        #     items = cart.items.all()
        #     item = items.filter(product=product)
        return render(request, 'shop/shop-detail.html', {'product':product, 
                                                         'related_products':related_products, 'form':form})
  