from itertools import count
from tabnanny import check
from .deap import base, algorithms
from .deap import creator
from .deap import tools

import random
import matplotlib.pyplot as plt
import numpy as np

from prettytable import PrettyTable

from .utils import *
from .conditions import *
from timetable.ga import conditions


# Сформировать блоки занятий
def gen_subj_list():
    '''
    На выходе список списков: [Класс, Предмет, Учитель]
    '''
    Z = []
    log = {"OK":[], "NO": []}
    err = 0
    # По всему уч плану
    for up in tr_cal:
        # По часам в записи
        for i in range(0, up.time_total):
            # найдем препода, который может это вести
            checkError = True
            for teacher in teachers_subjects:
                if teacher.subject == up.subject and teacher.nclass == up.ncls:
                    app = [up.ncls.pk, up.subject.pk, teacher.teacher.pk]
                    Z.append(app)

                    checkError = False
                    log["OK"].append(f'Получилось: {up.ncls.title, up.subject.title, teacher.teacher.user.username}')
            if checkError:
                log["NO"].append(f'Нет учителя у {up.ncls} для {up.subject}')
                err += 1
    return Z, log, err


# Распечатать блоки занятий в консоль
def printSubjList(lessons):
    '''
    Элемент: [0-Класс, 1-Предмет, 2-Учитель]
    '''
    newtt = []
    number = 0
    new_lessons = []
    for item in lessons:
        new_lessons.extend(item)
        
    tt = group(new_lessons, 6)
    for i in tt:
        number += 1
        a1 = number
        a2 = nClass.objects.get(pk=i[0]) # Класс
        a3 = Subjects.obj.get(pk=i[1]) # Предмет
        a4 = TeacherProfile.objects.get(pk=i[2]) # Учитель
        # print(f'{a1}\t{a2}\t\t{a3}\t\t\t{a4}\t{a5}\t{a6}\t')
        newtt.extend([a1, a2, a3, a4])
        
    # Определяем твою шапку и данные.
    th = ['#', 'Класс', 'Предмет', 'Преподаватель', ]
    td = newtt

    columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

    table = PrettyTable(th)  # Определяем таблицу.

    # Cкопируем список td, на случай если он будет использоваться в коде дальше.
    td_data = td[:]
    # Входим в цикл который заполняет нашу таблицу.
    # Цикл будет выполняться до тех пор пока у нас не кончатся данные
    # для заполнения строк таблицы (список td_data).
    while td_data:
        # Используя срез добавляем первые пять элементов в строку.
        # (columns = 5).
        table.add_row(td_data[:columns])
        # Используя срез переопределяем td_data так, чтобы он
        # больше не содержал первых 5 элементов.
        td_data = td_data[columns:]

    print(table)  # Печатаем таблицу


# Инициализация rooms_ids
def get_rooms_ids():
    for room in ROOMS:
        rooms_ids.append(room.pk)



# Тут оценить качество расписания
def oneMaxFitness(individual):
    """
    Необходимые проверки:
    * 1. Нет одновременных занятий у одной группы
    * 2. Нет одновременных занятий у одного препода
    * 3. Нет одновременных занятий в одной аудитории
    * 4. Для предмета в расписани стоит подходящий кабинет
    """
    '''
    Элемент расписания: [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет]
    '''
    s = 0
    
    for condition in CONDITIONS:
        i, _ = condition(individual)
        s += i

            
    return s, # кортеж


##############################################################################
##############################################################################
#################### Тут начинается ГА #######################################
##############################################################################
##############################################################################


# Формирование расписания
def createIndivid(lessons):
    '''
    out: [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет]
    '''
    tt = []
    for lesson in lessons:
        gr = lesson[0]
        disc = lesson[1]
        teacher = lesson[2]
        # Блок времени в расписание
        #! Потом брать из БД !!!!!!!
        time = random.randint(1, times_count)
        
        # room = random.randint(1, rooms_count)
        rooms = avialable_room(disc)
        room = random.choice(rooms)
        
        # print(f'time: {time}, room: {room}')
        iter = [gr, disc, teacher, time, room]
        tt.extend(iter)
        
    return creator.Individual(tt)


