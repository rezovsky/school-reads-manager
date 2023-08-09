from django.db import models

class TextBook(models.Model):
    isbn = models.CharField('ISBN', max_length=20, unique=True)
    title = models.CharField('Название', max_length=50)
    autor = models.CharField('Автор', max_length=30)
    year = models.CharField('Год издания', max_length=4)
    clas = models.CharField('Класс', max_length=5)
    iteration = models.CharField('Номер издание', max_length=3)
    publisher = models.CharField('Издатель', max_length=50)
    date = models.DateTimeField('Дата добавления')

    list_display = ('isbn', 'title')


    def __str__(self):
        return self.isbn

    class Meta:
        verbose_name = 'Учебник'
        verbose_name_plural = "Учебники"

class TextBookInvent(models.Model):
    inv = models.CharField('Инвентарный номер', max_length=10)
    isbn = models.ForeignKey(TextBook, on_delete=models.CASCADE, to_field='isbn')
    date = models.DateTimeField('Дата добавления')

    def __str__(self):
        return self.inv

    class Meta:
        verbose_name = 'Инвентарный номер'
        verbose_name_plural = "Инвентарные номера"

class TextBookArhiv(models.Model):
    inv = models.CharField('Инвентарный номер', max_length=10)
    isbn = models.CharField('ISBN', max_length=20)
    date = models.DateTimeField('Дата добавления')

    def __str__(self):
        return self.inv

    class Meta:
        verbose_name = 'Инвентарный номер'
        verbose_name_plural = "Инвентарные номера"