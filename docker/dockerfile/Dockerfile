FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y -qq curl git python-pip
WORKDIR /opt
RUN git clone https://github.com/ianmiell/shutit.git
WORKDIR /opt/shutit
RUN pip install -r requirements.txt

WORKDIR /opt
RUN git clone https://github.com/ianmiell/themortgagemeter.git

WORKDIR /opt/themortgagemeter/docker/shutit/shutit_modules/com/themortgagemeter
RUN /opt/shutit/shutit build -m /opt/shutit/library --interactive 0 -s build conn_module shutit.tk.conn_bash

CMD ["/bin/bash"]

