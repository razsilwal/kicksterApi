import requests
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, generics, permissions
from .models import Shoe, Order, Payment, Category, CartItem, Review, Wishlist, Profile
from .serializers import ShoeSerializer, UserSerializer, OrderSerializer, CategorySerializer, CartItemSerializer, ReviewSerializer, WishlistSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from django.contrib.auth.models import User

# Create your views here.

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS for everyone
        return request.user and request.user.is_staff  # Only admin users can write

class ShoeViewSet(viewsets.ModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        shoe = serializer.validated_data['shoe']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(user=user, shoe=shoe,
                                                       defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
class  ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

KHALTI_SECRET_KEY = 'test_public_key_99697f8fd7fc41e8b922cb5f84cf4e82'

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_khalti_payment(request):
    token = request.data.get("token")
    amount = request.data.get("amount")
    order_id = request.data.get("order_id")
    order = Order.objects.get(id=order_id)

    payload = {
        "token": token,
        "amount": amount
    }

    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}"
    }

    response = requests.post("https://khalti.com/api/v2/payment/verify/", data=payload, headers=headers)
    res_data = response.json()

    if response.status_code == 200 and res_data.get("idx"):
        payment = Payment.objects.create(
            order=order,
            khati_transaction_id = res_data["idx"],
            amount=amount,
            verified = True,
            verified_at = timezone.now()
        )
        order.paid = True
        order.save()

        return Response({"message" : "Payment Verified "})
    else:
        return Response({"error":"Payment Verification Failed ", "details":res_data}, status=400)
    