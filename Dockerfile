FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
