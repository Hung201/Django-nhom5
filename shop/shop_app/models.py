from django.db import models
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    BRAND = (
        ("Nike", "NIKE"),
        ("Hoka", "HOKA"),
        ("Salomon", "SALOMON"),
        ("Gucci", "GUCCI"),
        ("Dybbuk", "DYBBUK"),
        ("Converse", "CONVERSE"),
        ("Jordan", "JORDAN"),
        ("Vans", "VANS"),
    )
    
    name = models.CharField( max_length=100)
    sku = models.SlugField(blank=True,null=True)
    image = models.ImageField(upload_to='products_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=15, choices=BRAND, blank=True, null=True)
    color = models.CharField( max_length=100)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = slugify(self.name)
            unique_sku = self.sku
            counter = 1
            while Product.objects.filter(sku=unique_sku).exists():
                unique_sku = f'{self.sku}-{counter}'
                counter += 1
            self.sku = unique_sku
        super().save(*args, **kwargs)        
