#FROM python:3.8-slim-buster
#FROM ubuntu
FROM apache1
WORKDIR /app-sgn
RUN apt update
RUN apt install -y default-libmysqlclient-dev python3-dev build-essential python3 python3-pip iptables curl sudo
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate
CMD [ "python3" , "manage.py" , "runserver" , "0.0.0.0:8080" ]
