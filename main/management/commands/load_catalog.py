"""
Загрузка категорий и товаров из main.category_data в БД.
Запуск: python manage.py load_catalog
"""
from decimal import Decimal
import re

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from main.category_data import CATEGORIES
from main.models import Category, Product


def parse_price(price_str):
    """Извлекает число из строки цены (например '£89.99' -> Decimal('89.99'))."""
    if not price_str:
        return Decimal('0')
    match = re.search(r'[\d.,]+', str(price_str).replace(',', '.'))
    if match:
        return Decimal(match.group(0))
    return Decimal('0')


def make_product_slug(name, category_slug, used_slugs):
    """Генерирует уникальный slug для товара."""
    base = slugify(name) or 'product'
    if not base:
        base = 'product'
    slug = base
    n = 1
    while slug in used_slugs:
        slug = f'{base}-{n}'
        n += 1
    used_slugs.add(slug)
    return slug


class Command(BaseCommand):
    help = 'Загружает категории и товары из category_data в базу данных'

    def handle(self, *args, **options):
        used_product_slugs = set(Product.objects.values_list('slug', flat=True))

        for order, cat_data in enumerate(CATEGORIES):
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'parent_id': None,
                    'order': order,
                }
            )
            action = 'Создана' if created else 'Обновлена'
            self.stdout.write(f'  {action} категория: {category.name}')

            for prod_order, prod in enumerate(cat_data.get('products', [])):
                slug = make_product_slug(prod['name'], category.slug, used_product_slugs)
                price = parse_price(prod.get('price', '0'))
                Product.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': prod['name'],
                        'category': category,
                        'price': price,
                        'image': prod.get('image', ''),
                        'in_stock': True,
                        'order': prod_order,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'Каталог загружен: {len(CATEGORIES)} категорий.'))
