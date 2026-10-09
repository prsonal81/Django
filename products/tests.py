from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Category, Product

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Creamos un usuario de prueba y lo autenticamos para evitar el error 401
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Creamos una categoría base para las pruebas
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post('/api/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Autenticación para las pruebas de productos
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Creamos una categoría y un producto base
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        response = self.client.post('/api/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalambrico',
            'price': 500.00
        })
        self.assertEqual(response.status_code, 201)

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        response = self.client.put(f'/api/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Laptop Pro')

    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

class PrecioFinalTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category1 = Category.objects.create(name='Electronica')
        self.category2 = Category.objects.create(name='Ropa')
        self.product1 = Product.objects.create(
            name='Laptop', category=self.category1, description='HP', price=1000
        )
        self.product2 = Product.objects.create(
            name='Camisa', category=self.category2, description='Azul', price=500
        )

    def test_precio_final_authenticated(self):
        """Con token: debe devolver 200 y el precio final."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/products/{self.product1.id}/precio-final/?tipo=percentage')
        self.assertEqual(response.status_code, 200)
        self.assertIn('final_price', response.data)
        self.assertEqual(response.data['final_price'], 900.0)

    def test_precio_final_unauthenticated(self):
        """Sin token: debe devolver 401."""
        response = self.client.get(f'/api/products/{self.product1.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
        