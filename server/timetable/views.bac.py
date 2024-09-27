from asyncio.windows_events import NULL
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, View, ListView
from django.views.generic import TemplateView

from timetable.forms import FormCreateSubject

from timetable.models import (
    Subjects, Room, Organization, StudentProfile, TeacherProfile, nClass
)
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import loader

import random
import string

from data import dat



def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", rand_string)
    return rand_string


def test(request):
    # логика формирования расписания
    """
    TODO: считать данные с учебного плана
    TODO: считать справочные данне
    TODO: сформировать расписание
    """
    a = 100
    b = 444
    c = a + b
    print(c)
    return HttpResponse("Hello World!")


def add_rooms(request):
    data = { "hrefs": [],
            "again": "Создать еще кабинетов",
            "ref_again": "add-test-rooms/"}
    
    for item in range(100, 500, 10):
        room = Room()
        room.numb = item
        room.countm = random.randint(20, 30)
        room.org = Organization.objects.get(id=1)
        room.save()
        data['hrefs'].append(str(room))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_subjects(request):
    data = { "hrefs": [],
            "again": "Создать еще учеников",
            "ref_again": "add-test-students/"}
    
    test_sub = [
        'Пение',
        'Математика',
        'Русский язык',
        'Физика',
        'Философия',
        'Астраномия',
        'Химия',
        'Ядерная физика',
        'Программирование',
        'Бокс',
    ]
    for item in test_sub:
        sub = Subjects()
        sub.title = item
        sub.org = Organization.objects.get(id=1)
        sub.save()
        data['hrefs'].append(str(sub))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_organization(request):
    data = { "hrefs": [],
            "again": "Создать еще организаций",
            "ref_again": "add-test-organization/"}
    
    test_org = [
        'ООО "Ромашка"',
        'ООО "Василек"',
        'ООО "Дашка"',
        'ООО "Колокольчик"',
        'ООО "Жизнь"',
        'ООО "Мир"',
        'ООО "Максим"',
        'ООО "Роза"',
        'ООО "Солнце"',
    ]
    for item in test_org:
        org = Organization()
        org.title = item
        org.save()
        data['hrefs'].append(str(org))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_classes(request):
    """
    TODO: Разобраться с user-ом и профилем... 
    """
    data = { "hrefs": [],
            "again": "Создать еще классы",
            "ref_again": "add-test-classes/"}
    
    ids = [] # получим список существующий id
    for student in StudentProfile.objects.all():
        print("user_id: " + str(student.pk) + ", user: " + str(student))
        ids.append(student.pk)
    print(StudentProfile.objects.count())
    print(ids)
    
    for i in range(1, 11):
        clas = nClass()
        clas.title = str(random.randint(1, 12)) + generate_random_string(1)
        clas.save()
        
        for j in range(1, 5):
            rand_student = StudentProfile.objects.get(pk=random.choice(ids))
            clas.students.add(rand_student.pk)
            
        clas.save()
        data['hrefs'].append(str(clas))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_students(request):
    data = { "hrefs": [],
            "again": "Создать еще учеников",
            "ref_again": "add-test-students/"}
    
    for item in range(5):    
        user = User()
        user.username = "student-" + generate_random_string(10)
        user.first_name = "first-" + generate_random_string(5)
        user.last_name = "last-" + generate_random_string(5)
        user.password = "THE_TEST_PASS_123"
        user.save()
        student = StudentProfile()
        student.user = user
        student.save()
        data['hrefs'].append(str(student))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_teachers(request):
    data = { "hrefs": [],
            "again": "Создать еще учителей",
            "ref_again": "add-test-teachers/"}
    
    for item in range(5):
        user = User()
        user.username = "teacher-" + generate_random_string(10)
        user.first_name = "first-" + generate_random_string(5)
        user.last_name = "last-" + generate_random_string(5)
        user.password = "THE_TEST_PASS_123"
        user.save()
        teacher = TeacherProfile()
        teacher.user = user
        teacher.save()
        data['hrefs'].append(str(teacher))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def add_data(request):
    data = { "hrefs": [],
            "again": "Создать еще",
            "ref_again": "add-test-data/"}
    
    for item in range(5):    
        user = User()
        user.username = "student-" + generate_random_string(10)
        user.first_name = "first-" + generate_random_string(5)
        user.last_name = "last-" + generate_random_string(5)
        user.password = "THE_TEST_PASS_123"
        user.save()
        student = StudentProfile()
        student.user = user
        student.save()
        data['hrefs'].append(str(student))
    
    for item in range(5):
        user = User()
        user.username = "teacher-" + generate_random_string(10)
        user.first_name = "first-" + generate_random_string(5)
        user.last_name = "last-" + generate_random_string(5)
        user.password = "THE_TEST_PASS_123"
        user.save()
        teacher = TeacherProfile()
        teacher.user = user
        teacher.save()
        data['hrefs'].append(str(teacher))
        
    test_org = [
        'ООО "Гармония"',
        'ООО "Ромашка"',
        'ООО "Василек"',
        'ООО "Дашка"',
        'ООО "Колокольчик"',
        'ООО "Жизнь"',
        'ООО "Мир"',
        'ООО "Максим"',
        'ООО "Роза"',
        'ООО "Солнце"',
    ]
    for item in test_org:
        org = Organization()
        org.title = item
        org.save()
        data['hrefs'].append(str(org))
        
    test_sub = [
        'Пение',
        'Математика',
        'Русский язык',
        'Физика',
        'Философия',
        'Астраномия',
        'Химия',
        'Ядерная физика',
        'Программирование',
        'Бокс',
    ]
    for item in test_sub:
        sub = Subjects()
        sub.title = item
        sub.org = Organization.objects.get(id=1)
        sub.save()
        data['hrefs'].append(str(sub))
        
    for item in range(100, 500, 10):
        room = Room()
        room.numb = item
        room.countm = random.randint(20, 30)
        room.org = Organization.objects.get(id=1)
        room.save()
        data['hrefs'].append(str(room))
        
    ids = [] # получим список существующий id
    for student in StudentProfile.objects.all():
        print("user_id: " + str(student.pk) + ", user: " + str(student))
        ids.append(student.pk)
    print(StudentProfile.objects.count())
    print(ids)
    
    for i in range(1, 11):
        clas = nClass()
        clas.title = str(random.randint(1, 12)) + generate_random_string(1)
        clas.save()
        
        for j in range(1, 5):
            rand_student = StudentProfile.objects.get(pk=random.choice(ids))
            clas.students.add(rand_student.pk)
            
        clas.save()
        data['hrefs'].append(str(clas))
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


