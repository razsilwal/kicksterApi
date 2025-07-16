from rest_framework import serializers
from .models import Shoe, Order, Category

class ShoeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=False)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Shoe
        fields = '__all__'

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            Category, _= Category.objects.get_or_create(name=category_name)
            validated_data['catrgory'] = Category
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']