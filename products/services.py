from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from .models import Product

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price):
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, price):
        return price

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, price):
        return price * (1 - self.percentage)

class SeasonalDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, price):
        return price * (1 - self.percentage)

class DiscountContext:
    """Contexto que aplica la estrategia seleccionada."""
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def calculate(self, price):
        return round(self.strategy.apply(price), 2)

class ProductService:
    @staticmethod
    def get_product(product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Producto no encontrado")

    @staticmethod
    def calculate_final_price(product_id, discount_type="none"):
        """Calcula el precio final aplicando la estrategia de descuento."""
        product = ProductService.get_product(product_id)

        strategies = {
            "none": NoDiscount(),
            "percentage": PercentageDiscount(0.10),
            "seasonal": SeasonalDiscount(0.20),
        }
        strategy = strategies.get(discount_type, NoDiscount())
        context = DiscountContext(strategy)

        return {
            "product": product.name,
            "category": product.category.name if product.category else None,
            "original_price": float(product.price),
            "final_price": context.calculate(float(product.price)),
            "discount_type": discount_type,
        }