def main(request):
    template = "test_tables.html"
    context = {"hrefs": [
            {
                'href': "#",
                'text': "text"
            },
            {
                'href': "#",
                'text': "text"
            },
            {
                'href': "#",
                'text': "text"
            },
        ]}
    return HttpResponse(template.render(context, request))
    # return render("test_tables.html", context=context)


class MainView(TemplateView):
    template_name = "test_tables.html"
    
    def get_context_data(self, **kwargs):
        context = {
            "title": "Доступные ссылки:",
            # "hrefs": [
            # {
            #     'href': "see/",
            #     'text': "(В разработке)_________Просмотреть БД"
            # },
            # {
            #     'href': "add-test-data/",
            #     'text': "Создать тестовые данные для всей БД"
            # },
            # {
            #     'href': "add-test-teachers/",
            #     'text': "Создать Учителей"
            # },
            # {
            #     'href': "add-test-students/",
            #     'text': "Создать Студентов"
            # },
            # {
            #     'href': "add-test-rooms/",
            #     'text': "Создать Кабинеты"
            # },
            # {
            #     'href': "add-test-subjects/",
            #     'text': "Создать Пердметы"
            # },
            # {
            #     'href': "add-test-organization/",
            #     'text': "Создать Организации"
            # },
            # {
            #     'href': "add-test-classes/",
            #     'text': "Создать Классы"
            # },]
            'data':
            [
                {
                    'hrefs': [{
                        'href': "see/",
                        'text': "Просмотреть БД"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "create/TrainingCalendar/",
                        'text': "(В разработке) Сгенерировать учебный план"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "#",
                        'text': "(В разработке) Просмотреть Расписание"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "#",
                        'text': "(В разработке) Создать Расписание"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-data/",
                        'text': "Создать тестовые данные для всей БД"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-teachers/",
                        'text': "Создать Учителей"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-students/",
                        'text': "Создать Студентов"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-rooms/",
                        'text': "Создать Кабинеты"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-subjects/",
                        'text': "Создать Пердметы"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-organization/",
                        'text': "Создать Организации"
                    }]
                },
                {
                    'hrefs': [{
                        'href': "add-test-classes/",
                        'text': "Создать Классы"
                    }]
                },
            ]
        }
        return context


