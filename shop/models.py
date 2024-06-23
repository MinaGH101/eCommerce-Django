from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, default='indoor', blank=True, null=True)
    
    def __str__(self):
        return self.name
    


class Project(models.Model):

    title = models.CharField(max_length=100, blank=True, null=True, default='Project')
    description = models.TextField()
    employee = models.CharField(max_length=100, blank=True, null=True, default='IUST')
    img_proj = models.FileField(upload_to='images', default=None)
    img_emp = models.FileField(upload_to='images', default=None)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def img_empURL(self):
        try:
            url = self.img_emp.url
        except:
            url = ''
        return url

    @property
    def img_projURL(self):
        try:
            url = self.img_proj.url
        except:
            url = ''
        return url



class Product(models.Model):
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=200, null=True, blank=True, default='See More')
    description = models.TextField()
    img = models.FileField(upload_to='images', default=None)
    created = models.DateTimeField(auto_now_add=True)
    

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category_products')

    @property
    def imgURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url
    
    # def votes(self):
    #     return self.product_votes.count()
    
    # def rate(self):
    #     return Vote.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0
    
    # def seller(self):
    #     product_seller = Seller.objects.filter(product=self)[0]
    #     seller = product_seller.seller
        
    #     return seller




# class Cart(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_cart')
#     created = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False, blank=True, null=True)
#     discount = models.IntegerField(default=0, blank=True, null=True)
    
#     @property
#     def cart_items(self):
#         items = self.items.all()
#         total = sum([item.quantity for item in items])
#         return total
    
#     @property
#     def discounted_price(self):
#         items = self.items.all()
#         total = sum([item.total_price for item in items])
#         og_price = total
#         discounted_price = og_price - (og_price*(self.discount/100))
#         return discounted_price
    
#     @property
#     def cart_total_price(self):
#         items = self.items.all()
#         total = sum([item.total_price for item in items])
#         return total
    
    

# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
#     cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True, related_name='items')
#     size = models.CharField(max_length=10, default='M', blank=True, null=True)
#     quantity = models.IntegerField(default=1, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
    
#     @property
#     def total_price(self):
#         total = self.product.price * self.quantity
#         return total
    


# class Seller(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_seller')
#     seller = models.IntegerField(default=0, blank=True, null=True)


# class Vote(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_votes')
#     rating = models.IntegerField(default=0, blank=True, null=True)
    
#     def __str__(self):
#         return f'{self.user} rated {self.product}' 



# class Shipping(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_shipping', blank=True, null=True)
#     user = models.OneToOneField(User, default=None ,on_delete=models.CASCADE, blank=True, null=True)
#     first_name = models.CharField(max_length=50, default=None, blank=True, null=True)
#     last_name = models.CharField(max_length=50, default=None, blank=True, null=True)
#     phone = models.CharField(max_length=50,default=None, blank=True, null=True)
#     address1 = models.CharField(max_length=50, default=None, blank=True, null=True)
#     address2 = models.CharField(max_length=50, default=None, blank=True, null=True)
#     state = models.CharField(max_length=50, default=None, blank=True, null=True)
#     area = models.CharField(max_length=50, default=None, blank=True, null=True)
#     postal_code = models.CharField(max_length=50,default=None, blank=True, null=True)
#     created = models.DateTimeField(auto_now_add=True)
    


# class Promo(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
#     active = models.BooleanField()
    
#     def __str__(self):
#         return self.code







