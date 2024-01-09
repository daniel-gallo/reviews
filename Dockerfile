FROM python:3.10-alpine

WORKDIR reviews

# development.sqlite is only present locally
COPY flaskr requirements.txt development.sqlite* ./

RUN pip install -r requirements.txt

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 app:app