# Код мутации
def mutTT(individual, indpb):
    time_count = 0
    room_count = 0
    count_in_item = 5
    
    new_lst = group(individual, count_in_item)
    
    for index, item in enumerate(new_lst):
        
        # Время
        if random.random() < indpb:
            time_count += 1
            z = count_in_item*(index) + 3
            individual[z] = random.randint(1, times_count)
        
        # Кабинет
        if random.random() < indpb:
            # room_spec
            room_count += 1
            z = count_in_item*(index) + 4
            # individual[z] = random.randint(1, rooms_count)
            rooms = avialable_room(item[1])
            # individual[z] = random.choices(rooms)
            individual[z] = random.choice(rooms)

    return individual,


# Код консольного вывода расписания
def printTT(timetable):
    """Распечатать расписание"""
    '''
    Элемент расписания: [0-Класс, 1-Предмет, 2-Учитель, 3-Время, 4-Кабинет]
    '''
    
    newtt = []
    number = 0
    tt = group(timetable, 5)
    for i in tt:
        number += 1
        a1 = number
        
        a2 = nClass.objects.get(pk=i[0]) # Класс
        a3 = Subjects.obj.get(pk=i[1]) # Предмет
        a4 = TeacherProfile.objects.get(pk=i[2]) # Учитель
        
        a5 = i[3] # Время
        a6 = Room.objects.get(pk=i[4]) # Кабинет
        
        # print(f'{a1}\t{a2}\t\t{a3}\t\t\t{a4}\t{a5}\t{a6}\t')
        newtt.extend([a1, a2, a3, a4, a5, a6])
    
    
    # timetable_pro = []
    # # По каждому классу
    # for nclass in classes:
    #     # Проверяем расписания
    #     tt = group(timetable, 5)
    #     for item in tt:
    #         if nclass.pk == item[0]:
    #             # Каждый день недели и урок
    #             the_time = group(time_bloks, 5)
    #             for w in the_time:
    #                 for l in w:
    #                     print(f'')
    #                     timetable_pro.extend([
    #                         nclass,
    #                         w,
    #                         l,
    #                         Subjects.obj.get(pk=item[1]),
    #                         TeacherProfile.objects.get(pk=item[2]),
    #                         Room.objects.get(pk=item[4])
    #                     ])
                        
    
    # th2 = ['Класс', 'День', 'Урок', 'Предмет', 'Учитель', 'Кабинет', ]
    # td2 = timetable_pro
    # columns2 = len(th2)
    # table2 = PrettyTable(th2)
    # while td2:
    #     table2.add_row(td2[:columns2])
    #     td2 = td2[columns2:]
    # # print(table2)
        
    # Определяем твою шапку и данные.
    th = ['#', 'Класс', 'Предмет', 'Преподаватель', 'Время (код)', 'Кабинет', ]
    td = newtt

    columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

    table = PrettyTable(th)  # Определяем таблицу.

    # Cкопируем список td, на случай если он будет использоваться в коде дальше.
    td_data = td[:]
    # Входим в цикл который заполняет нашу таблицу.
    # Цикл будет выполняться до тех пор пока у нас не кончатся данные
    # для заполнения строк таблицы (список td_data).
    while td_data:
        # Используя срез добавляем первые пять элементов в строку.
        # (columns = 5).
        table.add_row(td_data[:columns])
        # Используя срез переопределяем td_data так, чтобы он
        # больше не содержал первых 5 элементов.
        td_data = td_data[columns:]

    print(table)  # Печатаем таблицу


