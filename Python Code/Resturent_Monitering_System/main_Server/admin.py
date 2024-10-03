from django.contrib import admin
import markupsafe

# Register your models here.
from .models import GeneratedValue,Categories   # Adjust the import based on your model's location

@admin.register(GeneratedValue)
class GeneratedValueAdmin(admin.ModelAdmin):
    list_display = ('conan_id', 'description', 'some_text', 'image')  # Include the image field

    # To display the image as an actual image instead of a file path
    def image_tag(self, obj):
        if obj.image:
            return markupsafe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return '-'
    image_tag.short_description = 'Image'  # Column name in admin panel

    list_display = ('conan_id', 'description', 'some_text', 'image_tag')  # Replace 'image' with 'image_tag'







    # -----------------Register Categories--------------------
    admin.site.register(Categories) 