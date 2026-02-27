from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from .models import Product


@require_GET
@cache_control(max_age=60, public=True)
def home(request):
    """Главная страница — каталог с карточками товаров (6 товаров)."""
    products = Product.objects.filter(in_stock=True).order_by('order', 'name')
    return render(request, 'main/index.html', {'products': products})
