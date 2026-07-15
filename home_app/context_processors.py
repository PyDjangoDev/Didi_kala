from products_app.models import Category

def category_list_for_header(request):
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('children')
    return {
        'header_categories': categories  
    }
    
    