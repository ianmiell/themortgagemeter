The code that runs:

themortgagemeter.com

Requirements:

python

pip

pip install -r requirements.txt

shutit

eg on 14.04 ubuntu:

apt-get update
apt-get install -y docker.io python-pip
git clone https://github.com/ianmiell/shutit.git
cd shutit
pip install -r requirements.txt 
mkdir -p ~/.shutit && touch ~/.shutit/config && chmod 600 ~/.shutit/config 
vi ~/.shutit/config


Set up ~/.shutit/config with:

# site admin's mail account for monitoring emails to be sent to
[com.themortgagemeter.setup]
# Your git repo for cloning, eg: https://user@bitbucket.org/user/themortgagemeter.git
gitrepo:
gitpassword:
mailpass:
# site admin's mail account for monitoring emails
adminemail:
# gmail account with simple auth
senderemail:
# sitename, eg yoursite.com
sitename:
