from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from django.shortcuts import redirect 

import random
import string

from data import dat

from .models import *

# url = 'Https://harmony-school.life/'
url = 'http://127.0.0.1:8000/'

SETTINGS = {
    "teachers": 10,
    "classes": 10,
    "rooms": 10,
    "subjects": 10,
} 


def generate_random_string(length, count=0):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", rand_string)
    if count > 0:
        lst = []
        lst.append(rand_string)
        for item in range(count):
            letters = string.ascii_lowercase
            rand_string = ''.join(random.choice(letters) for i in range(length))
            lst.append(rand_string)
        return lst
    return rand_string

# Расшифровка по дням недели
def n_week_decode(week):
    if week == 1:
        return 'Пн'
    elif week == 2:
        return 'Вт'
    elif week == 3:
        return 'Ср'
    elif week == 4:
        return 'Чт'
    elif week == 5:
        return 'Пт'
    elif week == 6:
        return 'Сб'
    elif week == 7:
        return 'Вс'


def teachers(data):
    for item in range(SETTINGS["teachers"]):
        rnd = generate_random_string(5, 4)
        name = "Пользователь - " + rnd[0]
        user = User.objects.create(username=name, password="THE_TEST_PASS_123")
        
        teacher = TeacherProfile()
        teacher.user = user
        teacher.name1 = "Фамилия - " + rnd[0]
        teacher.name2 = "Имя - " + rnd[1]
        teacher.name3 = "Отчество - " + rnd[2]
        teacher.save()
        data['hrefs'].append(str(teacher))
    return data

def classes(data):
    for item in range(SETTINGS["classes"]):
        clas = nClass()
        clas.title = str(random.randint(1, 12)) + generate_random_string(1)
        clas.save()
        data['hrefs'].append(str(clas))
    return data

def specializations(data):
    spec = Specialization()
    spec.title = 'Спортзал'
    spec.save()
    data['hrefs'].append(str(spec))
    
    spec = Specialization()
    spec.title = 'Проектор'
    spec.save()
    data['hrefs'].append(str(spec))
    return data

def rooms(data):
    for item in range(SETTINGS["rooms"]):
        room = Room()
        room.numb = random.randint(100, 500)
        room.count = random.randint(10, 50)
        room.save()
        data['hrefs'].append(str(room))
    return data

def subjects(data):
    for item in range(SETTINGS["subjects"]):
        subj = Subjects()
        subj.title = "Предмет - " + generate_random_string(5)
        subj.save()
        data['hrefs'].append(str(subj))
    return data

def teacher_subjects(data):
    teachers = TeacherProfile.objects.all()
    # По всем учителям
    for teacher in teachers:
        # Каждому учителю по 3 урока
        for itemn in range(3):
            ts = Teacher_Subjects()
            ts.teacher = teacher
            ts.nclass = nClass.objects.get(pk=random.randint(1, SETTINGS["classes"]))
            ts.subject = Subjects.objects.get(pk=random.randint(1, SETTINGS["subjects"]))
            ts.save()
            data['hrefs'].append(str(ts))
        
    return data

# def corse(data):
#     corse = Corse()
#     corse.start_data = 1
#     corse.the_time = 270
#     corse.title = 'Учебный план'
#     corse.save()
    
#     data['hrefs'].append(str(corse))
        
#     return data

# def course_lesson(data):
#     subjects = Subjects.objects.all()
#     for subject in subjects:
#         cl = CourseLesson()
#         cl.time_count = random.randint(1, 5)
#         # cl.course.set(Corse.objects.get(pk=1))
#         cl.save
#         data['hrefs'].append(str(cl))
        
#     return data

def lesson_number(data):
    for numb in range(7):
        ln = LessonNumber()
        ln.number = numb+1
        ln.save()
        data['hrefs'].append(str(ln))
        
    return data

def blok_time(data):
    lesson_numbers = LessonNumber.objects.all()
    for week in range(3):
        for lesson_number in lesson_numbers:
            bt = Blok_time()
            bt.n_week = week
            bt.lesson_number = lesson_number
            bt.save()
            data['hrefs'].append(str(bt))
        
    return data

