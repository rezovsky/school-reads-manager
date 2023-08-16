from .models import TextBook, TextBookInvent
from django.forms import ModelForm, TextInput, DateTimeInput


class AddTextBookForm(ModelForm):
    class Meta:
        model = TextBook
        fields = ['isbn', 'title', 'autor', 'year', 'clas', 'iteration', 'publisher', 'date']
        widgets = {
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN'
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название учебника'
            }),
            'autor': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор учебника'
            }),
            'year': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год издания'
            }),
            'clas': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Класс'
            }),
            'iteration': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер издания'
            }),
            'publisher': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Издатель'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата внесения'
            }),

        }

class EditTextBookForm(ModelForm):
    class Meta:
        model = TextBook
        fields = ['isbn', 'title', 'autor', 'year', 'clas', 'iteration', 'publisher', 'date']
        widgets = {
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN'
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название учебника'
            }),
            'autor': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор учебника'
            }),
            'year': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год издания'
            }),
            'clas': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Класс'
            }),
            'iteration': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер издания'
            }),
            'publisher': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Издатель'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата изменения'
            }),

        }

class AddTextBookInventForm(ModelForm):
    class Meta:
        model = TextBookInvent
        fields = ['inv', 'isbn', 'date']
        widgets = {
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN'
            }),
            'inv': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Инвентарный номер'
            }),
            'date': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата внесения'
            }),

        }