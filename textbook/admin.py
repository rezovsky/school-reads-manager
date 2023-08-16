from django.contrib import admin
from .models import TextBookInvent, TextBook

# Register your models here.
admin.site.register(TextBookInvent)
admin.site.register(TextBook)

class AdminTextBook(admin.ModelAdmin):
	list_display = ('isbn', 'title')