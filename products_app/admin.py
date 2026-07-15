from django.contrib import admin
from .models import (
    Product, Color, Category, Product_album, 
    Attribute_1, ProductAttributeValue, 
)
from mptt.admin import DraggableMPTTAdmin

# --- Inlines ---

class ProductAttributeValueInline(admin.StackedInline):
    model = ProductAttributeValue
    extra = 1 
    autocomplete_fields = ['attribute'] 
    
    
    
    
class AttributeInline(admin.TabularInline):
    model = Attribute_1
    extra = 1
    autocomplete_fields = ['category']

# --- Admins ---


@admin.register(Attribute_1)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'field_type', 'category') 
    list_filter = ('field_type', 'category') 
    search_fields = ('title',)
    autocomplete_fields = ['category']




@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'is_active')
    list_display_links = ('indented_title',)
    list_filter = ('is_active',)
    search_fields = ('title',)

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'تعداد محصولات'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'count', 'off', 'is_active', 'id', 'is_delete']
    list_filter = ['price', 'count', 'category', 'is_active']
    list_editable = ['price', 'count', 'off', 'is_active', 'is_delete']
    search_fields = ('title',)
    inlines = [ProductAttributeValueInline]




@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'hex_code', 'is_active')
    search_fields = ('title',)





@admin.register(Product_album)
class ProductAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'create_at')
    search_fields = ('title',)