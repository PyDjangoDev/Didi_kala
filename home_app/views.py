from django.shortcuts import render
from products_app.models import Category, Product
from django.shortcuts import render, get_object_or_404


# Create your views here.

def home_app_view(request):
    amazing_products = Product.objects.filter(
        off__gt=0, 
        is_active=True, 
        is_delete=False
    ).order_by('-off')
    
    return render(request, 'home.html', {
        'amazing_products': amazing_products       
    })


def header_component(request):
    # دریافت تمام دسته‌بندی‌های فعال (برای MPTT)
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'header.html', {
        'categories': categories  # ارسال categories به هدر
    })


def footer_component(request):
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('children')
    
    return render(request, 'footer.html', {
        'categories': categories
    })


def amazing_products_all_view(request):
    amazing_products = Product.objects.filter(
        off__gt=0, 
        is_active=True, 
        is_delete=False
    ).order_by('-off')
    
    return render(request, 'products.html', {
        'products': amazing_products,
        'baner': False
    })