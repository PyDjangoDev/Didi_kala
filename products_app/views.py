from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import Http404
# Create your views here.

def products_app_view(request):
    products_list = Product.objects.all()  
    return render (request,template_name='products.html',context={
        'products' : products_list
        
    })
    

def product_detail_view(request, id1, slug=None):
    if id1 :
        if slug :
            product = get_object_or_404(Product,id=id1,slug=slug)
        else:
            product = get_object_or_404(Product,id=id1)
    else:
        return render(request,'404.html')
    
    if product.is_active:
        colors = product.color.all()
        off_deadline = product.off_deadline
        categories = Category.objects.filter(parent=None, is_active=True)
        album = product.product_album_set.all()
        important_attributes_and_values = product.attr_values.filter(important_attribute=True)
        attributes_and_values = product.attr_values.all()
        return render (request,'product_detail.html',context={
            'product' : product,
            'colors' : colors,
            'is_active' : True,
            'off_deadline': off_deadline,
            'categories' : categories,
            'album' : album,
            'important_attributes' : important_attributes_and_values,
            'attributes_and_values' : attributes_and_values
            
        })
    else:
        return render(request,'product_detail.html',context={
            'is_active' : False
        })            
    