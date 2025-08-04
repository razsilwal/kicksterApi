from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import ShoeViewSet, OrderViewSet, CategoryViewSet, CartItemViewSet, ReviewViewSet,WishlistViewSet, UserProfileView, UserViewSet, verify_khalti_payment

router = DefaultRouter()
router.register('shoes', ShoeViewSet)
router.register('orders', OrderViewSet)
router.register('categories', CategoryViewSet)
router.register('cart', CartItemViewSet) # /api/shop/cart/<id>/ 
router.register('reviews', ReviewViewSet)
router.register('wishlist', WishlistViewSet)
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileView.as_view(), name='user-profile') ,
    path('verify-khalti-payment/', verify_khalti_payment),
]