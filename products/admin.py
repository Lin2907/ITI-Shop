from django.contrib import admin
from .models import Product, Category,Review
from taggit.forms import TagWidget

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        
    )

    ordering = ('sku',)

    formfield_overrides = {
        # Use the TagWidget to display tags as a text input with comma-separated values
        'tags': {'widget': TagWidget},
    }

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)