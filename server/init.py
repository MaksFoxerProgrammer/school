import os
from sys import argv

from ProjectSchool.wsgi import *
from django.contrib.auth.models import User


# commands = []

try:
    if argv[1] == '1':
        # commands.append("py manage.py runserver")
        os.system("py manage.py runserver")

    elif argv[1] == '2':
        os.system("py manage.py makemigrations")
        os.system("py manage.py migrate")
        os.system("py manage.py runserver")

    elif argv[1] == '3':
        os.system("py manage.py makemigrations")
        os.system("py manage.py migrate")
        User.objects.create_superuser('admin', 'admin@main.ru', 'admin')
        os.system("py manage.py runserver")

    elif argv[1] == '4':
        User.objects.create_superuser(argv[2], 'admin@main.ru', argv[3])

    else:
        print("Такой парметр не предусмотрен")

except IndexError:
    print("Ошибка параметра...")





