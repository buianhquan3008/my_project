# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên thể loại')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')

    def __str__(self):
        return self.name if self.name else '-'

    class Meta:
        db_table = 'd_book_category'
        verbose_name = "Thể loại"
        verbose_name_plural = "Thể loại"


class Book(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên sách')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Thể loại')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tác giả')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')

    def __str__(self):
        return self.name if self.name else '-'

    class Meta:
        db_table = 'd_book'
        verbose_name = "Sách"
        verbose_name_plural = "Sách"


class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()


class DataPoint(models.Model):
    label = models.CharField(max_length=50)
    x_coordinate = models.SmallIntegerField()
    y_coordinate = models.SmallIntegerField()
