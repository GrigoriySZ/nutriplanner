from django.contrib import admin, messages
from django.urls import path
import openpyxl
from django.shortcuts import render, redirect
from .models import Product
from .forms import ExcelInputForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'proteins', 'fats', 'carbs',)
    search_fields = ('name',)
    change_list_template = 'meals/admin/product_change_list.html'

    def get_urls(self):
        """Кастомный url для импорта Excel"""

        urls = super().get_urls()
        custom_url = [
            path('excel-import/', 
                 self.admin_site.admin_view(self.import_excel), 
                 name='product_import'), 
        ]
        return custom_url + urls
    
    def import_excel(self, request):
        if request.method == 'POST':
            form = ExcelInputForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = request.FILES['excel_file']
                try:
                    workbook = openpyxl.load_workbook(excel_file)
                    sheet = workbook.active
                    created_count = 0
                    # Куриное филе (сырое) 165 31,9 3,6 0,0

                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        if not row or not row[0]:
                            continue
                        name = str(row[0]).strip()
                        calories = int(row[1])
                        proteins = float(row[2])
                        fats = float(row[3])
                        carbs = float(row[4])

                        Product.objects.create(
                            name=name,
                            calories=calories, 
                            proteins=proteins, 
                            fats=fats, 
                            carbs=carbs
                        )
                        created_count += 1
                    self.message_user(
                        request,
                        f'Вставлено строк: {created_count}', 
                        messages.SUCCESS
                    )
                    return redirect('admin:meals_product_changelist')
                except Exception: 
                    self.message_user(
                        request,
                        'Ошибка при обработке формы',
                        messages.ERROR
                    )
        else:
            form = ExcelInputForm()

        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'title': 'Импоркт продуктов из Excel',
        }
        return render(request, 'meals/admin/excel_import.html', context)