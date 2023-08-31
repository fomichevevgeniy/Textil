# Generated by Django 4.1.1 on 2022-10-18 14:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fabrika', '0016_newreport_oldreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fabrika.clothproductmodel', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Готовый товар',
                'verbose_name_plural': 'Готовые товары',
            },
        ),
        migrations.AlterField(
            model_name='finalproduction',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fabrika.product', verbose_name='Товар'),
        ),
    ]
