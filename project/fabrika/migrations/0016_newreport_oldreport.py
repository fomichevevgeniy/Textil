# Generated by Django 4.1.1 on 2022-10-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fabrika', '0015_clients_client_quantity_clients_client_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default=0, verbose_name='Текст отчетов')),
            ],
        ),
        migrations.CreateModel(
            name='OldReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default=0, verbose_name='Текст отчетов')),
            ],
        ),
    ]
