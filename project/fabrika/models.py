from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from materials.models import Material, ClothModel
from django.utils.timezone import now


# Create your models here.
class EmployeeGroups(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название группы работника')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа работников'
        verbose_name_plural = 'Группы работников'


class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name='ФИО сотрудника')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', region='UZ')
    salary = models.FloatField(default=0, verbose_name='Зарплата')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Фото сотр')
    report = models.TextField(verbose_name='Отчет по зарплате', default='Отчет по зарплате\n', null=True, blank=True)
    group = models.ManyToManyField(EmployeeGroups, null=True, blank=True, verbose_name='Группа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'


class MaterialTaked(models.Model):
    profile = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name='Старший взял',
                                related_name='takedadmin')
    for_model = models.ForeignKey(ClothModel, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='На какую модель товара взял')
    taked_mass = models.FloatField(verbose_name='Взятая масса')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name='Материал')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата взятия')
    remaining_mass = models.FloatField(verbose_name='Оставшийся материал у старшего', blank=True, null=True)

    def __str__(self):
        date = str(self.created_at)
        import re
        r1 = re.search(r'\.\d+', date)[0]
        date = date.replace(r1, '')

        return f'{self.profile.name} - {self.taked_mass} кг / {self.remaining_mass} кг для {self.for_model}  - {self.material.title} - {date}'

    class Meta:
        verbose_name = 'Материал взятый старшим'
        verbose_name_plural = 'Материалы взятые старшими'


class Vyazka(models.Model):
    material = models.ForeignKey(MaterialTaked, on_delete=models.CASCADE, verbose_name='Взятая старшим масса материала')
    mass_taked = models.FloatField(verbose_name='Масса, которую дал старший', default=0)
    mass_finish = models.FloatField(verbose_name='Готовая масса после вязки', blank=True, null=True,
                                    help_text='Заполнить после того, как работник сделал вязку')
    count = models.IntegerField(verbose_name='Количество готовой модели', blank=True, null=True,
                                help_text='Заполнить после того, как работник сделал вязку')
    material_given_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,
                                          verbose_name='Рабочий по вязке', related_name='employees')
    mass_brak = models.FloatField(verbose_name='Масса брака', default=0,
                                  help_text='Заполнить после того, как работник сделал вязку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата передачи материала')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.material} - Партия {self.mass_finish} кг - {self.count} шт'

    class Meta:
        verbose_name = 'Вязка материала'
        verbose_name_plural = 'Распределение на вязку материала'


class ClothProductModel(models.Model):
    material_taked = models.ForeignKey(Vyazka, on_delete=models.CASCADE, verbose_name='Из какой вязки')
    bichuv_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name='Работник Бичув', related_name='bichuv')
    bichuv_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    chok_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                      verbose_name='Работник Чок', related_name='chok')
    chok_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    averlock_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                          verbose_name='Работник Аверлок', related_name='averlock')
    averlock_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    katelniy_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                          verbose_name='Работник Кательни', related_name='katelniy')
    katelniy_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    tugma_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='Работник Тугма', related_name='tugma')
    tugma_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    petlya_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name='Работник Петля', related_name='petlya')
    petlya_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    dazmol_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name='Работник Дазмол', related_name='dazmol')
    dazmol_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    chistka_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                         verbose_name='Работник Чистка', related_name='chistka')
    chistka_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    jemchug_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                         verbose_name='Работник Жемчуг', related_name='jemchug')
    jemchug_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    upakovka_employee = models.ForeignKey(Employee, default=None, null=True, blank=True, on_delete=models.CASCADE,
                                          verbose_name='Работник Упаковка', related_name='upakovka')
    upakovka_count = models.SmallIntegerField(default=0, verbose_name='Кол-во изменении')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата', null=True, blank=True)

    def __str__(self):
        return f'{self.material_taked.material.for_model}'

    class Meta:
        verbose_name = 'Процесс производства'
        verbose_name_plural = 'Процессы производства'


class Product(models.Model):
    product = models.ForeignKey(ClothProductModel, on_delete=models.PROTECT, verbose_name='Товар')
    count = models.IntegerField(default=0, verbose_name='Количество в партии')
    created_at = models.DateTimeField(default=now, editable=False, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.product.material_taked.material.for_model}'

    class Meta:
        verbose_name = 'Готовый товар'
        verbose_name_plural = 'Готовые товары'


class FinalProduction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    product_series = models.CharField(max_length=255, verbose_name='Серия продукта')
    created_at = models.DateTimeField(default=now, editable=False, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'Готовый товар'
        verbose_name_plural = 'Готовые товары'


class Clients(models.Model):
    client_name = models.CharField(max_length=255, verbose_name='Имя Фамилия')
    client_balance = models.FloatField(verbose_name='Баланс клиента')
    client_number = PhoneNumberField(verbose_name='Номер телефона', region='UZ', default=None, null=True)
    client_product = models.ForeignKey(ClothModel, on_delete=models.SET_NULL, null=True,
                                       verbose_name='Заказанная модель товара')
    client_quantity = models.IntegerField(default=0, verbose_name='Количество заказа')
    client_status = models.BooleanField(default=False, verbose_name='Статус готовности')

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'База клиентов'


class OldReport(models.Model):
    text = models.TextField(default=0, verbose_name='Текст отчетов')


class NewReport(models.Model):
    text = models.TextField(default=0, verbose_name='Текст отчетов')

class Brak(models.Model):
    vyazka = models.ForeignKey(Vyazka, on_delete=models.CASCADE, null=True, blank=True)
    mass_brak = models.FloatField(verbose_name='Масса брака', default=0,
                                  help_text='Заполнить после того, как работник сделал вязку')
    sum_shtraf = models.FloatField(verbose_name='Сумма штрафа')
    status = models.BooleanField(default=False, verbose_name='Починил ли брак')
    count_edit = models.IntegerField(default=0, verbose_name='Кол-во изменений')

    def __str__(self):
        return f'{self.vyazka.material_given_to} - {self.sum_shtraf}'

    class Meta:
        verbose_name = 'Брак'
        verbose_name_plural = 'Таблица брака'

