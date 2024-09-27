from itertools import count
from tabnanny import check
from deap import base, algorithms
from deap import creator
from deap import tools

import random
import matplotlib.pyplot as plt
import numpy as np

from prettytable import PrettyTable  # Импортируем установленный модуль.
# from timetable.models import TrainingCalendar, Class_Subjects
from ..models import (
    TrainingCalendar, 
    Class_Subjects,
    Room,
    Subjects,
    TeacherProfile,
    nClass,
)


def group(iterable, count):
    """ Группировка элементов последовательности по count элементов """
    return zip(*[iter(iterable)] * count)


# Получим список занятий, который останется
# только расфосовать по координатам места и времени.
def gen_u(teachers, tr_cal):
    Z = []
    log = []
    err = 0
    count = 0
    # По всему уч плану
    for up in tr_cal:
        # По часам в записи
        for i in range(0, up.time_total):
            # найдем препода, который может это вести
            checkError = True
            for teacher in teachers:
                if teacher.subject == up.subj and teacher.nclass == up.ncls:
                    app = [count, up.ncls, up.subj, teacher]
                    Z.append(app)

                    checkError = False
                    # log.append(f'Получилось: {count, up.ncls, up.subj, teacher}')
                    count += 1
            if checkError:
                log.append(f'Нет учителя у {up.ncls} для {up.subj}')
                err += 1
    return Z, log, err


def gen_u_2():
    pass




# def printTest():
sep = "================================="
teachers = Class_Subjects.objects.all()
tr_cal = TrainingCalendar.objects.all()

Z, log, err = gen_u(teachers, tr_cal)
for l in log:
    print(l)
print(sep)
print(f"Ошибок: {err}")
    
    
    
# Тут оценить качество расписания
def oneMaxFitness(individual):
    """
    Необходимые проверки:
    * 1. Нет одновременных занятий у одной группы
    * 2. Нет одновременных занятий у одного препода
    * 3. Нет одновременных занятий в одной аудитории
    """
    
    s = 0
    timetable = group(individual, 6)
    G = nClass.objects.all()
    T = TeacherProfile.objects.all()
    A = Room.objects.all()
    
    
    
    check_group = []
    # Проверка на первое условие
    # Сверяем каждую группу
    for Gr in G:
        # Перебираем сетку расписания
        for ind in timetable:
            # Если группа в сетке та, которую мы првоеряем
            if ind[1] == Gr["id"]:
                # Если это время встречается впервые
                if ind[4] not in check_group:
                    check_group.append(ind[4])
                    s += 1
                # Если одновременные занятия у одной группы - штраф
                else:
                    s -= 100
    
    
    check_teacher = []
    # Проверка на второе условие
    # Сверяем каждого препода
    for teacher in T:
        # Перебираем сетку расписания
        for ind in timetable:
            # Если препод в секти тот, которого мы првоеряем
            if ind[3] == teacher["id"]:
                # Если это время встречается впервые
                if ind[4] not in check_teacher:
                    check_teacher.append(ind[4])
                    s += 1
                # Если одновременные занятия у одного препода - штраф
                else:
                    s -= 100


    check_room = []
    # Проверка на третье условие
    # Сверяем каждую аудиторию
    for room in A:
        # Перебираем сетку расписания
        for ind in timetable:
            # Если ауд. в секти та, которую мы првоеряем
            if ind[5] == room["id"]:
                # Если это время встречается впервые
                if ind[4] not in check_room:
                    check_room.append(ind[4])
                    s += 1
                # Если одновременные занятия в одной аудитории - штраф
                else:
                    s -= 100
                    
    return s, # кортеж



# константы задачи
ONE_MAX_LENGTH = 6*(len(Z))    # длина подлежащей оптимизации битовой строки
print(f'\n=============== ONE_MAX_LENGTH = {ONE_MAX_LENGTH} ===============')

# константы генетического алгоритма
POPULATION_SIZE = 3   # количество индивидуумов в популяции
P_CROSSOVER = 0.9       # вероятность скрещивания
P_MUTATION = 0.1        # вероятность мутации индивидуума
MAX_GENERATIONS = 50    # максимальное количество поколений
HALL_OF_FAME_SIZE = 1

hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


# !Создать расписание
def createIndivid(lessons):
    tt = []
    for lesson in lessons:
        count = lesson[0]
        gr = lesson[1]["id"]
        disc = lesson[2]["id"]
        teacher = lesson[3]["id"]
        time = random.randint(1, 35)
        room = random.randint(0, len(A)-1)
        print(f'time: {time}, room: {room}')
        iter = [count, gr, disc, teacher, time, room]
        tt.extend(iter)
        
    # print(tt, len(tt))
    return creator.Individual(tt)




toolbox = base.Toolbox()

toolbox.register("rndIndivid", createIndivid, Z)
# toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.rndIndivid, ONE_MAX_LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.rndIndivid)

population = toolbox.populationCreator(n=POPULATION_SIZE)


def mutTT(individual, indpb):
    for i, ind in enumerate(individual):
        if i % 4 == 0:
            # print("PING ... ", end="")
            if random.random() < indpb:
                print("MUTATE TIME!")
                individual[4] = random.randint(1, 35)
            # else:
            #     print("NO")
        if i % 5 == 0:
            if random.random() < indpb:
                print("MUTATE ROOM!")
                individual[5] = random.randint(0, len(A))
    return individual,





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
                                        verbose=True)

maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

best = hof.items[0]
print(best)



def printTT(timetable):
    """Распечатать расписание"""
    
    newtt = []
    tt = group(timetable, 6)
    for i in tt:
        a1 = i[0]
        a2 = G[i[1]]["title"]
        a3 = D[i[2]]["title"]
        a4 = T[i[3]]["name"]
        a5 = i[4]
        a6 = A[i[5]]["title"]
        # print(f'{a1}\t{a2}\t\t{a3}\t\t\t{a4}\t{a5}\t{a6}\t')
        newtt.extend([a1, a2, a3, a4, a5, a6])
        
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


printTT(best)


plt.plot(maxFitnessValues, color='red')
plt.plot(meanFitnessValues, color='green')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()















