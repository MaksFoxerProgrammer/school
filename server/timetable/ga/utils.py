from email.headerregistry import Group
from ..models import *

import random

from .deap.algorithms import logger # Костыль =(

# from loguru import logger
# logger.add(
#     "log.log", 
#     format="{time} {level} {message}", 
#     level="DEBUG"
# )

ROOMS = Room.objects.all()
classes = nClass.objects.all()
subjects = Subjects.objects.all()
teachers = TeacherProfile.objects.all()
tr_cal = TrainingCalendar.objects.all()
teachers_subjects = Teacher_Subjects.objects.all()
time_bloks = Blok_time.objects.all()

sep = "================================="
rooms_count = ROOMS.count()
times_count = time_bloks.count()
rooms_ids = []

subj_spec = []
room_spec = []

CONDITIONS = list()

# Вспомогательная: сгруппировать iterable по count штук
def group(iterable, count):
    """ Группировка элементов последовательности по count элементов """
    return zip(*[iter(iterable)] * count)

def avialable_room(subject):
    """ Возвращает список допустимых кабинетов для предмета 
    
    Все специализации предмета
    По всем кабинетам
        Если спец. кабинета В спец. предмета:
            Кабинет к доступным
    Вернуть все доступные кабинеты
    """
    subj = Subjects.objects.get(pk=subject)
    subject_spec_list = []#set()
    rooms = []
    
    for item in subj.spec.all():
        subject_spec_list.append(item.pk)
    
    for room in ROOMS:
        rooms_spec_list = []#set()
        
        for item in room.spec.all():
            rooms_spec_list.append(item.pk)
            
        # print(f'\t rooms_spec_list = {rooms_spec_list} \t subject_spec_list {subject_spec_list}')
        
        if rooms_spec_list == subject_spec_list:
            rooms.append(room.pk)
            # print(f'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\t room = {room}')
        # else:
        #     print(f'{rooms_spec_list} != {subject_spec_list}')
            
    if not rooms:
        for room in ROOMS:
            rooms.append(room.pk)
    return rooms


def avialable_group(lessons, time):
    ''' lessons = [ [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет], ] '''
    groups = []
    G = classes
    check = True
    

    # Сверяем каждую группу
    for Gr in G:
        timetable = group(lessons, 5)
        # Перебираем сетку расписания
        for ind in timetable:
            # Если группа в сетке та, которую мы првоеряем
            if ind[0] == Gr.pk:
                # Если такое время уже встречалось, то это плохо
                if ind[3] == time:
                    check = False
                    break
        if check:
            groups.append(Gr)

    if not groups:
        # print("Ooooooooops.....")
        logger.error('Не найдено группы')
        groups = classes

    return groups


def avialable_time_v1(lessons, gr):
    ''' lessons = [ [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет], ] '''
    times = []
    for time in range(1, times_count):
        times.append(time)
    
    gr = nClass.objects.get(pk=gr)
    check_times = []

    if not lessons:
        return times
    
    timetable = group(lessons, 5)
    # Перебираем сетку расписания
    for ind in timetable:
        # Если группа в сетке та, которую мы првоеряем
        if ind[0] == gr.pk:
            # Если это время встречается впервые
            if ind[3] not in check_times:
                check_times.append(ind[3])


    if not check_times:
        print("Ooooooooops.....")
        check_times = times
    
    return check_times



def avialable_time_v2(lessons, gr):
    ''' lessons = [ [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет], ] '''
    times = []
    for time in range(1, times_count):
        times.append(time)
    return times


def avialable_time_v3(lessons, gr, count = 1):
    ''' lessons = [ [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет], ] '''
    gr = nClass.objects.get(pk=gr)
    timetable = group(lessons, 5)

    time_all = [i for i in range(1, 36)]
    good_times = []

    close_time = []
    # Перебираем сетку расписания
    for ind in timetable:
        # Если группа в сетке та, которую мы првоеряем
        if ind[0] == gr.pk:
            close_time.append(ind[3])
            # print(f'Для gr={gr.pk} время {ind[3]} занято!')

    for day in group(time_all, 5):
        # print(f"\n {day} \n") 
        for time in day:
            if count <= 0:
                return good_times
            if time in close_time:
                continue
            else:
                good_times.append(time)
                count -= 1
    print("Ooooooopssss....")
    return good_times


def avialable_time_v4(lessons, gr):
    ''' lessons = [ [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет], ] '''

    gr = nClass.objects.get(pk=gr)
    timetable = group(lessons, 5)
    time_all = [i for i in range(1, 36)]
    good_time = []
    close_time = []

    # Соберем занятое время для группы
    # Перебираем сетку расписания
    for ind in timetable:
        # Если группа в сетке та, которую мы првоеряем
        if ind[0] == gr.pk:
            close_time.append(ind[3])
            # print(f'Для gr={gr.pk} время {ind[3]} занято!')

    # Сформируем текущую доступную неделю
    week = []
    for day in group(time_all, 7):
        week_item = []
        for time in day:
            if time not in close_time: ################
                week_item.append(time)
        if week_item:
            week.append(week_item)
    # print(week)
    
    # Соберем доступное время
    for day in week:
        # print(f'day = {day}')
        good_time.append(day[0])
    # print("\n\n")

    return good_time
