from django.core.management.base import BaseCommand
from ..models import Category, Brand, Product, Review, Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        category1 = Category.objects.create(name="Смартфоны", description="Смартфоны всех производителей")
        category2 = Category.objects.create(name="Ноутбуки", description="Ноутбуки всех производителей")

        brand1 = Brand.objects.create(name="Samsung", country="Южная Корея")
        brand2 = Brand.objects.create(name="Apple", country="США")

        for i in range(10):
            Product.objects.create(
                name=f"Продукт {i + 1}",
                price=random.uniform(100, 1000),
                in_stock=bool(random.getrandbits(1)),
                brand=random.choice([brand1, brand2]),
                category=random.choice([category1, category2]),
                discount=random.uniform(0, 30),
                status=random.choice(['NEW', 'POPULAR', 'DISCOUNT']),
                quantity=random.randint(0, 20),
            )

        products = Product.objects.all()
        for product in products:
            for _ in range(random.randint(1, 5)):
                Review.objects.create(
                    product=product,
                    user_name="TestUser",
                    rating=random.randint(1, 5),
                    comment="Это тестовый отзыв.",
                    created_at=timezone.now()
                )

        user = User.objects.create_user(username="testuser", password="testpass")

        for _ in range(5):
            order = Order.objects.create(
                user=user,
                description="Тестовый заказ с описанием",
                created_at=timezone.now(),
                status=random.choice(['PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED'])
            )
            for product in random.sample(list(products), 3):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 3),
                    price_at_order=product.price
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена тестовыми данными.'))
