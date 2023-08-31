from django.db import models

# Create your models here.
class Colors(models.Model):
    title = models.CharField(max_length=255, verbose_name='Цвет')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Таблица цветов материалов'


class Type(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тип материала')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы материалов'


class Material(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название нити', default='Название')
    firm = models.CharField(max_length=255, verbose_name='Фирма производитель')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, verbose_name='Цвет', related_name='colors')
    mass = models.FloatField(verbose_name='Масса на складе (кг)')
    type = models.ForeignKey(Type, verbose_name='Тип материала', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.firm} - {self.type}'

    class Meta:
        verbose_name = 'Таблица материалов нитей'
        verbose_name_plural = 'Таблица материалов нитей'


class ClothModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название продукта')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Из какого материала сделан')

    price_vyazka =  models.FloatField(default=0, verbose_name='Цена за Вязку')
    bichuv = models.BooleanField(default=False, verbose_name='Бичув - выкройка')
    price_bichuv =  models.FloatField(default=0, verbose_name='Цена за бичув')
    chok = models.BooleanField(default=False, verbose_name='Чок')
    price_chok = models.FloatField(default=0, verbose_name='Цена за Чок')
    averlock = models.BooleanField(default=False, verbose_name='Аверлок')
    price_averlock = models.FloatField(default=0, verbose_name='Цена за Аверлок')
    katelniy = models.BooleanField(default=False, verbose_name='Кательная')
    price_katelniy = models.FloatField(default=0, verbose_name='Цена за Кательная')
    tugma = models.BooleanField(default=False, verbose_name='Тугма - Пуговицы')
    price_tugma = models.FloatField(default=0, verbose_name='Цена за Тугма')
    petlya = models.BooleanField(default=False, verbose_name='Петли')
    price_petlya = models.FloatField(default=0, verbose_name='Цена за Петли')
    dazmol = models.BooleanField(default=False, verbose_name='Дазмол - Утюг')
    price_dazmol = models.FloatField(default=0, verbose_name='Цена за Дазмол')
    chistka = models.BooleanField(default=False, verbose_name='Чистка')
    price_chistka = models.FloatField(default=0, verbose_name='Цена за Чистка')
    jemchug = models.BooleanField(default=False, verbose_name='Жемчуг')
    price_jemchug = models.FloatField(default=0, verbose_name='Цена за Жемчуг')
    upakovka = models.BooleanField(default=False, verbose_name='Упаковка')
    price_upakovka = models.FloatField(default=0, verbose_name='Цена за Упаковка')


#     def __str__(self):
#         return f"""{self.title}\n
# Бичув - выкройка - {'Да' if self.bichuv else 'Нет'}"""
    def __str__(self):
        return f"""{self.title}"""

    class Meta:
        verbose_name = 'Модель одежды'
        verbose_name_plural = 'Модели одежды'
