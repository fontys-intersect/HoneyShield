FROM python:latest

RUN useradd -rm -d /home/listener -s /bin/bash -u 1001 -p "$(openssl passwd -1 listener)" listener
USER listener

COPY --chown=listener:listener script /home/listener/script

WORKDIR /home/listener/script

RUN pip3 install mysql-connector-python
RUN pip3 install python-dotenv
RUN pip3 install requests
RUN pip3 install urllib3

CMD python3 /home/listener/script/listener.py