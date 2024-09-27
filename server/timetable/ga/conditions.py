from .utils import *

'''
Элемент расписания: [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет]
'''
def condition1(individual):
    G = classes
    s = 0
    check = True
    
    check_group = []
    # Проверка на первое условие
    # Сверяем каждую группу
    for Gr in G:
        timetable = group(individual, 5)
        check_group = []
        # Перебираем сетку расписания
        for ind in timetable:
            # Если группа в сетке та, которую мы првоеряем
            if ind[0] == Gr.pk:
                # Если это время встречается впервые
                if ind[3] not in check_group:
                    check_group.append(ind[3])
                    s += 1
                # Если одновременные занятия у одной группы - штраф
                else:
                    s -= 1000
                    # print("Ooops...")
                    check = False
        check_group.clear()
    return s, check


def condition2(individual):
    T = teachers
    s = 0
    check = True
    
    check_teacher = []
    # Проверка на второе условие
    # Сверяем каждого препода
    for teacher in T:
        check_teacher = []
        timetable = group(individual, 5)
        # Перебираем сетку расписания
        for ind in timetable:
            # Если препод в секти тот, которого мы првоеряем
            if ind[2] == teacher.pk:
                # Если это время встречается впервые
                if ind[3] not in check_teacher:
                    check_teacher.append(ind[3])
                    s += 1
                # Если одновременные занятия у одного препода - штраф
                else:
                    s -= 1000
                    check = False
    return s, check


def condition3(individual):
    A = ROOMS
    s = 0
    check = True
    
    check_room = []
    # Проверка на третье условие
    # Сверяем каждую аудиторию
    for room in A:
        check_room = []
        timetable = group(individual, 5)
        # Перебираем сетку расписания
        for ind in timetable:
            # Если ауд. в секти та, которую мы првоеряем
            if ind[4] == room.pk:
                # Если это время встречается впервые
                if ind[3] not in check_room:
                    check_room.append(ind[3])
                    s += 1
                # Если одновременные занятия в одной аудитории - штраф
                else:
                    s -= 1000
                    check = False
    return s, check


def cond_ition4(individual):
    # 4. Для предмета в расписани стоит подходящий кабинет
    s = 0
    check = True
    
    timetable = group(individual, 5)
    # Прверим каждый элемент расписания
    for item in timetable:
        # subj_spec = Subjects.obj.get(pk=item[1]).spec.all()
        # print(f'subj_spec = {subj_spec}')
        subj_spec_list = []
        for i in subj_spec:
            if i[0] == item[1]:
                subj_spec_list.append(i[1])
                break
            
        # room_spec = Room.objects.get(pk=item[4]).spec.all()
        room_spec_list = []
        for i in room_spec:
            if i[0] == item[4]:
                room_spec_list.append(i[1])
                break
        
        if subj_spec_list == room_spec_list:
            if subj_spec_list != []:
                # print(f'subj_spec_list = {subj_spec_list}\t\t room_spec_list = {room_spec_list}')
                s += 30
        else:
            s -= 10000
            check = False
    return s, check


def cond5(individual):
    # 5. Нет окон у классов
    '''
    f1(класс, время1, время2):
        Взять все уроки в данный день у данного класса
        Сверить последнее время с время2?
        Совпадает:
            "НЕТ"
        НеСовпадает:
            "ДА"

    Перебор расписания:
        Взяли класс и его время
        Есть ли следующий урок?
        ДА:
            contininy
        НЕТ:
            Есть ли еще уроки в этот день: (???) -> f1(класс, текущий урок и время, предполагаемое время)
            "ДА":
                ПЛОХО
            "НЕТ":
                ХОРОШО
    '''
    s = 0
    check = True
    
    
    for nclass in classes:
        class_times = []
        timetable = group(individual, 5)
        for tt in timetable:
            # Если класс в рассписании тот, который мы проверяем, то 
            # добавить время проведения занятия в список для дальнейшей проверки
            if nclass.pk == tt[0]:
                class_times.append(tt[3])
            
        times = group(time_bloks, 5)
        for w in times:
            for l in w:
                pass
    
    timetable = group(individual, 5)
    # Прверим каждый элемент расписания
    for item in timetable:
        # subj_spec = Subjects.obj.get(pk=item[1]).spec.all()
        # print(f'subj_spec = {subj_spec}')
        subj_spec_list = []
        for i in subj_spec:
            if i[0] == item[1]:
                subj_spec_list.append(i[1])
                break
            
        # room_spec = Room.objects.get(pk=item[4]).spec.all()
        room_spec_list = []
        for i in room_spec:
            if i[0] == item[4]:
                room_spec_list.append(i[1])
                break
        
        if subj_spec_list == room_spec_list:
            if subj_spec_list != []:
                # print(f'subj_spec_list = {subj_spec_list}\t\t room_spec_list = {room_spec_list}')
                s += 30
        else:
            s -= 1000
            check = False
    return s, check



class Cond:
    function_list = []

    def __init__(self):
        self.function_list = [
            self.cond1,
            self.cond2,
            self.cond3
        ]

    def cond1(self, individual):
        G = classes
        s = 0
        check = True
        
        check_group = []
        # Проверка на первое условие
        # Сверяем каждую группу
        for Gr in G:
            timetable = group(individual, 5)
            check_group = []
            # Перебираем сетку расписания
            for ind in timetable:
                # Если группа в сетке та, которую мы првоеряем
                if ind[0] == Gr.pk:
                    # Если это время встречается впервые
                    if ind[3] not in check_group:
                        check_group.append(ind[3])
                        s += 1
                    # Если одновременные занятия у одной группы - штраф
                    else:
                        s -= 1000
                        # print("Ooops...")
                        check = False
            check_group.clear()
        return s, check


    def cond2(self, individual):
        T = teachers
        s = 0
        check = True
        
        check_teacher = []
        # Проверка на второе условие
        # Сверяем каждого препода
        for teacher in T:
            check_teacher = []
            timetable = group(individual, 5)
            # Перебираем сетку расписания
            for ind in timetable:
                # Если препод в секти тот, которого мы првоеряем
                if ind[2] == teacher.pk:
                    # Если это время встречается впервые
                    if ind[3] not in check_teacher:
                        check_teacher.append(ind[3])
                        s += 1
                    # Если одновременные занятия у одного препода - штраф
                    else:
                        s -= 1000
                        check = False
        return s, check


    def cond3(self, individual):
        A = ROOMS
        s = 0
        check = True
        
        check_room = []
        # Проверка на третье условие
        # Сверяем каждую аудиторию
        for room in A:
            check_room = []
            timetable = group(individual, 5)
            # Перебираем сетку расписания
            for ind in timetable:
                # Если ауд. в секти та, которую мы првоеряем
                if ind[4] == room.pk:
                    # Если это время встречается впервые
                    if ind[3] not in check_room:
                        check_room.append(ind[3])
                        s += 1
                    # Если одновременные занятия в одной аудитории - штраф
                    else:
                        s -= 1000
                        check = False
        return s, check