#FROM --platform=linux/amd64 python:3.11-slim
FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

CMD ["gunicorn", "-b 0.0.0.0:8000", "app.main:app"]