# def blok_lesson(data):
#     classes = nClass.objects.all()
#     teachers = TeacherProfile.objects.all()
#     subjects = Subjects.objects.all()
    
#     for item in range(50):
#         bl = Blok_lesson()
#         bl.nclass = random.choice(classes)
#         bl.teacher = random.choice(teachers)
#         bl.subject = random.choice(subjects)
#         bl.save()
#         data['hrefs'].append(str(bl))
        
#     return data

def blok_timetable(data):
    # lessons = Blok_lesson.objects.all()
    times = Blok_time.objects.all()
    rooms = Room.objects.all()
    
    nclass = nClass.objects.all()
    teacher = TeacherProfile.objects.all()
    subject = Subjects.objects.all()
    
    
    lesson_numbers = LessonNumber.objects.all()
    
    for item in range(100):
        # lesson_id = 
        timetable = Blok_timetable()
        # timetable.blok_lesson = random.choice(lessons)
        timetable.blok_time = random.choice(times)
        timetable.room = random.choice(rooms)
        
        timetable.nclass = random.choice(nclass)
        timetable.teacher = random.choice(teacher)
        timetable.subject = random.choice(subject)
        
        timetable.n_week = random.randint(1, 7)
        timetable.lesson_number = random.choice(lesson_numbers)
        timetable.save()
        data['hrefs'].append(str(timetable))
        
    return data



def geterate_test_data(request):
    data = { "hrefs": [],
            "again": "Создать еще кабинетов",
            "ref_again": "add-test-rooms/"}
    
    data = teachers(data)
    data = classes(data)
    data = specializations(data)
    data = rooms(data)
    data = subjects(data)
    data = teacher_subjects(data)
    # data = corse(data)
    # data = course_lesson(data)
    data = lesson_number(data)
    data = blok_time(data)
    # data = blok_lesson(data)
    data = blok_timetable(data)
    
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))


###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################


def admin_geterate_test_data(request):
    data = { "hrefs": [],
            "again": "Создать еще кабинетов",
            "ref_again": "add-test-rooms/"}
    
    data = teachers(data)
    data = classes(data)
    data = specializations(data)
    data = rooms(data)
    data = subjects(data)
    data = teacher_subjects(data)
    # data = corse(data)
    # data = course_lesson(data)
    data = lesson_number(data)
    data = blok_time(data)
    # data = blok_lesson(data)
    data = blok_timetable(data)
    
    # return redirect('http://127.0.0.1:8000/admin/timetable/blok_timetable/')
    return redirect(url+'admin/timetable/')




def main_page(request):    
    return redirect(url+'admin/timetable/')


###############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################


def specializations(data):
    # Создаем специализации
    for item in dat.SPECIALIZATIONS:
        org = Specialization()
        org.title = item["title"]
        org.save()
        data['hrefs'].append(str(org))
    return data

def subjects(data):
    # Создаем предметы
    for item in dat.SUBJECTS:
        sub = Subjects()
        sub.title = item["title"]
        sub.save()
        # Добавим допы к предмету
        specs = []
        for spec in item["Dop"]:
            s = Specialization.objects.all().filter(title=spec).first() 
            specs.append(s.pk)
            
        # print(f'sub = {sub}, cpec = {specs}, \t\t\t\t\t\t\t item["Dop"] = {item["Dop"]}')
        
        if specs:
            sub.spec.set(specs)
            sub.save()
            
        data['hrefs'].append(str(sub))
    print(data)
    return data

def rooms(data):
    # Создаем комнаты
    for item in dat.ROOMS:
        room = Room()
        room.numb = item["title"]
        room.count = item["Counts"]
        room.save()
        
        specs = []
        for spec in item["dop"]:
            s = Specialization.objects.all().filter(title=spec).first() 
            specs.append(s.pk)
            
        if specs:
            room.spec.set(specs)
            room.save()
        
        # specc = Specialization.objects.filter(room=item["dop"]).first()
        # print(specc)
        # if specc:
        #     room.spec.set(specc)
        #     room.save()
        data['hrefs'].append(str(room))
    return data

def classes(data):
    # Создаем классы
    for item in dat.CLASSES:
        clas = nClass()
        clas.title = item["title"]
        clas.size = item["size"]
        clas.digit = item.get("digit")
        clas.ltr = item.get("char")
        clas.save()        
        data['hrefs'].append(str(clas))
    return data

def teachers(data):
    # Создаем преподавателей
    for item in dat.TEACHERS:
        rnd = generate_random_string(5)
        name = item["name"]+" "+rnd
        user = User.objects.create(username=name, password="THE_TEST_PASS_123")
        teacher = TeacherProfile()
        teacher.user = user
        teacher.name1 = item["name"]
        teacher.name2 = ''
        teacher.save()
        
        # Что этот препод может вести?
        for sub in item["available"]:
            '''sub = {"Gr": "8а, 8б, 9а, 9б, 9в, 10а, 10б, 11а, 11б, 11в", "Disc": [1]}'''
            # item = Class_Subjects.objects.create(nclass=sub["Gr"], subject=sub["Disc"])
            groups = sub["Gr"] # Тут строка
            disc = sub["Disc"] # Тут id предмета
            
            groups = groups.split(", ")
            
            # Для каждого предмета
            for d in disc:
                # Каждый класс (строка!)
                for g in groups:
                    # real_cls = nClass.objects.filter(title__contains=g)
                    try:
                        real_cls = nClass.objects.filter(title=g).first()
                    except nClass.DoesNotExist:
                        # Если такой класс еще был не создан, то 
                        # его надо создать
                        real_cls = nClass.objects.create(title=g, Number=20)
                        data['hrefs'].append(str(real_cls))
                        
                    reat_sub = Subjects.objects.get(id=d)
                        
                    cls_sub = Teacher_Subjects.objects.create(
                        teacher = teacher,
                        nclass = real_cls,
                        subject = reat_sub
                    )
                    
        data['hrefs'].append(str(teacher))
    return data

def lesson_number(data):
    lessons = 7
    for less in range(1, lessons+1):
        ln = LessonNumber()
        ln.number = less
        ln.save()
        data['hrefs'].append(str(ln))
    return data

def time_bloks(data, weeks = 5, lessons = 7):
    '''
    Пн = 7 уроков
    Неделя = 7*5 = 35
    '''
    # Создаем комнаты
    for w in range(1, weeks+1):
        for less in range(1, lessons+1):
            time_bl = Blok_time()
            time_bl.n_week = w
            time_bl.lesson_number = LessonNumber.objects.get(pk=less)
            time_bl.save()
            data['hrefs'].append(str(time_bl))
    return data

def corse_lesson(data):
    # Создаем учебный план
    for item in dat.TRAINING_PLAN:
        """
        Достать все X-е классы (по буквам):
            Вставить предмет (id-7) на posX часов
        """
        subj = Subjects.objects.get(pk=item[7]) # Там id предмета 
        # Для всех классов
        classes = nClass.objects.all()
        for cls in classes:
            time = -1
            # Для каждого N-го класса
            if cls.digit == 5:
                time = item[0] # Часы в неделю для класса
            elif cls.digit == 6:
                time = item[1] # Часы в неделю для класса
            elif cls.digit == 7:
                time = item[2] # Часы в неделю для класса
            elif cls.digit == 8:
                time = item[3] # Часы в неделю для класса
            elif cls.digit == 9:
                time = item[4] # Часы в неделю для класса
            elif cls.digit == 10:
                time = item[5] # Часы в неделю для класса
            elif cls.digit == 11:
                time = item[6] # Часы в неделю для класса
            
            if time > 0:
                tr_c = TrainingCalendar()
                tr_c.ncls = cls
                tr_c.subj = subj
                tr_c.time_total = time
                tr_c.save()
                # data['hrefs'].append({
                #     "cls": tr_c.ncls,
                #     "subj": tr_c.subj,
                #     "org": tr_c.org,
                #     "h": tr_c.time_total,
                # })
                data['hrefs'].append(str(tr_c))
    return data



