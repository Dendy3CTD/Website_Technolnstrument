"""
Админ-панель: товары, пользователи, заказы, платежи, бухгалтерия.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem, Payment, AccountingEntry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order']
    list_editable = ['order']
    list_filter = ['parent']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    fields = ['name', 'slug', 'parent', 'order']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'admin/main/product/change_list.html'
    list_display = ['name', 'category', 'brand', 'price', 'old_price', 'in_stock', 'order', 'updated_at']
    list_display_links = ['name']
    list_filter = ['category', 'brand', 'in_stock']
    list_editable = ['price', 'old_price', 'in_stock', 'order']
    list_per_page = 25
    ordering = ['order', 'name']
    search_fields = ['name', 'brand', 'description']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from .models import Category
        extra_context['category_tabs'] = Category.objects.filter(parent=None).order_by('order', 'name')
        return super().changelist_view(request, extra_context)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Карточка товара', {
            'fields': ('name', 'slug', 'category', 'brand', 'description'),
        }),
        ('Цены', {
            'fields': ('price', 'old_price'),
        }),
        ('Изображение', {
            'fields': ('image',),
            'description': 'Ссылка на изображение (URL). Например: https://placehold.co/400x400/1a1d2e/4a9eff?text=Товар',
        }),
        ('Наличие и порядок', {
            'fields': ('in_stock', 'order'),
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['phone', 'email', 'full_name']
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'price', 'quantity']
    list_filter = ['order']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method']


@admin.register(AccountingEntry)
class AccountingEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'entry_type', 'amount', 'description', 'order', 'created_at']
    list_filter = ['entry_type', 'date']
    search_fields = ['description']
