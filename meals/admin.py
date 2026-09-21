from django.contrib import admin, messages
import openpyxl
from django.shortcuts import render, redirect
from .models import Product
from .forms import ExcelInputForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'proteins', 'fats', 'carbs',)
    search_fields = ('name',)
    change_list_template = 'meals/admin/product_change_list.html'