def delete_everything(request):
    Specialization.objects.all().delete()
    print('ok')
    Teacher_Subjects.objects.all().delete()
    print('ok')
    TrainingCalendar.objects.all().delete()
    print('ok')
    Blok_time.objects.all().delete()
    print('ok')
    Blok_timetable.objects.all().delete()
    print('ok')
    Subjects.objects.all().delete()
    print('ok')
    Room.objects.all().delete()
    print('ok')
    nClass.objects.all().delete()
    print('ok')
    TeacherProfile.objects.all().delete()
    print('ok')
    LessonNumber.objects.all().delete()
    print('ok')
    
    # Results.objects.all().delete()
    # TypeOfWork.objects.all().delete()
    # Jurnal.objects.all().delete()
    # TeacherRequests.objects.all().delete()
    # TypeOfRequest.objects.all().delete()
    # Blok_lesson.objects.all().delete()
    # Teacher_Subjects.objects.all().delete()
    # Corse.objects.all().delete()
    # User.objects.all().delete()
    
    return redirect(url+'admin/timetable/')

    

def add_real_data(request):
    data = { "hrefs": [],
            # "again": "Создать еще",
            # "ref_again": "add-test-data/"
            }
    
    data = specializations(data)
    data = subjects(data)
    data = rooms(data)
    data = classes(data)
    data = teachers(data)
    data = corse_lesson(data)
    data = lesson_number(data)
    data = time_bloks(data)
        
    print(data)
    return HttpResponse(loader.render_to_string("test_detail.html", data))



class CreateTimeTable(TemplateView):
    template_name = "createTimeTable.html"
    
    def get_context_data(self, **kwargs):
        '''
        
        '''
        context = { "hrefs": [],
            "again": "Сформировать еще (Не предусмотрено)",
            "ref_again": "create/TrainingCalendar/"}
        tt_old = Blok_timetable.objects.all()
        
        for item in tt_old:
            item.delete()
        
        from .ga import ga3
        timetable = ga3.run()
        
        for item in timetable:
            # print(item)
            clas = nClass.objects.get(pk=item[0])
            subj = Subjects.objects.get(pk=item[1])
            teacher = TeacherProfile.objects.get(pk=item[2])
            time = Blok_time.objects.get(pk=item[3])
            room = Room.objects.get(pk=item[4])
            
            tt = Blok_timetable()
            tt.nclass = clas
            tt.subject = subj
            tt.teacher = teacher
            tt.blok_time = time
            tt.room = room
            
            tt.n_week = time.n_week
            tt.save()
            
            
            app = {
                # 'org': '0',
                'd': n_week_decode(time.n_week),
                'numb': time.lesson_number,
                'cls': clas.title,
                'subj': subj.title,
                'room': room.numb,
                'teacher': teacher.user.username,
            }
            context['hrefs'].append(app)

        return context


GA = 1

def createTimeTable(request):
    if GA:
        tt_old = Blok_timetable.objects.all()
            
        for item in tt_old:
            item.delete()
        
        from .ga import ga3
        timetable = ga3.run()
        
        for item in timetable:
            # print(item)
            clas = nClass.objects.get(pk=item[0])
            subj = Subjects.objects.get(pk=item[1])
            teacher = TeacherProfile.objects.get(pk=item[2])
            time = Blok_time.objects.get(pk=item[3])
            room = Room.objects.get(pk=item[4])
            
            tt = Blok_timetable()
            tt.nclass = clas
            tt.subject = subj
            tt.teacher = teacher
            tt.blok_time = time
            tt.room = room
            
            tt.n_week = time.n_week
            tt.lesson_number = time.lesson_number
            tt.save()
        
    return redirect(url+'admin/timetable/blok_timetable/')


