from django import forms

class ExcelInputForm(forms.Form):
    ecxel_file = forms.FileField(
        label='Выберите excel файл для загрузки',
        help_text='Файл должен содержать столбцы: Название, Калории, Белки, Жиры, Углеводы'
    )