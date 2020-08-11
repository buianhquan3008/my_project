# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Book, Category

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
