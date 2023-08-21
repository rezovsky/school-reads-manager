from django.db import models
from django.utils import timezone

from textbook.models import TextBookInvent


class Reader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    clas = models.PositiveIntegerField()
    class_letter = models.CharField(max_length=1)
    date = models.DateTimeField('Дата добавления', default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.clas}{self.class_letter}"


class BorrowedBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    textbook = models.ForeignKey(TextBookInvent, on_delete=models.CASCADE)
    date = models.DateTimeField('Дата добавления', default=timezone.now)

    def __str__(self):
        return f"{self.reader} - {self.textbook} ({self.date})"
