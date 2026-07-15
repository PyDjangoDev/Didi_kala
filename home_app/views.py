from django.shortcuts import render
from products_app.models import Category

# Create your views here.

def home_app_view(request):
    return render (request,template_name='home.html',context={
        
    })
    
    
    
    
def header_component(request):
    
    return render(request,template_name='header.html',context={
        
    })
    
def footer_component(request):
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('children')  
    return render(request,template_name='footer.html',context={
        'categories':categories
        
    })
    
