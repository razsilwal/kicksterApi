from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoeViewSet, OrderViewSet, CategoryViewSet,  verify_khalti_payment

router = DefaultRouter()
router.register('shoes', ShoeViewSet)
router.register('orders', OrderViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-khalti-payment/', verify_khalti_payment),
]