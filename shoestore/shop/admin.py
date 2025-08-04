from django.contrib import admin
from .models import Profile, Shoe, Order, Payment, Category, CartItem, Review, Wishlist 

# Register your models here.
admin.site.register(Category)
admin.site.register(Shoe)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Profile)