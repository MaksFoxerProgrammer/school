FROM python:3.9

COPY . /.
RUN pip install --upgrade pip && pip install -r req.txt
RUN python manage.py makemigrations
RUN echo yes | python manage.py collectstatic

ENTRYPOINT python manage.py migrate && gunicorn -b 0.0.0.0:8000 ProjectSchool.wsgi:application