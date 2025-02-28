FROM python:3.11-slim

WORKDIR /cafe

COPY ./requirements.txt /cafe/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

WORKDIR /cafe/cafe

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py fulldb &&python manage.py runserver 0.0.0.0:8000"]
