from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.html import format_html
from .models import *






# Сигнал для проверки перед сохранением новых данных Взятия старшим
@receiver(pre_save, sender=MaterialTaked)  # Ждём сигнала, что в базе произошли изменения
def on_material_taked(sender, instance: MaterialTaked, **kwargs):
    if instance.pk is None:  # Проверяем, что в базе отсутвует новый объект
        if instance.material.mass >= instance.taked_mass:
            instance.material.mass -= instance.taked_mass  # Изменяем массу
            instance.material.save()  # Сохраняем

            text = f'''Старший: {instance.profile}
Взял: {instance.taked_mass} кг
Со склада: {instance.material}
Для модели: {instance.for_model}
'''
            report = OldReport()
            report.text = text
            report.save()
        else:
            # Если материала на складе меньше отправляем ошибку
            raise Exception('Нельзя взять больше чем есть на складе')


@receiver(pre_save, sender=Vyazka)
def on_material_given(sender, instance: Vyazka, **kwargs):
    if instance.pk is None:
        if instance.material.remaining_mass >= instance.mass_taked:
            instance.material.remaining_mass -= instance.mass_taked
            instance.material.save()
            text = f'''Старший отдал на вязку: {instance.material}
Работнику: {instance.material_given_to}
Массу: {instance.mass_taked}
'''
            report = OldReport()
            report.text = text
            report.save()

        else:
            raise Exception('Пытаемся взять больше чем взял старший')


@receiver(pre_save, sender=Vyazka)
def on_material_given_finished(sender, instance: Vyazka, **kwargs):
    if instance.pk is not None:
        if instance.count > 0:
            print(instance.material.for_model.price_vyazka)
            salary = instance.material.for_model.price_vyazka * instance.count
            instance.material_given_to.salary += salary
            print(instance.material_given_to)

            text = f'''
За вязку {instance} - {instance.count} шт по цене {instance.material.for_model.price_vyazka} - {salary}
'''
            if instance.mass_brak > 0:
                shtraf = instance.mass_brak * 100000
                instance.material_given_to.salary -= shtraf
                text += f'За брак {instance} - {instance.mass_brak} штраф {shtraf} сум'
                brak = Brak.objects.create(vyazka = instance,
                                           mass_brak = instance.mass_brak,
                                           sum_shtraf = shtraf)
                brak.save()
            else:
                shtraf = 0
            bot_text = f'''Работник: {instance.material_given_to}
Закончил вязку: {instance.material}
Получил: {instance.mass_taked} кг
Готовая масса: {instance.mass_finish} кг
Брак: {instance.mass_brak} кг
Готовых штук: {instance.count}
За брак {instance} - {instance.mass_brak} штраф {shtraf} сум
За вязку {instance} - {instance.count} шт 
по цене {instance.material.for_model.price_vyazka} - 
{salary} сум

'''
            report = OldReport()
            report.text = bot_text
            report.save()
            print(instance.material_given_to.report)
            instance.material_given_to.report += text
            instance.material_given_to.save()


@receiver(pre_save, sender=ClothProductModel)
def on_cloth_bichuv_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.bichuv_employee is not None:
            if instance.bichuv_count == 0:
                salary = instance.material_taked.material.for_model.price_bichuv * instance.material_taked.count
                instance.bichuv_employee.salary += salary
                print(instance.bichuv_employee)
                text = f'''
За бичув {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_bichuv} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.bichuv_employee}
За бичув {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_bichuv} - 
{salary} сум
                '''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.bichuv_employee.report += text
                instance.bichuv_count += 1
                instance.bichuv_employee.save()
                instance.save()


@receiver(pre_save, sender=ClothProductModel)
def on_cloth_chok_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.chok_employee is not None:
            if instance.chok_count == 0:
                salary = instance.material_taked.material.for_model.price_chok * instance.material_taked.count
                instance.chok_employee.salary += salary
                print(instance.chok_employee)
                text = f'''
За чок {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_chok} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.chok_employee}
За чок {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_chok} - {salary} сум
'''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.chok_employee.report += text
                instance.chok_count += 1
                instance.chok_employee.save()
                instance.save()

@receiver(pre_save, sender=ClothProductModel)
def on_cloth_averlock_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.averlock_employee is not None:
            if instance.averlock_count == 0:
                salary = instance.material_taked.material.for_model.price_averlock * instance.material_taked.count
                instance.averlock_employee.salary += salary
                print(instance.averlock_employee)
                text = f'''
За аверлок {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_averlock} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.averlock_employee}
За аверлок {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_averlock} - {salary} сум
                '''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.averlock_employee.report += text
                instance.averlock_count += 1
                instance.averlock_employee.save()
                instance.save()

@receiver(pre_save, sender=ClothProductModel)
def on_cloth_katelniy_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.katelniy_employee is not None:
            if instance.katelniy_count == 0:
                salary = instance.material_taked.material.for_model.price_katelniy * instance.material_taked.count
                instance.katelniy_employee.salary += salary
                print(instance.katelniy_employee)
                text = f'''
За кательный {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_katelniy} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.katelniy_employee}
За кательный {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_katelniy} - {salary} сум
'''
                report = OldReport()
                report.text = bot_text
                report.save()

                instance.katelniy_employee.report += text
                instance.katelniy_count += 1
                instance.katelniy_employee.save()
                instance.save()


