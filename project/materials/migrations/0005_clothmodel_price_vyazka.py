# Generated by Django 4.1.1 on 2022-09-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_rename_tutma_clothmodel_tugma_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothmodel',
            name='price_vyazka',
            field=models.FloatField(default=0, verbose_name='Цена за Вязку'),
        ),
    ]
