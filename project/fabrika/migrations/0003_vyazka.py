# Generated by Django 4.1.1 on 2022-09-18 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fabrika', '0002_alter_employee_options_materialtaked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vyazka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mass_taked', models.FloatField(default=0, verbose_name='Масса, которую дал старший')),
                ('mass_finish', models.FloatField(blank=True, null=True, verbose_name='Готовая масса после вязки')),
                ('count', models.IntegerField(blank=True, null=True, verbose_name='Количество готовой модели')),
                ('mass_brak', models.FloatField(default=0, verbose_name='Масса брака')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата передачи материала')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabrika.materialtaked', verbose_name='Взятая старшим масса материала')),
                ('material_given_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='fabrika.employee', verbose_name='Рабочий по вязке')),
            ],
            options={
                'verbose_name': 'Вязка метериала',
                'verbose_name_plural': 'Вязка метериала',
            },
        ),
    ]