def init_specs(see_subj = False, see_room = False):
    # subj_spec = []
    subj = subjects
    for i in subj:
        app = [i.pk, ]
        app2 = []
        sub_s = i.spec.all()
        if not sub_s:
            app2.append(0,)
        for j in sub_s:
            app2.append(j.pk)
            
        app.append(app2)
        subj_spec.append(app)
    
    if see_subj:
        for item in subj_spec:
            print(item)
    
    # room_spec = []
    for item in ROOMS:
        app = [item.pk, ]
        app2 = []
        rom_s = item.spec.all()
        if not rom_s:
            app2.append(0,)
        for j in rom_s:
            app2.append(j.pk)
            
        app.append(app2)
        room_spec.append(app)
    
    if see_room:
        for item in room_spec:
            print(item)





def run():
    config = {
        # 'log_OK': True,
        # 'log_NO': True,
        # 'rooms_count': True,
        # 'printSubjList': True,
        # 'err_count': True,
        'print_info': True,
        # 'timetable': True,
        'graph': True,
        'check_best': True,
        # 'see_subj': False,
        # 'see_room': False,
    }
    
    from inspect import getmembers, isfunction
    functions_list = [o for o in getmembers(conditions) if isfunction(o[1])]
    for item in functions_list:
        if 'condition' in item[0]:
            CONDITIONS.append(item[1])
    
    
    init_specs(config.get('see_subj'), config.get('see_room'))
    
    if config.get('rooms_count'):
        print(f'rooms_count = {rooms_count}')
        
    get_rooms_ids()
    subj_list, log, err = gen_subj_list()
    
    if config.get('printSubjList'):
        printSubjList(subj_list)
        
    if config.get('log_OK'):
        for l in log["OK"]:
            print(l)
            
    if config.get('log_NO'):
        for l in log["NO"]:
            print(l)
    
    if config.get('err_count'): 
        print(sep)
        print(f"Ошибок: {err}")
        print(sep)

    
    # константы задачи
    ONE_MAX_LENGTH = 5*(len(subj_list))    # длина подлежащей оптимизации битовой строки
    print(f'\n=============== ONE_MAX_LENGTH = {ONE_MAX_LENGTH} ===============')

    # константы генетического алгоритма
    POPULATION_SIZE = 10   # количество индивидуумов в популяции
    P_CROSSOVER = 0.9       # вероятность скрещивания
    P_MUTATION = 0.3        # вероятность мутации индивидуума
    MAX_GENERATIONS = 100    # максимальное количество поколений
    HALL_OF_FAME_SIZE = 2

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    RANDOM_SEED = 42
    random.seed(RANDOM_SEED)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()

    toolbox.register("rndIndivid", createIndivid, subj_list)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.rndIndivid)

    population = toolbox.populationCreator(n=POPULATION_SIZE)
    
    toolbox.register("evaluate", oneMaxFitness)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", mutTT, indpb=1.0/ONE_MAX_LENGTH)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)

    population, logbook = algorithms.eaSimple(population, toolbox,
                                            cxpb=P_CROSSOVER,
                                            mutpb=P_MUTATION,
                                            ngen=MAX_GENERATIONS,
                                            halloffame=hof,
                                            stats=stats,
                                            verbose=config.get('print_info'))

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    best = hof.items[0]
    # best = population[0]
    
    if config.get('timetable'):
        printTT(best)
        
    if config.get('check_best'):
        s = 0
        count = 1
        text = ''
        
        for cond in CONDITIONS:
            i, check = cond(best)
            text += f'\t check{count} = {check} \n'
            count += 1
            s += i

        text += f'\t s = {s}'
        print(text)
        
    if config.get('graph'):
        plt.plot(maxFitnessValues, color='red')
        plt.plot(meanFitnessValues, color='green')
        plt.xlabel('Поколение')
        plt.ylabel('Макс/средняя приспособленность')
        plt.title('Зависимость максимальной и средней приспособленности от поколения')
        plt.show()
    
    timetable = group(best, 5)
    return timetable