FROM python:latest

RUN useradd -rm -d /home/flask -s /bin/bash -u 1001 -p "$(openssl passwd -1 flask)" flask
USER flask

COPY --chown=flask:flask site /home/flask/site

RUN mkdir /home/flask/ssl
WORKDIR /home/flask/ssl
RUN openssl req -x509 -days 3650 -nodes \
    -keyout cert.key -out cert.crt -newkey rsa:4096 \
    -subj "/C=NL/ST=Eindhoven/O=HoneyShield Industrial Inc/CN=HoneyShield"

WORKDIR /home/flask/site

ENV SSL_KEY=/home/flask/ssl/cert.key
ENV SSL_CRT=/home/flask/ssl/cert.crt

RUN pip3 install flask
RUN pip3 install mysql-connector-python
RUN pip3 install gevent
RUN pip3 install python-dotenv
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install folium
RUN pip3 install matplotlib
RUN pip3 install mpld3
RUN pip3 install SQLAlchemy
RUN pip3 install PyMySQL

EXPOSE 5000/tcp

CMD python3 app.py
