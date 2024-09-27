from django.db import models
from django.contrib.auth.models import User


# Профиль Учителя
class TeacherProfile(models.Model):
    description = models.TextField(blank=True, verbose_name='Желаемое время')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    user = models.OneToOneField(
        User,
        verbose_name='Учитель',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Профиль учителя'  # Наименование в ед ч
        verbose_name_plural = 'Учтеля'  # Наименование в мн ч
        # ordering = ['name']
# Профиль Ученика


class StudentProfile(models.Model):
    # description = models.TextField(blank=True, verbose_name='Желаемое время')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    user = models.OneToOneField(
        User,
        verbose_name='Ученик',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    ncls = models.ForeignKey(
        "nClass",
        verbose_name='Класс',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Профиль ученика'  # Наименование в ед ч
        verbose_name_plural = 'Ученики'  # Наименование в мн ч
        # ordering = ['name']

# Учебный класс


class nClass(models.Model):
    title = models.CharField(max_length=250, verbose_name='Класс')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    Number = models.IntegerField(verbose_name='Численность?', blank=True, null=True)
    isClub = models.BooleanField(verbose_name='Это кружок?', blank=True, null=True)
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    students = models.ManyToManyField(
        StudentProfile,
        verbose_name='Ученик',
        related_name='srudents_in_the_class',
        # on_delete=models.PROTECT,
        # blank=True, null=True, default=None
    )

    class_teacher = models.ForeignKey(
        TeacherProfile,
        verbose_name='Классынй руководитель',
        related_name="class_teacher",
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )

    org = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Класс'  # Наименование в ед ч
        verbose_name_plural = 'Классы'  # Наименование в мн ч
        ordering = ['title']


# Учебный план
class TrainingCalendar(models.Model):
    time_total = models.IntegerField(verbose_name='Всего времени', blank=True)
    time_now = models.IntegerField(verbose_name='Осталось/прошло', blank=True)
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    ncls = models.ForeignKey(
        nClass,
        verbose_name='Класс',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    subj = models.ForeignKey(
        "Subjects",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Предмет'
    )

    org = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    def __str__(self):
        return str(self.ncls)

    class Meta:
        verbose_name = 'Элемент учебного плана'  # Наименование в ед ч
        verbose_name_plural = 'Учебный план'  # Наименование в мн ч
        ordering = ['time_total']


# Кабинеты
class Room(models.Model):
    numb = models.CharField(max_length=250, verbose_name='Номер комнаты')
    countm = models.IntegerField(verbose_name='Вместимость')

    org = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    # Проектор, актовый/спортивный зал
    spec = models.ForeignKey(
        "Specialization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Специализация'
    )

    def __str__(self):
        return str(self.numb)

    class Meta:
        verbose_name = 'Кабинет'  # Наименование в ед ч
        verbose_name_plural = 'Кабинеты'  # Наименование в мн ч
        ordering = ['numb']


# Специализации
class Specialization(models.Model):
    title = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    # subj = models.ForeignKey(
    #     "Organization",
    #     on_delete=models.PROTECT, blank=True, null=True, default=None,
    #     verbose_name='Организация'
    # )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Специализация'  # Наименование в ед ч
        verbose_name_plural = 'Специализации'  # Наименование в мн ч
        ordering = ['title']


# Предметы
class Subjects(models.Model):
    obj = models.Manager()
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    org = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Предмет'  # Наименование в ед ч
        verbose_name_plural = 'Предметы'  # Наименование в мн ч
        ordering = ['title']


# Связи
class Contacts(models.Model):
    type = models.CharField(max_length=250, verbose_name='Тип')
    status = models.CharField(
        max_length=250, blank=True, verbose_name='Статус')

    h1 = models.ForeignKey(
        User,
        verbose_name='От',
        related_name="h_from",
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    h2 = models.ForeignKey(
        User,
        verbose_name='К',
        related_name="h_to",
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        verbose_name = 'Связь'  # Наименование в ед ч
        verbose_name_plural = 'Связи'  # Наименование в мн ч
        ordering = ['type']


# Ррасписание
class Timetable(models.Model):
    # title = models.CharField(max_length=250, verbose_name='Название')
    # description = models.TextField(blank=True, verbose_name='Описание')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    clas = models.ForeignKey(
        nClass,
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    d = models.IntegerField(blank=True, null=True,
                            default=None, verbose_name='День')
    m = models.IntegerField(blank=True, null=True,
                            default=None, verbose_name='Месяц')
    y = models.IntegerField(blank=True, null=True,
                            default=None, verbose_name='Год')
    numb = models.IntegerField(
        blank=True, null=True, default=None, verbose_name='№ Урока')

    subj = models.ForeignKey(
        Subjects,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Предмет'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Кабинет'
    )

    org = models.ForeignKey(
        "Organization",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    teacher = models.ForeignKey(
        User,
        verbose_name='Учитель',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.clas)

    class Meta:
        verbose_name = 'Элемент расписания'  # Наименование в ед ч
        verbose_name_plural = 'Расписание'  # Наименование в мн ч
        # ordering = ['title']


# Организация
class Organization(models.Model):
    title = models.CharField(max_length=50, verbose_name='Организация')
    description = models.TextField(blank=True, verbose_name='Описание')
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)

    ttab = models.ForeignKey(
        "Timetable",
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Организация'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Организация'  # Наименование в ед ч
        verbose_name_plural = 'Организации'  # Наименование в мн ч
        ordering = ['title']

# class User(AbstractUser):
#     pass
