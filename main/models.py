"""
Модели: товары, пользователи (Django User), заказы, платежи, бухгалтерия.
"""
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Категория товаров (например: Дрели, УШМ)."""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар в каталоге."""
    name = models.CharField('Название', max_length=300)
    slug = models.SlugField('URL', max_length=300, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Категория'
    )
    brand = models.CharField('Бренд', max_length=100, blank=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Цена, ₽',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    old_price = models.DecimalField(
        'Старая цена, ₽',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    image = models.URLField('URL изображения', max_length=500, blank=True)
    in_stock = models.BooleanField('В наличии', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def price_display(self):
        """Цена для отображения: «12 490 ₽»."""
        s = f'{self.price:,.0f}'.replace(',', ' ')
        return f'{s} ₽'

    def old_price_display(self):
        """Старая цена для отображения или пустая строка."""
        if self.old_price is None:
            return ''
        s = f'{self.old_price:,.0f}'.replace(',', ' ')
        return f'{s} ₽'


class Order(models.Model):
    """Заказ пользователя."""
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_PAID = 'paid'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_CONFIRMED, 'Подтверждён'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_SHIPPED, 'Отправлен'),
        (STATUS_DELIVERED, 'Доставлен'),
        (STATUS_CANCELLED, 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    full_name = models.CharField('ФИО', max_length=200, blank=True)
    address = models.TextField('Адрес доставки', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    total = models.DecimalField(
        'Сумма, ₽',
        max_digits=12,
        decimal_places=2,
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))]
    )
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'История заказов'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} от {self.created_at.strftime("%d.%m.%Y")}'


class OrderItem(models.Model):
    """Позиция в заказе (товар + количество + цена на момент заказа)."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Товар'
    )
    product_name = models.CharField('Название товара', max_length=300)
    price = models.DecimalField(
        'Цена за ед., ₽',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    @property
    def subtotal(self):
        return self.price * self.quantity


class Payment(models.Model):
    """Платёж по заказу (бухгалтерия: приходы)."""
    METHOD_CARD = 'card'
    METHOD_CASH = 'cash'
    METHOD_OTHER = 'other'
    METHOD_CHOICES = [
        (METHOD_CARD, 'Карта'),
        (METHOD_CASH, 'Наличные'),
        (METHOD_OTHER, 'Другое'),
    ]
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_COMPLETED, 'Проведён'),
        (STATUS_FAILED, 'Ошибка'),
        (STATUS_REFUNDED, 'Возврат'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Заказ',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        'Сумма, ₽',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    method = models.CharField(
        'Способ оплаты',
        max_length=20,
        choices=METHOD_CHOICES,
        default=METHOD_CARD
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    description = models.CharField('Описание', max_length=300, blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.amount} ₽ — {self.get_status_display()}'


class AccountingEntry(models.Model):
    """Проводка бухгалтерии: приход или расход."""
    ENTRY_INCOME = 'income'
    ENTRY_EXPENSE = 'expense'
    ENTRY_CHOICES = [
        (ENTRY_INCOME, 'Приход'),
        (ENTRY_EXPENSE, 'Расход'),
    ]

    date = models.DateField('Дата')
    entry_type = models.CharField(
        'Тип',
        max_length=10,
        choices=ENTRY_CHOICES
    )
    amount = models.DecimalField(
        'Сумма, ₽',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    description = models.CharField('Описание', max_length=500)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accounting_entries',
        verbose_name='Заказ'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accounting_entries',
        verbose_name='Платёж'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Проводка'
        verbose_name_plural = 'Бухгалтерия'
        ordering = ['-date', '-id']

    def __str__(self):
        sign = '+' if self.entry_type == self.ENTRY_INCOME else '−'
        return f'{self.date}: {sign}{self.amount} ₽ — {self.description[:40]}'
