from django.shortcuts import render
from products_app.models import Category
from products_app.models import Product 

# Create your views here.

def home_app_view(request):
    amazing_products = Product.objects.filter(
    off__gt=0, 
    is_active=True, 
    is_delete=False
    ).order_by('-off') 
    return render (request,template_name='home.html',context={
        'amazing_products' : amazing_products       
    })
    
    
    
    
def header_component(request):

    
    return render(request,template_name='header.html',context={

        
    })
    
    
    
def footer_component(request):
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('children')  
    return render(request,template_name='footer.html',context={
        'categories':categories
        
    })
    
    