@receiver(pre_save, sender=ClothProductModel)
def on_cloth_tugma_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.tugma_employee is not None:
            if instance.tugma_count == 0:
                salary = instance.material_taked.material.for_model.price_tugma * instance.material_taked.count
                instance.tugma_employee.salary += salary
                print(instance.tugma_employee)
                text = f'''
За тугма {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_tugma} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.tugma_employee}
За тугма {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_tugma} - {salary} сум
'''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.tugma_employee.report += text
                instance.tugma_count += 1
                instance.tugma_employee.save()
                instance.save()


@receiver(pre_save, sender=ClothProductModel)
def on_cloth_petlya_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.petlya_employee is not None:
            if instance.petlya_count == 0:
                salary = instance.material_taked.material.for_model.price_petlya * instance.material_taked.count
                instance.petlya_employee.salary += salary
                print(instance.petlya_employee)
                text = f'''
За петля {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_petlya} - {salary}
            '''
                bot_text = f'''Работник: {instance.petlya_employee}
За петля {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_petlya} - {salary} сум
'''
                print(text)
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.petlya_employee.report += text
                instance.petlya_count += 1
                instance.petlya_employee.save()
                instance.save()

@receiver(pre_save, sender=ClothProductModel)
def on_cloth_dazmol_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.dazmol_employee is not None:
            if instance.dazmol_count == 0:
                salary = instance.material_taked.material.for_model.price_dazmol * instance.material_taked.count
                instance.dazmol_employee.salary += salary
                print(instance.dazmol_employee)
                text = f'''
За дазмол {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_dazmol} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.dazmol_employee}
За дазмол {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_dazmol} - {salary} сум
'''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.dazmol_employee.report += text
                instance.dazmol_count += 1
                instance.dazmol_employee.save()
                instance.save()

@receiver(pre_save, sender=ClothProductModel)
def on_cloth_chistka_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.chistka_employee is not None:
            if instance.chistka_count == 0:
                salary = instance.material_taked.material.for_model.price_chistka * instance.material_taked.count
                instance.chistka_employee.salary += salary
                print(instance.chistka_employee)
                text = f'''
За чистка {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_chistka} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.chistka_employee}
За чистка {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_chistka} - {salary} сум
'''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.chistka_employee.report += text
                instance.chistka_count += 1
                instance.chistka_employee.save()
                instance.save()


@receiver(pre_save, sender=ClothProductModel)
def on_cloth_jemchug_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.jemchug_employee is not None:
            if instance.jemchug_count == 0:
                salary = instance.material_taked.material.for_model.price_jemchug * instance.material_taked.count
                instance.jemchug_employee.salary += salary
                print(instance.jemchug_employee)
                text = f'''
За жемчуг {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_jemchug} - {salary}
            '''
                bot_text = f'''Работник: {instance.jemchug_employee}
За жемчуг {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_jemchug} - {salary} сум
'''
                print(text)
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.jemchug_employee.report += text
                instance.jemchug_count += 1
                instance.jemchug_employee.save()
                instance.save()

@receiver(pre_save, sender=ClothProductModel)
def on_cloth_upakovka_employee(sender, instance: ClothProductModel, **kwargs):
    if instance.pk is not None:
        if instance.upakovka_employee is not None:
            if instance.upakovka_count == 0:
                salary = instance.material_taked.material.for_model.price_upakovka * instance.material_taked.count
                instance.upakovka_employee.salary += salary
                print(instance.upakovka_employee)
                text = f'''
За упаковка {instance} - {instance.material_taked.count} шт по цене {instance.material_taked.material.for_model.price_upakovka} - {salary}
            '''
                print(text)
                bot_text = f'''Работник: {instance.upakovka_employee}
За упаковка {instance} - 
{instance.material_taked.count} шт по цене 
{instance.material_taked.material.for_model.price_upakovka} - {salary} сум
                '''
                report = OldReport()
                report.text = bot_text
                report.save()
                instance.upakovka_employee.report += text
                instance.upakovka_count += 1
                instance.upakovka_employee.save()
                instance.save()


@receiver(post_save, sender=Brak,  dispatch_uid="fuck")
def brak2_save(sender, instance: Brak, created, **kwargs):
    if not created:
        if instance.status is True and instance.count_edit < 1:
            print(instance.vyazka.material_given_to.salary)
            instance.vyazka.material_given_to.salary += instance.sum_shtraf
            text = f'''Отработал брак на сумму {instance.sum_shtraf}'''
            print(text)
            instance.vyazka.material_given_to.report += text
            print(instance.vyazka.material.material.mass)
            instance.vyazka.material.material.mass += instance.mass_brak
            instance.vyazka.material.material.save()
            instance.vyazka.material_given_to.save()
            instance.count_edit += 1
            instance.save()
