# Откат к версии с 6 карточками товаров: удалить поле image у Category, сбросить данные

from decimal import Decimal
from django.db import migrations, models


def reset_to_six_products(apps, schema_editor):
    """Удалить все товары и категории, создать только 6 начальных товаров (как в 0002)."""
    Product = apps.get_model('main', 'Product')
    Category = apps.get_model('main', 'Category')
    Product.objects.all().delete()
    Category.objects.all().delete()
    products = [
        {'name': 'Дрель ударная GSB 18V-50', 'slug': 'drel-udarnaya-gsb-18v-50', 'price': Decimal('12490.00'), 'old_price': Decimal('14990.00'), 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=Дрель', 'order': 1},
        {'name': 'УШМ 125 мм 900 Вт', 'slug': 'ushm-125-900', 'price': Decimal('4790.00'), 'old_price': None, 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=УШМ', 'order': 2},
        {'name': 'Перфоратор GBH 2-26 DRE', 'slug': 'perforator-gbh-2-26', 'price': Decimal('18990.00'), 'old_price': Decimal('21490.00'), 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=Перфоратор', 'order': 3},
        {'name': 'Лазерный уровень 360°', 'slug': 'lazernyj-uroven-360', 'price': Decimal('8290.00'), 'old_price': None, 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=Лазер', 'order': 4},
        {'name': 'Шуруповёрт аккумуляторный 18 В', 'slug': 'shurupovert-18v', 'price': Decimal('6590.00'), 'old_price': Decimal('7990.00'), 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=Шуруповёрт', 'order': 5},
        {'name': 'Инвертор сварочный 200 А', 'slug': 'invertor-svarochnyj-200', 'price': Decimal('15990.00'), 'old_price': None, 'image': 'https://placehold.co/400x400/1a1d2e/4a9eff?text=Сварка', 'order': 6},
    ]
    for p in products:
        Product.objects.create(**p)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_category_image'),
    ]

    operations = [
        migrations.RunPython(reset_to_six_products, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
    ]
