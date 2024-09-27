from itertools import count
from tabnanny import check
from deap import base, algorithms
from deap import creator
from deap import tools

import random
import matplotlib.pyplot as plt
import numpy as np

from prettytable import PrettyTable  # Импортируем установленный модуль.
from ..models import (
    TrainingCalendar, 
    Class_Subjects,
    Room,
    Subjects,
    TeacherProfile,
    nClass,
)

A = [
    {"id": 0, "title": "A0", "Counts": 30, "dop": []},
    {"id": 1, "title": "A1", "Counts": 30, "dop": []},
    {"id": 2, "title": "A2", "Counts": 300, "dop": ["Sport", ]},
    {"id": 3, "title": "A3", "Counts": 30, "dop": []},
    {"id": 4, "title": "A4", "Counts": 30, "dop": []},
]
G = [
    {"id": 0, "title": "11a", "Students": 20 },
    {"id": 1, "title": "1б", "Students": 20 },
    {"id": 2, "title": "1а", "Students": 20 },
]
D = [
    {"id": 0, "title": "Математика", "Dop": [] },
    {"id": 1, "title": "Физкультура", "Dop": ["Sport", ] },
    {"id": 2, "title": "Русский", "Dop": [] },
    {"id": 3, "title": "Химия", "Dop": [] },
    {"id": 4, "title": "Биология", "Dop": [] },
    {"id": 5, "title": "Английский", "Dop": [] },
    {"id": 6, "title": "Физика", "Dop": [] },
    {"id": 7, "title": "География", "Dop": [] },
    {"id": 8, "title": "Общество", "Dop": [] },
]
T = [
    {
        "id": 0, 
        "name": "Иванов ИИ", 
        "available": [ 
            {"Gr": G[0], "Disc": D[0]},
            {"Gr": G[0], "Disc": D[1]},
            {"Gr": G[0], "Disc": D[2]},
            {"Gr": G[0], "Disc": D[3]},
            {"Gr": G[0], "Disc": D[4]},
        ]
    },
    {
        "id": 1, 
        "name": "петров ПП", 
        "available": [ {"Gr": G[1], "Disc": D[1]} ]
    },
    {
        "id": 2, 
        "name": "Сидоров СС", 
        "available": [ 
            {"Gr": G[2], "Disc": D[2]},
            {"Gr": G[2], "Disc": D[3]},
            {"Gr": G[2], "Disc": D[4]},
        ]
    },
]
UP = [
    {
        "id": 0, 
        "Gr": G[0], 
        "Disc": D[0], 
        "time": 6
    },
    {
        "id": 1, 
        "Gr": G[0], 
        "Disc": D[1], 
        "time": 1
    },
    {
        "id": 1, 
        "Gr": G[0], 
        "Disc": D[2], 
        "time": 3
    },
    {
        "id": 1, 
        "Gr": G[0], 
        "Disc": D[3], 
        "time": 3
    },
    {
        "id": 1, 
        "Gr": G[0], 
        "Disc": D[4], 
        "time": 3
    },
    {
        "id": 2, 
        "Gr": G[1], 
        "Disc": D[1], 
        "time": 15
    },
    {
        "id": 3, 
        "Gr": G[2], 
        "Disc": D[2], 
        "time": 3
    },
    # {
    #     "id": 3, 
    #     "Gr": G[2], 
    #     "Disc": D[3], 
    #     "time": 3
    # },
    # {
    #     "id": 3, 
    #     "Gr": G[2], 
    #     "Disc": D[4], 
    #     "time": 8
    # },
]

rooms = Room.objects.all()
classes = nClass.objects.all()
subjects = Subjects.obj.all()
teachers = TeacherProfile.objects.all()
tr_cal = TrainingCalendar.objects.all()

A = []
for room in rooms:
    dops = room.spec.all()
    dop_list = []
    for i in dops:
        dop_list.append(i.pk)
    app = {
        "id": room.id,
        "title": room.numb,
        "Counts": room.count,
        "dop": dop_list
    }
    # print(app)
    A.append(app)  
    
G = []
for cls in classes:
    app = {
        "id": cls.id,
        "title": cls.title,
        "Students": cls.size,
    }
    print(app)
    G.append(app)

D = []
for subj in subjects:
    dops = subj.spec.all()
    dop_list = []
    for i in dops:
        dop_list.append(i.pk)
    app = {
        "id": subj.id,
        "title": subj.title,
        "Dop": dop_list
    }
    # print(app)
    D.append(app)

T = []
for teacher in teachers:
    cl_sub = Class_Subjects.objects.filter(teacher=teacher).all()
    dop = []
    for item in cl_sub:
        dop.append({
            "Gr": item.nclass.pk, 
            "Disc": item.subject.pk
        })
    
    app = {
        "id": teacher.id,
        "name": teacher.user.username,
        "available": dop
    }
    # print(app, end="\n\n===================\n\n")
    T.append(app)

UP = []
for item in tr_cal:
    app = {
        "id": item.pk, 
        "Gr": item.ncls.pk, 
        "Disc": item.subj.pk, 
        "time": item.time_total
    }
    # print(app)
    UP.append(app)


def get_for_id(lst, id):
    for dct in lst:
        if dct["id"]==id:
            return dct.index
    raise




