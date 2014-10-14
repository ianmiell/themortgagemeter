FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y -qq curl git python-pip
WORKDIR /opt
RUN git clone https://github.com/ianmiell/shutit.git
WORKDIR /opt/shutit
RUN pip install -r requirements.txt

ENV HOME /root

RUN mkdir /opt/themortgagemeter
ADD . /opt/themortgagemeter

RUN mkdir ~/.shutit
RUN touch ~/.shutit/config
RUN chmod 600 ~/.shutit/config
RUN echo "[com.themortgagemeter.setup]" >> ~/.shutit/config

################################################################################
# Fill this in appropriately and delete this line
# Git repository to clone the code from within the container. We will run
# git clone [this value]
RUN echo "gitrepo:https://github.com/ianmiell/themortgagemeter.git" >> ~/.shutit/config
# Git password for pushing changes up (only needed if required)
#RUN echo "#gitpassword:mygitpass" >> ~/.shutit/config
# Email to send emails
RUN echo "senderemail:ian.miell@gmail.com" >> ~/.shutit/config
# Password for senderemail account
RUN echo "mailpass:mymailpass" >> ~/.shutit/config
# Administrative email account (ie mail to send alerts etc to)
RUN echo "adminemail:ian.miell@gmail.com" >> ~/.shutit/config
# Your site's domain name, eg themortgagemeter.com
RUN echo "sitename:themortgagemeter.com" >> ~/.shutit/config
# This value will be the root password for your container
RUN echo "containerpass:rootpass" >> ~/.shutit/config
# CONFIG SECTION COMPLETE
################################################################################

WORKDIR /opt/themortgagemeter/docker/shutit/shutit_modules/com/themortgagemeter
RUN /opt/shutit/shutit build --shutit_module_path /opt/shutit/library --delivery dockerfile

CMD ["/bin/bash"]

