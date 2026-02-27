"""
Копирует 6 базовых товаров в каждую категорию.
Запуск: python manage.py copy_products_to_categories
"""
from django.core.management.base import BaseCommand

from main.models import Category, Product

# Slug'и 6 начальных товаров (как в миграции 0002)
INITIAL_SLUGS = [
    'drel-udarnaya-gsb-18v-50',
    'ushm-125-900',
    'perforator-gbh-2-26',
    'lazernyj-uroven-360',
    'shurupovert-18v',
    'invertor-svarochnyj-200',
]


class Command(BaseCommand):
    help = 'Копирует 6 имеющихся карточек товаров в каждую категорию'

    def handle(self, *args, **options):
        base_products = list(Product.objects.filter(slug__in=INITIAL_SLUGS).order_by('order'))
        if len(base_products) != 6:
            self.stdout.write(
                self.style.WARNING(
                    f'В базе найдено {len(base_products)} из 6 базовых товаров. '
                    'Сначала выполните миграции (python manage.py migrate).'
                )
            )
            return

        categories = list(Category.objects.all().order_by('order', 'name'))
        if not categories:
            self.stdout.write(
                self.style.WARNING('Нет ни одной категории. Создайте категории в админке (Категории).')
            )
            return

        created = 0
        for category in categories:
            for product in base_products:
                new_slug = f'{product.slug}-{category.slug}'[:300]
                _, was_created = Product.objects.get_or_create(
                    slug=new_slug,
                    defaults={
                        'name': product.name,
                        'category': category,
                        'brand': product.brand or '',
                        'description': product.description or '',
                        'price': product.price,
                        'old_price': product.old_price,
                        'image': product.image or '',
                        'in_stock': product.in_stock,
                        'order': product.order,
                    },
                )
                if was_created:
                    created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Готово: скопировано товаров {created} (в {len(categories)} категорий по 6 позиций; дубликаты пропущены).'
            )
        )
