from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Category(MPTTModel):
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='دسته والد'
    )
    create_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        db_table = 'Category_table'
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'  

class Color(models.Model):
    title = models.CharField(max_length=20)
    hex_code = models.CharField(max_length=10)
    note = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    class Meta :
        db_table = 'Color_table'
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'        


class Product(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d/',null=True,blank=True)
    title = models.CharField(max_length=30)
    price = models.IntegerField()
    description = models.TextField(null=True,blank=True)
    color = models.ManyToManyField(Color,blank=True)
    off = models.IntegerField(null=True,blank=True)
    off_deadline = models.DateTimeField(null=True, blank=True, verbose_name='مهلت تخفیف')
    brand = models.CharField(max_length=25)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name='products')
    count = models.IntegerField(default=1)
    slug = models.SlugField(max_length=100,null=True,blank=True,unique=True,allow_unicode=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return self.title
    
    @property
    def formatted_final_price(self):

        if self.off:
            final = int(self.price * (1 - self.off / 100))
        else:
            final = self.price
    

        return "{:,}".format(final)
    
    
    def save (self,*args,**kwargs):
        if not self.slug :
            f = f'dkp-{self.title}-brand-{self.brand}'
            self.slug = f.replace(" " , "-")
        return super().save(*args,**kwargs)
    
    
    class Meta :
        db_table = 'product_table'
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    

class Product_album(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='products/album/')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title : 
            return f'{self.title}-{self.product.title}'
        else:
            return f'iamge-{self.product.title}'
    class Meta :
        db_table = 'product_album'
        verbose_name = 'آلبوم'
        verbose_name_plural = 'آلبوم ها'






    




class Attribute_1(models.Model):
    FIELD_TYPES = (
        ('text', 'متنی'),
        ('number', 'عددی'),
        ('boolean', 'بله/خیر'),
        ('choice', 'انتخابی'),
    )

    title = models.CharField(max_length=50, verbose_name="نام ویژگی")
    field_type = models.CharField(max_length=10, choices=FIELD_TYPES, default='text', verbose_name="نوع مقدار")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return f"{self.title}-({self.get_field_type_display()})"
    
    class Meta:
        db_table = 'Attribute_table'
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها '
    
    
class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attr_values')
    attribute = models.ForeignKey(Attribute_1, on_delete=models.CASCADE)
    value = models.CharField(max_length=100,verbose_name="مقدار")
    important_attribute = models.BooleanField(null=True,blank=True,verbose_name="ویژگی مهم",default='خیر')

    def __str__(self):
        return f"{self.attribute.title}: {self.value}"
    class Meta:
        db_table = 'ProductAttributeValue_table'
        verbose_name = 'ویژگی '
        verbose_name_plural = 'ویژگی ها '
        
    
    
