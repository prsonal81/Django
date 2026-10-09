from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .services import ProductService

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    @action(detail=True, methods=["get"], url_path="precio-final")
    def precio_final(self, request, pk=None):
        discount_type = request.query_params.get("tipo", "none")
        try:
            result = ProductService.calculate_final_price(pk, discount_type)
            return Response(result)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)