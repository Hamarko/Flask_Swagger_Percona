FROM python:3.6
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/

CMD gunicorn -w 3 -b 0.0.0.0:5000 -t 600 --reload wsgi:app


