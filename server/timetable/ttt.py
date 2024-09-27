import os

data = {
	"class": {
		"5a": {
			"id": 1,
			"count_people": 30, 
			"lessons": {
				"математика": {
					"count_lessons": 20
				},
				"русский": {
					"count_lessons": 10
				}
			}
		},
		"8b": {
			"id": 1,
			"count_people": 30, 
			"lessons": {
				"математика": {
					"count_lessons": 20
				},
				"русский": {
					"count_lessons": 10
				}
			}
		}
	},


	"rooms": {
		"240": {
			"count": 40,
			"spec": ""
		},
		"150": {
			"count": 35,
			"spec": "",
		},
	},


	"teachers": {
		"Olga Dmitrievna": {
			"id": 1,

			"para": {
				"8a": {
					"Химия": {
						"room": 250,
						"dey": {
							"d1": {
								"numb_of_less": [2, 3]
							},
						},
					}
				}
			},


			
			"dop": ["кружок 3D-моделирования", ],
		},

		"Dmitriy Olegovich": {
			"id": 1,

			"para": [
				{
					"name": "8a",
					"lesson": "Химия",
					"room": 250,
					"dey": [
						{
							"d": 1,
							"numb_of_less": [2, 3]
						},
					],

				}
			],
		},
	}
}



def sod(data, cont = ""):
	c = "  " # Регулировка вывода
	if type(data) is dict:
		for k, v in data.items():
			# print("{0}: {1}".format(k, v))
			# print("TEST: ", type(v))
			print(cont, "", k, ": ", end="")

			if type(v) is dict:
				# print("OK")
				print("{")
				sod(v, cont+c)
				print(cont, "}")

			elif type(v) is list:
				
				# print("!!!!!!!!! ", type(v))
				print("[ ")
				sod(v, cont+c)
				print(cont, "]")
			
			else:
				print(v)
		# print("")
	elif type(data) is list:
		count = 1
		for item in data:
			print(cont, "[{}]: ".format(count), "{")
			sod(item, cont+c)
			print(cont, "}")
			count += 1

	else:
		# print("IT IS n")
		print(cont, data)



def abra(data, cont = 'data/'):
	while True:
		os.system("clear")
		print(cont, end="\n\n")
		# sod(data)

		
		for item in data.keys():

			if type(data[item]) is dict:
				print("dict: " + item)

			elif type(data[item]) is list:
				print("list: " + item)

			else:
				print("item: " + item)

		# print("\n\n", cont)
		text = """
		Добро подаловать!"""
		end = """
		! - отобразить текущий индекс
		0 - выход
		'name' - выбрать элемент
		Введите для просмотра: """

		if cont == "data/class/":
			text += """
		1 - создать класс""" 

		elif cont == "data/rooms/":
			text += """
		1 - создать кабинет"""

		if cont == "data/teachers/":
			text += """
		1 - создать учителя"""

		index = input(text+end)

		# Если выходим 
		if index == "0":
			break
		

		# Класс
		elif index == "1" and cont == "data/class/":
			name = input("Введите назавние класса: ")
			count_people = int(input("Введите число учеников: "))
			data["class"][name] = dict()
			data["class"][name]["count_people"] = count_people
			data["class"][name]["lessons"] = dict()
			less = 1

			while less != "0":
				less = input("Введите название предмета (0 для завершения): ")
				if less == "0":
					break
				if less in data[name]["lessons"]:
					print("Воу, да у тебя етсь этот предмет уже!")
				else:
					h = int(input("Введите количество часов: "))
					data[name]["lessons"][less] = dict()
					data[name]["lessons"][less]["count_lessons"] = h
				# for key, value in data["class"].items():
  		# 			print("{0}: {1} \n".format(key,value))


  		# Кабиенет
		elif index == "1" and cont == "data/rooms/":
			name = input("Введите номер: ")
			count = int(input("Введите вместимость: "))
			data[name] = dict()
			data[name]["count"] = count
			data[name]["spec"] = input("Введите специализацию: ")


  		# Учитель
		elif index == "1" and cont == "data/teachers/":
			name = input("Введите ФИО: ")
			data[name] = dict()
			data[name]["para"] = dict()

			# Перечисляем классы:
			while True:
				clas = input("Введите название класса (0 - отменить): ")
				if clas == "0":
					break
				else:
					data[name]["para"][clas] = dict()

					# Перечисляем предметы
					while True:
						less = input("Введите пердмет (0 - отменить): ")
						if less == "0":
							break
						else:
							data[name]["para"][clas][less] = dict()
							data[name]["para"][clas][less]["day"] = dict()

										
							# Каинет
							room = input("Введите кабинет (0 - пропустить): ")
							if room == "0":
								pass
							else:
								data[name]["para"][clas][less]["room"] = room

							# Перечиляем дни и комнаты
							while True:
								day = input("Введите желаемый день недели (цифрой) (0 - пропустить): ")
								if day == "0":
									break
								else:
									data[name]["para"][clas][less]["day"][day] = dict()
									data[name]["para"][clas][less]["day"][day]["numb_of_less"] = list()
									while True:
										d = input("Введите желаемые номер урока (цифрой) (0 - пропустить): ")
										if d == "0":
											break
										else:
											data[name]["para"][clas][less]["day"][day]["numb_of_less"].append(d)
								


		# Вывод
		elif index == "!":
			sod(data)
			input("\n Нажмите 'Enter' для продолжения. ")				



	
		# Если у нас list
		elif type(data[index]) is list:
			print("Кол-во: ", len(data[index]))
			y = int(input("Выеберите элемент (а вообще тут в разработке): "))


		# Если словарь
		elif type(data[index]) is dict:
			print("Словарь! ")
			abra(data[index], cont + index + "/")
			

		# Если значение
		else:
			print(index, " = ", data[index])
			r = input("""
		Выберете 1 для изменения значения (чило)
		Выберете 2 для изменения значения (строка)
		Выберете 0 для выхода
		Выбор: """)
			if r == "1":
				change = int(input("Введите чило: "))
				data[index] = change


			if r == "2":
				change = input("Введите значение: ")
				data[index] = change


			if r == "0":
				pass




abra(data)