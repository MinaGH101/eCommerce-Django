from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=100, default='indoor', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    code = models.CharField(max_length=100)
    quantity = models.IntegerField()
    shipping_tax = models.CharField(max_length=100, default='Free')
    img = models.FileField(upload_to='images', default=None)
    created = models.DateTimeField(auto_now_add=True)
    
    size_L = models.BooleanField(default=True)
    size_M = models.BooleanField(default=True)
    size_S = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category_products')
    
    hot = models.BooleanField(default=False, blank=True, null=True)
    sale = models.BooleanField(default=False, blank=True, null=True)

    @property
    def imgURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url
    
    def votes(self):
        return self.product_votes.count()
    
    def rate(self):
        return Vote.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    def seller(self):
        product_seller = Seller.objects.filter(product=self)[0]
        seller = product_seller.seller
        
        return seller




class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_cart')
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    discount = models.IntegerField(default=0, blank=True, null=True)
    
    @property
    def cart_items(self):
        items = self.items.all()
        total = sum([item.quantity for item in items])
        return total
    
    @property
    def discounted_price(self):
        items = self.items.all()
        total = sum([item.total_price for item in items])
        og_price = total
        discounted_price = og_price - (og_price*(self.discount/100))
        return discounted_price
    
    @property
    def cart_total_price(self):
        items = self.items.all()
        total = sum([item.total_price for item in items])
        return total
    
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
    size = models.CharField(max_length=10, default='M', blank=True, null=True)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_price(self):
        total = self.product.price * self.quantity
        return total
    


class Seller(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_seller')
    seller = models.IntegerField(default=0, blank=True, null=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_votes')
    rating = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} rated {self.product}' 



class Shipping(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_shipping', blank=True, null=True)
    user = models.OneToOneField(User, default=None ,on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    phone = models.CharField(max_length=50,default=None, blank=True, null=True)
    address1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    address2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    area = models.CharField(max_length=50, default=None, blank=True, null=True)
    postal_code = models.CharField(max_length=50,default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    