class SeeDbView(TemplateView):
    template_name = "test_tables.html"
    
    def get_context_data(self, **kwargs):
        context = {
            "title": "Веберите сущность для отображения:",
            'data': 
            [
                {
                    'hrefs': [{
                        'href': 'see/students/',
                        'text': 'Просмотреть Студентов'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/classes/',
                        'text': 'Просмотреть Классы'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/teachers/',
                        'text': 'Просмотреть Учителей'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/rooms/',
                        'text': 'Просмотреть Кабинеты'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/sub/',
                        'text': 'Просмотреть Предметы'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/organizations/',
                        'text': 'Просмотреть Организации'
                    }]
                },
                {
                    'hrefs': [{
                        'href': 'see/users/',
                        'text': 'Просмотреть всех пользователей'
                    }]
                },
            ]
        }
        return context


class ModelFromSubjects(FormView):
    form_class = FormCreateSubject
    template_name = "model_from_page.html"
    success_url = reverse_lazy("createsub")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TotalSubjects(TemplateView):
    template_name = "test_tables.html"
    
    def get_context_data(self, **kwargs):
        context = {
            "title": "(В разработке) Предметы:",
            "data": [
            {
                'hrefs': [{
                    'href': "see/sub/#",
                    'text': "Тут список предметов"
                }]
            }],
        }
        sub = Subjects.obj.all()
        for s in sub:
            context["data"].append({
                'hrefs': 
                [
                    {
                        'href': 'see/sub/#',
                        'text': s.title
                    },
                    {
                        'href': 'see/sub/#',
                        'text': s.pk
                    },
                ]
            })
        # print(context)
        return context



class ListSub(ListView):
    template_name = 'see/sub.html'
    queryset = Subjects.obj.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'Предметы', 
            'id',
            'Кнопки действий. Функционал не реализован. Можно добавить '
                'в последующих спринтах'
        ]
        return context


class ListStudents(ListView):
    template_name = 'see/students.html'
    queryset = StudentProfile.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'Студенты', 
            'id',
            'Кнопки действий. Функционал не реализован. Можно добавить '
                'в последующих спринтах'
        ]
        return context


class ListClasses(ListView):
    template_name = 'see/classes.html'
    queryset = nClass.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'id', 
            'Классы', 
            'Номер',
            'Организация'
        ]
        return context


class ListTeachers(ListView):
    template_name = 'see/Teachers.html'
    queryset = TeacherProfile.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'id', 
            'Учитель',
            'Кнопки действий. Функционал не реализован. Можно добавить '
                'в последующих спринтах'
        ]
        return context


class ListRooms(ListView):
    template_name = 'see/Rooms.html'
    queryset = Room.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'id', 
            'Кабинет',
            'Кнопки действий. Функционал не реализован. Можно добавить '
                'в последующих спринтах'
        ]
        return context


class ListOrg(ListView):
    template_name = 'see/Org.html'
    queryset = Organization.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'id', 
            'Организаия',
            'Кнопки действий. Функционал не реализован. Можно добавить '
                'в последующих спринтах'
        ]
        return context
    

class ListUsers(ListView):
    template_name = 'see/Users.html'
    queryset = User.objects.all()
    context_object_name = "objects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_caps'] = [
            'id', 
            'Пользователь',
            'Админ?',
            'Пароль',
        ]
        return context
    
    

class CreateTrainingCalendar(TemplateView):
    template_name = "test_detail.html"
    
    def get_context_data(self, **kwargs):
        context = { "hrefs": [],
            "again": "Сформировать еще (Не предусмотрено)",
            "ref_again": "create/TrainingCalendar/"}
        context['hrefs'].append("Для генерации нужны данные...")
        return context


# class DBViewer(ListView):
#     template_name = 'see/sub.html'
    
#     def get(self, request, s):
#         print("hi")
#         return render(request,
#                       self.template_name)


class ViewSubjects(View):
    def get(self, request, pk):
        print(request)
        t = Subjects.obj.get(id=pk)
        print(type(t))
        return HttpResponse("Hello, world! I wont see the sub\n" + str(t))
