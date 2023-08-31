from django.contrib import admin
from django.http import HttpResponseRedirect
import openpyxl
from .models import *
from django.contrib import messages
from django.utils.html import format_html
from .forms import DropdownModelForm
from openpyxl import load_workbook, Workbook


# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'salary']
    #readonly_fields = ['report']

class MaterialTakedAdmin(admin.ModelAdmin):
    list_display = ['profile', 'taked_mass', 'material', 'remaining_mass', 'for_model', 'created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        profile = EmployeeGroups.objects.get(title='Старший по вязке')
        if db_field.name == 'profile':
            kwargs['queryset'] = Employee.objects.filter(group=profile)
            print(kwargs['queryset'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Удаление стандартного сообщения о создании
    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def save_model(self, request, obj, form, change):
        try:
            obj.remaining_mass = obj.taked_mass
            return super().save_model(request, obj, form, change)
        except Exception as e:
            print(e)
            msg = f'На складе меньше, чем хочет взять старший. На складе {obj.material.mass} кг, а старший пытался взять {obj.taked_mass} кг'
            messages.add_message(request, messages.ERROR, msg)

    # if obj.material.mass >= obj.taked_mass:
    #     obj.material.mass -= obj.taked_mass
    #     obj.material.save()
    #     messages.add_message(request, messages.SUCCESS, f'Старший взял {obj.taked_mass}')
    #     return super().save_model(request, obj, form, change)
    # else:
    #     messages.add_message(request, messages.ERROR, f'На складе меньше, чем хочет взять старший')
    #     return super().save_model(request, obj, form, change)


class VyazkaAdmin(admin.ModelAdmin):
    list_display = ['material_given_to', 'mass_taked', 'mass_finish', 'mass_brak', 'count', 'created_at',
                    'updated_at']
    #list_editable = ['mass_finish', 'count', 'mass_brak']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        material_given_to = EmployeeGroups.objects.get(title='Вязка')
        if db_field.name == 'material_given_to':
            kwargs['queryset'] = Employee.objects.filter(group=material_given_to)
            print(kwargs['queryset'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def save_model(self, request, obj, form, change):
        try:
            return super().save_model(request, obj, form, change)
        except Exception as e:
            print(e)
            msg = f'Нельзя дать больше чем осталось у старшего. У старшего: {obj.material.remaining_mass} кг, а рабочему пытались дать {obj.mass_taked} кг'
            messages.add_message(request, messages.ERROR, msg)


class ClothProductModelAdmin(admin.ModelAdmin):
    css = {
        'all': ("css/admin.css",)
    }

    list_display = ['list_display_material_taked', 'show_partiya_quantity', ]
    change_form_template = "admin/excel_export.html"
    # fieldsets = (
    #     ('Выбор вязки', {
    #         'fields': ('material_taked',),
    #         'classes': ('predefined',)
    #     }),
    #     (None, {
    #         'fields': (
    #             ('show_main_information'),
    #             ('bichuv_employee', 'show_price_bichuv'),
    #             ('chok_employee', 'show_price_chok'),
    #             ('averlock_employee', 'show_price_averlock'),
    #             ('katelniy_employee', 'show_price_katelniy'),
    #             ('tugma_employee', 'show_price_tugma'),
    #             ('petlya_employee', 'show_price_petlya'),
    #             ('dazmol_employee', 'show_price_dazmol'),
    #             ('chistka_employee', 'show_price_chistka'),
    #             ('jemchug_employee', 'show_price_jemchug'),
    #             ('upakovka_employee', 'show_price_upakovka')
    #         ),
    #         'classes': ('abcdefg',)
    #     })
    # )
    # form = DropdownModelForm
    fields = ('material_taked',
              ('show_main_information'),
              ('bichuv_employee', 'show_price_bichuv'),
              ('chok_employee', 'show_price_chok'),
              ('averlock_employee', 'show_price_averlock'),
              ('katelniy_employee', 'show_price_katelniy'),
              ('tugma_employee', 'show_price_tugma'),
              ('petlya_employee', 'show_price_petlya'),
              ('dazmol_employee', 'show_price_dazmol'),
              ('chistka_employee', 'show_price_chistka'),
              ('jemchug_employee', 'show_price_jemchug'),
              ('upakovka_employee', 'show_price_upakovka')
              )
    readonly_fields = ('show_main_information',
                       'show_price_bichuv',
                       'show_price_chok',
                       'show_price_averlock',
                       'show_price_katelniy',
                       'show_price_tugma',
                       'show_price_petlya',
                       'show_price_dazmol',
                       'show_price_chistka',
                       'show_price_jemchug',
                       'show_price_upakovka')

    # def get_exclude(self, request, obj=None):
    #     lst = []
    #     if not obj.material_taked.material.for_model.bichuv:
    #         lst.append('bichuv_employee')
    #     return lst
    def get_form(self, request, obj=None, **kwargs):
        form = super(ClothProductModelAdmin, self).get_form(request, obj, **kwargs)
        if obj.material_taked.material.for_model.bichuv:
            del form.base_fields['bichuv_employee']
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        bichuv_group = EmployeeGroups.objects.get(title='Бичув')
        katelniy_group = EmployeeGroups.objects.get(title='Кательня')
        chok_group = EmployeeGroups.objects.get(title='Чок')
        averlock_group = EmployeeGroups.objects.get(title='Аверлок')
        tugma_group = EmployeeGroups.objects.get(title='Тугма')
        petlya_group = EmployeeGroups.objects.get(title='Петля')
        dazmol_group = EmployeeGroups.objects.get(title='Дазмол')
        chistka_group = EmployeeGroups.objects.get(title='Чистка')
        jemchug_group = EmployeeGroups.objects.get(title='Жемчуг')
        upakovka_group = EmployeeGroups.objects.get(title='Упаковка')

        if db_field.name == 'bichuv_employee':
            kwargs['queryset'] = Employee.objects.filter(group=bichuv_group)
            print(kwargs['queryset'])
        if db_field.name == 'chok_employee':
            kwargs['queryset'] = Employee.objects.filter(group=chok_group)
            print(kwargs['queryset'])
        if db_field.name == 'katelniy_employee':
            kwargs['queryset'] = Employee.objects.filter(group=katelniy_group)
            print(kwargs['queryset'])
        if db_field.name == 'averlock_employee':
            kwargs['queryset'] = Employee.objects.filter(group=averlock_group)
            print(kwargs['queryset'])
        if db_field.name == 'tugma_employee':
            kwargs['queryset'] = Employee.objects.filter(group=tugma_group)
            print(kwargs['queryset'])
        if db_field.name == 'petlya_employee':
            kwargs['queryset'] = Employee.objects.filter(group=petlya_group)
            print(kwargs['queryset'])
        if db_field.name == 'dazmol_employee':
            kwargs['queryset'] = Employee.objects.filter(group=dazmol_group)
            print(kwargs['queryset'])
        if db_field.name == 'chistka_employee':
            kwargs['queryset'] = Employee.objects.filter(group=chistka_group)
            print(kwargs['queryset'])
        if db_field.name == 'jemchug_employee':
            kwargs['queryset'] = Employee.objects.filter(group=jemchug_group)
            print(kwargs['queryset'])
        if db_field.name == 'upakovka_employee':
            kwargs['queryset'] = Employee.objects.filter(group=upakovka_group)
            print(kwargs['queryset'])

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def list_display_material_taked(self, instance):
        return format_html(
            f'''<span truncated_address" title="
            Модель: {instance.material_taked.material.for_model}
            
Бичув: {'Да' if instance.material_taked.material.for_model.bichuv else 'Нет'} - {instance.material_taked.material.for_model.price_bichuv} сум за шт,
Чок: {'Да' if instance.material_taked.material.for_model.chok else 'Нет'} - {instance.material_taked.material.for_model.price_chok} сум за шт,
Аверлок: {'Да' if instance.material_taked.material.for_model.averlock else 'Нет'} - {instance.material_taked.material.for_model.price_averlock} сум за шт,
Кательная: {'Да' if instance.material_taked.material.for_model.katelniy else 'Нет'} - {instance.material_taked.material.for_model.price_katelniy} сум за шт,
Тугма: {'Да' if instance.material_taked.material.for_model.tugma else 'Нет'} - {instance.material_taked.material.for_model.price_tugma} сум за шт,
Петли: {'Да' if instance.material_taked.material.for_model.petlya else 'Нет'} - {instance.material_taked.material.for_model.price_petlya} сум за шт,
Дазмол: {'Да' if instance.material_taked.material.for_model.dazmol else 'Нет'} - {instance.material_taked.material.for_model.price_dazmol} сум за шт,
Чистка: {'Да' if instance.material_taked.material.for_model.chistka else 'Нет'} - {instance.material_taked.material.for_model.price_chistka} сум за шт,
Жемчуг: {'Да' if instance.material_taked.material.for_model.jemchug else 'Нет'} - {instance.material_taked.material.for_model.price_jemchug} сум за шт,
Упаковка: {'Да' if instance.material_taked.material.for_model.upakovka else 'Нет'} - {instance.material_taked.material.for_model.price_upakovka} сум за шт,
{instance.material_taked}">{instance.material_taked.material.for_model}</span>'''
        )

    def show_main_information(self, obj):
        if obj.material_taked:
            name = obj.material_taked.material.for_model.title
            material = obj.material_taked.material.for_model.material.title
            firm = obj.material_taked.material.for_model.material.firm
            color = obj.material_taked.material.for_model.material.color
            quantity = obj.material_taked.count
            return f'''Название товара: {name}
Название материала материала: {material}
Фирма производитель материала: {firm}
Цвет материала: {color}
Принятое кол-во продукции после вязки: {quantity}

Выполнять сохранение по очереди по мере готовности'''

    def show_partiya_quantity(self, obj):
        if obj.material_taked:
            mass_finish = obj.material_taked.mass_finish
            return mass_finish

    def show_price_bichuv(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_bichuv
            return str(price) + ' сум'

    def show_price_chok(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_bichuv
            return str(price) + ' сум'

    def show_price_averlock(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_averlock
            return str(price) + ' сум'

    def show_price_katelniy(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_katelniy
            return str(price) + ' сум'

    def show_price_tugma(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_tugma
            return str(price) + ' сум'

    def show_price_petlya(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_petlya
            return str(price) + ' сум'

    def show_price_dazmol(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_dazmol
            return str(price) + ' сум'

    def show_price_chistka(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_chistka
            return str(price) + ' сум'

    def show_price_jemchug(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_jemchug
            return str(price) + ' сум'

    def show_price_upakovka(self, obj):
        if obj.material_taked:
            price = obj.material_taked.material.for_model.price_upakovka
            return str(price) + ' сум'

    def response_change(self, request, obj):
        if '_excel_export' in request.POST:
            try:
                wb = load_workbook(filename='../test.xlsx')
                sheet_ranges = wb['Лист1']
                sheet_ranges['A2'].value = obj.pk
                sheet_ranges['B2'].value = obj.created_at
                sheet_ranges['C2'].value = str(obj.material_taked.material.for_model)
                sheet_ranges['D2'].value = str(obj.material_taked.count)
                sheet_ranges['E2'].value = str(obj.material_taked.material_given_to)
                sheet_ranges['F2'].value = str(obj.bichuv_employee.name)
                sheet_ranges['G2'].value = str(obj.chok_employee.name)
                sheet_ranges['H2'].value = str(obj.averlock_employee.name)
                sheet_ranges['I2'].value = str(obj.katelniy_employee.name)
                sheet_ranges['J2'].value = str(obj.tugma_employee.name)
                sheet_ranges['K2'].value = str(obj.petlya_employee.name)
                sheet_ranges['L2'].value = str(obj.dazmol_employee.name)
                sheet_ranges['M2'].value = str(obj.chistka_employee.name)
                sheet_ranges['N2'].value = str(obj.jemchug_employee.name)
                sheet_ranges['O2'].value = str(obj.upakovka_employee.name)
                date = str(obj.created_at)[:19].replace(':', '-')
                wb.save(filename=f'../chek_{date}.xlsx')
                return HttpResponseRedirect(".")
            except:
                msg = f'Не все поля заполнены'
                messages.add_message(request, messages.ERROR, msg)
        if '_final_products' in request.POST:

            product = Product.objects.create(product=obj, count=obj.material_taked.count)
            product.save()
            for i in range(obj.material_taked.count):
                final_product = FinalProduction.objects.create(product=product)
                final_product.product_series = f'{obj.pk}-{final_product.pk}'
                final_product.save()

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


    show_main_information.short_description = 'Основная информация'
    show_price_bichuv.short_description = 'Бичув цена за шт'
    show_price_chok.short_description = 'Чок цена за шт'
    show_price_averlock.short_description = 'Аверлок цена за шт'
    show_price_katelniy.short_description = 'Кательня цена за шт'
    show_price_petlya.short_description = 'Петля цена за шт'
    show_price_dazmol.short_description = 'Дазмол цена за шт'
    show_price_chistka.short_description = 'Чистка цена за шт'
    show_price_jemchug.short_description = 'Жемчуг цена за шт'
    show_price_upakovka.short_description = 'Упаковка цена за шт'


class FinalProductAdmin(admin.TabularInline):
    model = FinalProduction
    fk_name = 'product'
    can_delete = False
    extra = 0


class ProductionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'count', 'created_at']
    list_display_links = ['pk','product']
    inlines = [FinalProductAdmin]


class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_balance', 'client_product']
    list_editable = ['client_balance']

class BrakAdmin(admin.ModelAdmin):
    list_display = ['show_emloyee', 'mass_brak', 'sum_shtraf', 'status']
    list_editable = ['status']

    def show_emloyee(self, obj):
        return obj.vyazka.material_given_to

admin.site.register(Clients, ClientAdmin)
admin.site.register(EmployeeGroups)
admin.site.register(Product, ProductionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Vyazka, VyazkaAdmin)
admin.site.register(Brak, BrakAdmin)
admin.site.register(ClothProductModel, ClothProductModelAdmin)
admin.site.register(MaterialTaked, MaterialTakedAdmin)


'''Создать модель готовых товаров
Создать модель чека'''
