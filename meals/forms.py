from django import forms

class ExcelInputForm(forms.Form):
    excel_file = forms.FileField(
        label='Выберите excel файл для загрузки',
        help_text='Файл должен содержать столбцы: Название, Калории, Белки, Жиры, Углеводы'
    )