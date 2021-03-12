FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /code/

CMD ["gunicorn", "--bind", ":8000", "--workers", "8", "remusgold.wsgi:application"]