def group(iterable, count):
    """ Группировка элементов последовательности по count элементов """
    return zip(*[iter(iterable)] * count)


# Получим список занятий, который останется 
# только расфосовать по координатам места и времени.
def gen_u(UP, T):
    Z = []
    log = []
    err = 0
    count = 0
    # print(f"\n\n\t\t UP === {UP} --------------> Должен поступать!!!\n\n")
    # По всему уч плану
    for up in UP:
        # print(f'up = {up}')
        disc = D[up["Disc"]]["title"]
        group = G[up["Gr"]]["title"]
        # group = G[get_for_id(up, )]
        print(f'disc = {disc} \t group = {group}')
        # По часам в записи
        for i in range(0, up["time"]):
            # найдем препода, который может это вести
            checkError = True
            for teacher in T:
                # Теперь посмотрим все, что ведет этот препод
                for item in teacher["available"]:
                    # print(f'item["Disc"] = {item["Disc"]}, up["Disc"] = {up["Disc"]} ---- item["Gr"] = {item["Gr"]}, up["Gr"] = {up["Gr"]}')
                    if item["Disc"] == up["Disc"] and item["Gr"] == up["Gr"]:
                        app = [count, up["Gr"], up["Disc"], teacher["id"]]
                        # print(f'app = {app}')
                        Z.append(app)
                        
                        checkError = False
                        
                        # print(f'\n\n\t\t  group =  {group}  \n\n')  # Это для корректного вывода названия группы по учебному плану
                        
                        log.append(f'Получилось: {count, group, disc, teacher["name"]}')
                        # log.append(f'Получилось: {count}, {up["Gr"]["title"]}, {up["Disc"]["title"]}, {teacher["name"]}')
                        count += 1
            if checkError:
                log.append(f'Нет учителя у {group} для {disc}')
                err += 1
    return Z, log, err
  
  
def gen_u2(UP, T):
    Z = []
    log = []
    err = 0
    count = 0
    
    # По всему уч плану
    for up in UP:
        up_disc_id = up["Disc"]#["id"]
        up_group_id = up["Gr"]#["id"]
        # print(f'up_disc_id = {up_disc_id} \t up_group_id = {up_group_id}')
        
        # disc = D[up["Disc"]]["title"]
        # group = G[up["Gr"]]["title"]
        
        print(f'\t\t\tget_for_id(G, up_group_id)["id"] = {get_for_id(G, up_group_id)["id"]}')
        disc = D[  get_for_id(D, up_disc_id)["id"]  ]["title"]
        group = G[  get_for_id(G, up_group_id)["id"]  ]["title"]
        
        print(f'disc = {disc} \t group = {group}')
        # По часам в записи
        for i in range(0, up["time"]):
            # найдем препода, который может это вести
            checkError = True
            for teacher in T:
                # Теперь посмотрим все, что ведет этот препод
                for item in teacher["available"]:
                    # print(f'item["Disc"] = {item["Disc"]}, up["Disc"] = {up["Disc"]} ---- item["Gr"] = {item["Gr"]}, up["Gr"] = {up["Gr"]}')
                    if item["Disc"] == up["Disc"] and item["Gr"] == up["Gr"]:
                        app = [count, up["Gr"], up["Disc"], teacher["id"]]
                        # print(f'app = {app}')
                        Z.append(app)
                        
                        checkError = False
                        
                        # print(f'\n\n\t\t  group =  {group}  \n\n')  # Это для корректного вывода названия группы по учебному плану
                        
                        log.append(f'Получилось: {count, group, disc, teacher["name"]}')
                        # log.append(f'Получилось: {count}, {up["Gr"]["title"]}, {up["Disc"]["title"]}, {teacher["name"]}')
                        count += 1
            if checkError:
                log.append(f'Нет учителя у {group} для {disc}')
                err += 1
    return Z, log, err
  
  
  
# def printTest():
sep = "================================="     
Z, log, err = gen_u2(UP, T)
print(f'Z = {Z}')
print(f'log = {log}')
print(f'err = {err}')

for l in log:
    print(l)
print(sep)
# for z in Z:
#     print(z)
# print(sep)
print(f"Ошибок: {err}")

# printTest()


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









"""# Создать расписание
def getlen(lessons):
    count = 0
    for lesson in lessons:
        count = lesson[0]
        gr = lesson[1]["id"]
        disc = lesson[2]["id"]
        teacher = lesson[3]["id"]
        time = random.randint(1, 35)
        room = random.randint(0, len(A)-1)
        # print(f'time: {time}, room: {room}')
        iter = [count, gr, disc, teacher, time, room]
        count+=1
    return count


tt = getlen(Z)"""


# константы задачи
ONE_MAX_LENGTH = 6*(len(Z))    # длина подлежащей оптимизации битовой строки

print(f'ONE_MAX_LENGTH = {ONE_MAX_LENGTH}')
print(f'len(Z) = {len(Z)}')


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


# Создать расписание
def createIndivid(lessons):
    tt = []
    for lesson in lessons:
        count = lesson[0]
        gr = lesson[1]["id"]
        disc = lesson[2]["id"]
        teacher = lesson[3]["id"]
        time = random.randint(1, 35)
        room = random.randint(0, len(A)-1)
        # print(f'time: {time}, room: {room}')
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
