from django.db import models
from django.contrib.auth.models import User


# Профиль Учителя
class TeacherProfile(models.Model):
    name1 = models.CharField(max_length=250, verbose_name='Фамилия')
    name2 = models.CharField(max_length=250, verbose_name='Имя')
    name3 = models.CharField(max_length=250, verbose_name='Отчество', blank=True)
    time_work = models.CharField(max_length=250, verbose_name='Стаж работы', blank=True, null=True)
    hard_time = models.IntegerField(verbose_name='Занятость', blank=True, null=True)

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = 'Профиль учителя'  # Наименование в ед ч
        verbose_name_plural = 'Учтеля'  # Наименование в мн ч


# Учебный класс
class nClass(models.Model):
    title = models.CharField(max_length=250, verbose_name='Класс')
    isClub = models.BooleanField(verbose_name='Это кружок?', blank=True, null=True)
    digit = models.IntegerField(verbose_name='Цифра', blank=True, null=True)
    
    size = models.IntegerField(verbose_name='Численность', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)


    class_teacher = models.ForeignKey(
        TeacherProfile,
        verbose_name='Классынй руководитель',
        related_name="class_teacher",
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Класс'  # Наименование в ед ч
        verbose_name_plural = 'Классы'  # Наименование в мн ч
        ordering = ['title']


# Специализации
class Specialization(models.Model):
    title = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Специализация'  # Наименование в ед ч
        verbose_name_plural = 'Специализации'  # Наименование в мн ч
        ordering = ['title']


# Кабинеты
class Room(models.Model):
    numb = models.CharField(max_length=250, verbose_name='Номер комнаты')
    count = models.IntegerField(verbose_name='Вместимость')

    # Проектор, актовый/спортивный зал
    spec = models.ManyToManyField(
        "Specialization",
        verbose_name='Специализация',
        blank=True
    )

    def __str__(self):
        return str(self.numb)

    class Meta:
        verbose_name = 'Кабинет'  # Наименование в ед ч
        verbose_name_plural = 'Кабинеты'  # Наименование в мн ч
        ordering = ['numb']


# Предметы
class Subjects(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    spec = models.ManyToManyField(
        Specialization,
        verbose_name='Специализация',
        related_name='spec_for_subjects',
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Предмет'  # Наименование в ед ч
        verbose_name_plural = 'Предметы'  # Наименование в мн ч
        ordering = ['title']


# Какие занятия может проводить учитель
class Teacher_Subjects(models.Model):
    teacher = models.ForeignKey(
        TeacherProfile,
        verbose_name='Учитель',
        # related_name='srudents_in_the_class',
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )
    
    nclass = models.ForeignKey(
        nClass,
        verbose_name='Класс',
        # related_name='srudents_in_the_class',
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )

    subject = models.ForeignKey(
        Subjects,
        verbose_name='Предмет',
        # related_name="class_teacher",
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )

    def __str__(self):
        return str(self.teacher) + " - " + str(self.nclass) + " - " + str(self.subject)

    class Meta:
        verbose_name = 'Занятие учителя'  # Наименование в ед ч
        verbose_name_plural = 'Занятия учителей'  # Наименование в мн ч


# # Курс
# class Corse(models.Model):
#     start_data = models.IntegerField(verbose_name='Дата начала')
#     the_time = models.IntegerField(verbose_name='Продолжительность')
#     title = models.CharField(max_length=250, verbose_name='Название')
#     description = models.TextField(blank=True, verbose_name='Описание')
    
#     def __str__(self):
#         return str(self.title)

#     class Meta:
#         verbose_name = 'Курс'  # Наименование в ед ч
#         verbose_name_plural = 'Курсы'  # Наименование в мн ч
#         ordering = ['title']


# # Занятия курса
# class CourseLesson(models.Model):
#     time_count = models.IntegerField(verbose_name='Кол-во часов')
#     subject = models.ForeignKey(
#         Subjects,
#         verbose_name='Предмет',
#         on_delete=models.PROTECT, blank=True, null=True, default=None
#     )
    
#     ncls = models.ForeignKey(
#         nClass,
#         verbose_name='Класс',
#         on_delete=models.PROTECT, blank=True, null=True, default=None
#     )
    
#     course = models.ManyToManyField(
#         Corse,
#         verbose_name='Курс'
#     )
    
#     def __str__(self):
#         return str(self.subject)

#     class Meta:
#         verbose_name = 'Занятие курса'  # Наименование в ед ч
#         verbose_name_plural = 'Занятия курсов'  # Наименование в мн ч
#         ordering = ['time_count']


# Учебный план
class TrainingCalendar(models.Model):
    time_total = models.IntegerField(verbose_name='Всего времени', blank=True)
    time_now = models.IntegerField(verbose_name='Осталось/прошло', blank=True, null=True)

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

    def __str__(self):
        return str(self.ncls)

    class Meta:
        verbose_name = 'Элемент учебного плана'  # Наименование в ед ч
        verbose_name_plural = 'Учебный план'  # Наименование в мн ч
        ordering = ['time_total']


# Номер урока
class LessonNumber(models.Model):
    number = models.IntegerField(verbose_name='Номер урока')
    time_start = models.CharField(max_length=250, verbose_name='Время начала', blank=True)
    time_end = models.CharField(max_length=250, verbose_name='Время окончания', blank=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Номер урока'  # Наименование в ед ч
        verbose_name_plural = 'Номера уроков'  # Наименование в мн ч
        ordering = ['number']


# Блок времени
class Blok_time(models.Model):
    n_week = models.IntegerField(verbose_name='День недели')
    lesson_number = models.ForeignKey(
        LessonNumber,
        verbose_name='Номер урока',
        related_name="lesson_number",
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )
    
    def __str__(self):
        w = f'Неделя №{str(self.n_week)}'
        l = f'урок №{str(self.lesson_number)}'
        return w + ', ' + l

    class Meta:
        verbose_name = 'Блок времени'  # Наименование в ед ч
        verbose_name_plural = 'Блоки времени'  # Наименование в мн ч


# # Блок занятия
# class Blok_lesson(models.Model):
#     nclass = models.ForeignKey(
#         nClass,
#         on_delete=models.PROTECT, blank=True, null=True, default=None,
#         verbose_name='Класс'
#     )
    
#     teacher = models.ForeignKey(
#         TeacherProfile,
#         on_delete=models.PROTECT, blank=True, null=True, default=None,
#         verbose_name='Учитель'
#     )
    
#     subject = models.ForeignKey(
#         Subjects,
#         on_delete=models.PROTECT, blank=True, null=True, default=None,
#         verbose_name='Предмет'
#     )    
    
#     def __str__(self):
#         return str(self.nclass) + " - " + str(self.subject) + " - " + str(self.teacher)

#     class Meta:
#         verbose_name = 'Блок занятия'  # Наименование в ед ч
#         verbose_name_plural = 'Блоки занятий'  # Наименование в мн ч


# Блок расписания
class Blok_timetable(models.Model):    
    nclass = models.ForeignKey(
        nClass,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Класс'
    )
    
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Учитель'
    )
    
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Предмет'
    )
    
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Кабинет'
    )
    
    lesson_number = models.ForeignKey(
        LessonNumber,
        verbose_name='Номер урока',
        related_name="lesson_numb",
        on_delete=models.PROTECT,
        blank=True, null=True, default=None
    )
    
    blok_time = models.ForeignKey(
        Blok_time,
        on_delete=models.PROTECT, blank=True, null=True, default=None,
        verbose_name='Блок времени'
    )
    
    n_week = models.IntegerField(verbose_name='День недели', blank=True, null=True, default=None)
    
    def __str__(self):
        w = f'Неделя №{str(self.n_week)}'
        l = f'урок №{str(self.lesson_number)}'
        time = w + ', ' + l
        str_lesson = str(self.nclass) + " - " + str(self.subject) + " - " + str(self.teacher)
        return str_lesson + " - " + str(self.room) + " - " + time

    class Meta:
        verbose_name = 'Блок расписания'  # Наименование в ед ч
        verbose_name_plural = 'Блоки расписаний'  # Наименование в мн ч


# Тип пожелания
class TypeOfRequest(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    
    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Тип пожелания'  # Наименование в ед ч
        verbose_name_plural = 'Типы пожеланий'  # Наименование в мн ч
        ordering = ['title']


# Пожелания
class TeacherRequests(models.Model):
    description = models.TextField(blank=True, verbose_name='Коментарий')
    lavel_value = models.IntegerField(blank=True, verbose_name='Уровень важностьи')
    
    teacer = models.ForeignKey(
        TeacherProfile,
        verbose_name='Учитель',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )
    
    type = models.ForeignKey(
        TypeOfRequest,
        verbose_name='Тип пожелания',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )
    
    time = models.ForeignKey(
        Blok_time,
        verbose_name='Время',
        on_delete=models.PROTECT, blank=True, null=True, default=None
    )
    
    def __str__(self):
        return str(self.teacer) + " - " + str(self.lavel_value)

    class Meta:
        verbose_name = 'Пожелание'  # Наименование в ед ч
        verbose_name_plural = 'Пожелания'  # Наименование в мн ч


# # Журнал
# class Jurnal(models.Model):
#     HomeWork = models.TextField(blank=True, verbose_name='Домашнее задание')

#     timetable = models.ForeignKey(
#         Blok_timetable,
#         verbose_name='К занятияю...',
#         # related_name="class_teacher",
#         on_delete=models.PROTECT,
#         blank=True, null=True, default=None
#     )
    
#     def __str__(self):
#         return str(self.timetable)

#     class Meta:
#         verbose_name = 'Запись журнала'  # Наименование в ед ч
#         verbose_name_plural = 'Журнал'  # Наименование в мн ч


# # Вид работы
# class TypeOfWork(models.Model):
#     title = models.CharField(max_length=250, verbose_name='Вид работы')
#     description = models.TextField(blank=True, verbose_name='Описание')
    
#     def __str__(self):
#         return str(self.title)

#     class Meta:
#         verbose_name = 'Вид работы'  # Наименование в ед ч
#         verbose_name_plural = 'Виды работ'  # Наименование в мн ч


# # Оценки
# class Results(models.Model):
#     student = models.CharField(max_length=250, verbose_name='Обучающийся')
#     point = models.IntegerField(verbose_name='Отметка')

#     jurnal = models.ForeignKey(
#         Jurnal,
#         verbose_name='Журнал',
#         # related_name="class_teacher",
#         on_delete=models.PROTECT,
#         blank=True, null=True, default=None
#     )

#     type_of_work = models.ForeignKey(
#         TypeOfWork,
#         verbose_name='Вид работы',
#         # related_name="class_teacher",
#         on_delete=models.PROTECT,
#         blank=True, null=True, default=None
#     )
    
#     def __str__(self):
#         return str(self.student)

#     class Meta:
#         verbose_name = 'Оценка'  # Наименование в ед ч
#         verbose_name_plural = 'Оценки'  # Наименование в мн ч







