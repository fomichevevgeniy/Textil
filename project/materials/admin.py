from django.contrib import admin
from django.utils.html import format_html

from .models import *
# Register your models here.
from django.contrib.auth.models import User, Group

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'firm', 'color', 'mass', 'type']
    list_editable = ['mass']

class ClothAdmin(admin.ModelAdmin):
    list_display = ['list_display_material_taked', 'material']
    readonly_fields = ('list_display_material_taked',)
    css = {
        'all': ("css/admin.css",)
    }
    def list_display_material_taked(self, instance):
        return format_html(
            f'''<span class="truncated_address btn btn-secondary" title="
                Модель: {instance.title}

    Бичув: {'Да' if instance.bichuv else 'Нет'} - {instance.price_bichuv} сум за шт,
    Чок: {'Да' if instance.chok else 'Нет'} - {instance.price_chok} сум за шт,
    Аверлок: {'Да' if instance.averlock else 'Нет'} - {instance.price_averlock} сум за шт,
    Кательная: {'Да' if instance.katelniy else 'Нет'} - {instance.price_katelniy} сум за шт,
    Тугма: {'Да' if instance.tugma else 'Нет'} - {instance.price_tugma} сум за шт,
    Петли: {'Да' if instance.petlya else 'Нет'} - {instance.price_petlya} сум за шт,
    Дазмол: {'Да' if instance.dazmol else 'Нет'} - {instance.price_dazmol} сум за шт,
    Чистка: {'Да' if instance.chistka else 'Нет'} - {instance.price_chistka} сум за шт,
    Жемчуг: {'Да' if instance.jemchug else 'Нет'} - {instance.price_jemchug} сум за шт,
    Упаковка: {'Да' if instance.upakovka else 'Нет'} - {instance.price_upakovka} сум за шт,
    ">{instance.title}</span>'''
        )

    list_display_material_taked.short_description = 'Название продукта'


admin.site.register(ClothModel, ClothAdmin)
admin.site.register(Type)
admin.site.register(Colors)

admin.site.register(Material, MaterialAdmin)