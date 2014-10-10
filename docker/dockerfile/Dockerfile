FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y -qq curl git python-pip
WORKDIR /opt
RUN git clone https://github.com/ianmiell/shutit.git
WORKDIR /opt/shutit
RUN pip install -r requirements.txt

WORKDIR /opt
RUN git clone https://github.com/ianmiell/themortgagemeter.git

ENV HOME /root

RUN mkdir ~/.shutit
RUN touch ~/.shutit/config
RUN chmod 600 ~/.shutit/config
RUN echo "[com.themortgagemeter.setup]" >> ~/.shutit/config

# Delete the TODOs, and this line when you've filled this in
TODO RUN echo "#gitpassword:OPTIONAL - YOUR GIT PASSWORD HERE" >> ~/.shutit/config
TODO RUN echo "gitrepo:YOUR GIT CLONE URL" >> ~/.shutit/config
TODO RUN echo "senderemail:YOUR SITE SENDER EMAIL ACCOUNT" >> ~/.shutit/config
TODO RUN echo "mailpass:YOUR MAIL SENDER ACCOUNT PASSWORD" >> ~/.shutit/config
TODO RUN echo "adminemail:YOUR SITE ADMIN EMAIL ACCOUNT" >> ~/.shutit/config
TODO RUN echo "sitename:YOUR SITE DOMAIN NAME" >> ~/.shutit/config
TODO RUN echo "containerpassword:YOUR CONTAINER ROOT PASSWORD" >> ~/.shutit/config

WORKDIR /opt/themortgagemeter/docker/shutit/shutit_modules/com/themortgagemeter
RUN /opt/shutit/shutit build --shutit_module_path /opt/shutit/library --delivery bash

CMD ["/bin/bash"]

