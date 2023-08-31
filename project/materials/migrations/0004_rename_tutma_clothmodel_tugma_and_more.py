# Generated by Django 4.1.1 on 2022-09-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_alter_material_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothmodel',
            old_name='tutma',
            new_name='tugma',
        ),
        migrations.RemoveField(
            model_name='clothmodel',
            name='description',
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_averlock',
            field=models.FloatField(default=0, verbose_name='Цена за Аверлок'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_bichuv',
            field=models.FloatField(default=0, verbose_name='Цена за бичув'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_chistka',
            field=models.FloatField(default=0, verbose_name='Цена за Чистка'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_chok',
            field=models.FloatField(default=0, verbose_name='Цена за Чок'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_dazmol',
            field=models.FloatField(default=0, verbose_name='Цена за Дазмол'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_jemchug',
            field=models.FloatField(default=0, verbose_name='Цена за Жемчуг'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_katelniy',
            field=models.FloatField(default=0, verbose_name='Цена за Кательная'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_petlya',
            field=models.FloatField(default=0, verbose_name='Цена за Петли'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_tugma',
            field=models.FloatField(default=0, verbose_name='Цена за Тугма'),
        ),
        migrations.AddField(
            model_name='clothmodel',
            name='price_upakovka',
            field=models.FloatField(default=0, verbose_name='Цена за Упаковка'),
        ),
    ]
