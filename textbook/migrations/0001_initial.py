# Generated by Django 4.1.5 on 2023-02-09 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=20, verbose_name='ISBN')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('autor', models.CharField(max_length=30, verbose_name='Автор')),
                ('year', models.CharField(max_length=4, verbose_name='Год издания')),
                ('clas', models.CharField(max_length=5, verbose_name='Класс')),
                ('iteration', models.CharField(max_length=3, verbose_name='Номер издание')),
                ('publisher', models.CharField(max_length=50, verbose_name='Издатель')),
                ('date', models.DateTimeField(verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Учебник',
                'verbose_name_plural': 'Учебники',
            },
        ),
        migrations.CreateModel(
            name='TextBookInvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv', models.CharField(max_length=10, verbose_name='Инвентарный номер')),
                ('isbn', models.CharField(max_length=20, verbose_name='ISBN')),
                ('date', models.DateTimeField(verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Инвентарный номер',
                'verbose_name_plural': 'Инвентарные номера',
            },
        ),
    ]