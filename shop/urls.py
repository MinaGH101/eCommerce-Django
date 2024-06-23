from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    # path('shop/<str:sort_by>/<str:category>/', views.ShopNewestView.as_view(), name='newest'),
    path('shop-detail/<int:product_id>', views.ShopDetailView.as_view(), name='shop-detail'),
    path('project-detail/<int:project_id>', views.ProjectDetailView.as_view(), name='project-detail'),
    # path('cart/', views.CartView.as_view(), name='cart'),
    # path('add-to-cart/', views.addToCart, name="shop-add-to-cart"),
    # path('discount/', views.Discount, name="discount"),
    # path('rate/product/<int:product_id>/<int:rating>/', views.RateView.as_view(), name='rate'),
    # path('shop-detail/add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    # path('cart/delete-item/<int:product_id>/', views.DeleteItemView.as_view(), name='delet-item'),
    # path('cart/delete_item/', views.deleteItem, name='delet_item'),
    # path('update_item/', views.updateItem, name="update_item"),
    # path('shipping/<int:cart_id>/', views.CheckOutView.as_view(), name='checkout'),
]
