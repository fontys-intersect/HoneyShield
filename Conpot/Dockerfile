FROM ubuntu:20.04

RUN apt update
RUN apt upgrade -y
RUN apt install sudo -y
RUN apt install nano -y

RUN useradd -rm -d /home/conpot -s /bin/bash -g root -G sudo -u 1001 -p "$(openssl passwd -1 conpot)" conpot
USER conpot
WORKDIR /home/conpot

RUN sudo apt install systemctl -y
RUN sudo apt install curl -y
RUN sudo apt install git -y
RUN git clone --quiet https://github.com/mushorg/conpot.git
COPY conpot.cfg /home/conpot/conpot.cfg

WORKDIR /home/conpot/conpot/
RUN sudo apt update
RUN sudo apt install python3-pip -y
RUN sudo pip3 install -r requirements.txt
RUN sudo pip3 install sphinx==6.1.3
RUN sudo python3 setup.py install

RUN sudo sed -i 's/port="2121"/port="21"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/ftp/ftp.xml
RUN sudo sed -i 's/port="8800"/port="80"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/http/http.xml
RUN sudo sed -i 's/port="6230"/port="623"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/ipmi/ipmi.xml
RUN sudo sed -i 's/port="5020"/port="502"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/modbus/modbus.xml
#Make conpot instance invisible for Shodan
RUN sudo sed -i 's/<MajorMinorRevision>S7-200<\/MajorMinorRevision>/<MajorMinorRevision>S7-300<\/MajorMinorRevision>/g' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/modbus/modbus.xml
RUN sudo sed -i 's/<starting_address>1<\/starting_address>/<starting_address>1002<\/starting_address>/g' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/modbus/modbus.xml
RUN sudo sed -i 's/<size>128<\/size>/<size>31<\/size>/g' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/modbus/modbus.xml
RUN sudo sed -i 's/port="10201"/port="102"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/s7comm/s7comm.xml
RUN sudo sed -i 's/port="16100"/port="161"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/snmp/snmp.xml
RUN sudo sed -i 's/port="6969"/port="69"/' /usr/local/lib/python3.8/dist-packages/conpot-0.6.0-py3.8.egg/conpot/templates/default/tftp/tftp.xml
RUN sudo apt install libcap2-bin -y
RUN sudo setcap cap_net_bind_service=+ep /usr/bin/python3.8

RUN mkdir -p /tmp/conpot
RUN sudo chmod 777 /tmp/conpot
RUN sudo usermod -aG staff conpot
RUN sudo usermod -aG sudo conpot
RUN sudo chmod -R 775 /usr/local/lib/python3.8/dist-packages/
RUN mkdir -p /home/conpot/log
RUN chown conpot:root /home/conpot/log

WORKDIR /home/conpot

EXPOSE 80/tcp
EXPOSE 102/tcp
EXPOSE 502/tcp
EXPOSE 161/udp
EXPOSE 47808/udp
EXPOSE 623/udp
EXPOSE 21/tcp
EXPOSE 69/udp
EXPOSE 44818/tcp

CMD conpot --template default --temp_dir /tmp/conpot --logfile /home/conpot/log/conpot.log --config /home/conpot/conpot.cfg