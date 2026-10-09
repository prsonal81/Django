from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()  # Muestra el nombre, no el ID

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category')