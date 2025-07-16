import requests
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from .models import Shoe, Order, Payment, Category
from .serializers import ShoeSerializer, OrderSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class ShoeViewSet(viewsets.ModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

KHALTI_SECRET_KEY = '1231654564key'

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
    