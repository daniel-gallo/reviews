FROM python:3.10-alpine

WORKDIR reviews

COPY flaskr .
COPY requirements.txt .
# development.sqlite will not be used in production
COPY development.sqlite .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 app:app