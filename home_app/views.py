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
    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    return render(request, 'home.html', {
        'amazing_products': amazing_products,
        'categories' : categories
    })




def header_component(request):
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'header.html', {
        'categories': categories 
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
    
    
    
def products_by_category_view(request, id):
    
    category = get_object_or_404(Category, id=id, is_active=True)
    
    all_categories = category.get_descendants(include_self=True)
    
    products = Product.objects.filter(
        category__in=all_categories,
        is_active=True,
        is_delete=False
    )
    
    total_products_count = products.count()
    
    return render(request, 'products.html', {
        'products': products,
        'category': category,
        'total_products_count': total_products_count,
    })