# Generated by Django 4.1.1 on 2022-09-18 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Таблица цветов материалов',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Тип материала')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы материалов',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Название', max_length=255, verbose_name='Название нити')),
                ('firm', models.CharField(max_length=255, verbose_name='Фирма производитель')),
                ('mass', models.FloatField(verbose_name='Масса на складе (кг)')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='materials.colors', verbose_name='Цвет')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.type', verbose_name='Тип материала')),
            ],
            options={
                'verbose_name': 'Нить',
                'verbose_name_plural': 'Таблица нитей',
            },
        ),
        migrations.CreateModel(
            name='ClothModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('description', models.TextField(verbose_name='Описание продукта')),
                ('bichuv', models.BooleanField(default=False, verbose_name='Бичув - выкройка')),
                ('chok', models.BooleanField(default=False, verbose_name='Чок')),
                ('averlock', models.BooleanField(default=False, verbose_name='Аверлок')),
                ('katelniy', models.BooleanField(default=False, verbose_name='Кательная')),
                ('tutma', models.BooleanField(default=False, verbose_name='Тугма - Пуговицы')),
                ('petlya', models.BooleanField(default=False, verbose_name='Петли')),
                ('dazmol', models.BooleanField(default=False, verbose_name='Дазмол - Утюг')),
                ('chistka', models.BooleanField(default=False, verbose_name='Чистка')),
                ('jemchug', models.BooleanField(default=False, verbose_name='Жемчуг')),
                ('upakovka', models.BooleanField(default=False, verbose_name='Упаковка')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.material', verbose_name='Из какого материала сделан')),
            ],
        ),
    ]
