from django.db import models

from django.db import models


class Reader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    clas = models.PositiveIntegerField()
    class_letter = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.clas}{self.class_letter}"
