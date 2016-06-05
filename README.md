This is the code that runs:

[themortgagemeter.com](http://themortgagemeter.com)

Requirements:
=============

For Using:
==========

- docker

then:

```sh
cd themortgagemeter
vi Dockerfile
```

Update items where it says TODO (see Config below)

```sh
docker build --no-cache .
```

For Development
===============

- python

- pip / python-pip

- [ShutIt](https://github.com/ianmiell/shutit) [More here](http://ianmiell.github.io/shutit/)



eg on 14.04 ubuntu:

```sh
apt-get update
apt-get install -y docker.io python-pip
sudo pip install shutit
mkdir -p ~/.shutit && touch ~/.shutit/config && chmod 600 ~/.shutit/config 
vi ~/.shutit/config
```


Set up ~/.shutit/config with:


Config:
=======
```
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
```
