FROM python:3.9

WORKDIR /app

COPY ./srcs/ .
COPY ./includes/ .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./server.py"]