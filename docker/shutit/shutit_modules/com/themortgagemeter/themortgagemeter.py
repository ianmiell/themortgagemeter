from shutit_module import ShutItModule

class themortgagemeter(ShutItModule):

	def is_installed(self,shutit):
		shutit.send('export LANG=en_US.UTF-8')
		shutit.send('locale-gen en_US.UTF-8')
		shutit.send('update-locale LANG=en_US.UTF-8')
		return False

	def build(self,shutit):
		config_dict = shutit.cfg
		shutit.install('adduser')
		shutit.install('cron')
		shutit.install('sudo')
		shutit.install('telnet')
		shutit.install('openssh-server')
		shutit.send('mkdir -p /var/run/ssh')
		shutit.send('groupadd -g 1000 themortgagemeter')
		shutit.send('useradd -g themortgagemeter -d /home/themortgagemeter -s /bin/bash -m themortgagemeter')
		shutit.send('adduser themortgagemeter sudo')
		shutit.send('echo "%sudo ALL=(ALL:ALL) ALL" > /etc/sudoers.d/sudo')
		shutit.send('chmod 0440 /etc/sudoers.d/sudo')
		shutit.send("""echo "
# m h  dom mon dow   command
00 16 * * * cd /opt/themortgagemeter/bin && ./get_mortgages.sh 2>&1 > /tmp/get_mortgages.out && cd /opt/themortgagemeter/retrieval/emailer && python emailer.py 2>&1 > /tmp/emailer.out
00 16 * * * cd /opt/themortgagemeter/bin && ./get_savings.sh 2>&1 > /tmp/get_savings.out
00 19 * * * (cd /opt/themortgagemeter/bin && ./backup_db.exp) > /tmp/backupout 2>&1" | crontab -u themortgagemeter -""")
		shutit.send('passwd','new UNIX password:')
		shutit.send(config_dict[self.module_id]['containerpass'],'new UNIX password:',check_exit=False)
		shutit.send(config_dict[self.module_id]['containerpass'],check_exit=False)
		# prevent grub from being installed
		shutit.send('echo "Package: grub-pc" >> /etc/apt/preferences')
		shutit.send('echo "Pin: release *" >> /etc/apt/preferences')
		shutit.send('echo "Pin-Priority: -1" >> /etc/apt/preferences')
		shutit.install('linux-image-virtual',timeout=1200)
		shutit.install('vim expect linux-tools-common linux-tools-virtual postgresql libpq-dev libpostgresql-jdbc-java python-psycopg2 xml-twig-tools html2text tidy git-core python-pip python-html5lib python-beautifulsoup python-pygresql python-bs4 python-html5lib npm apache2 libapache2-mod-wsgi python-django python-pexpect curl git busybox-syslogd cron',timeout=2400)
		shutit.send('pip install beautifulsoup4')
		shutit.send('pip install openpyxl')
		shutit.send('chmod 777 /opt')
		if shutit.file_exists('/opt/themortgagemeter'):
			shutit.send('rm -rf /opt/themortgagemeter')
		shutit.login('themortgagemeter')
		# If we're delivering within a dockerfile this will already have been added
		if not shutit.file_exists('/opt/themortgagemeter'):
			shutit.send('cd /opt')
			if shutit.send('git clone ' + shutit.cfg[self.module_id]['gitrepo'] + ' themortgagemeter',expect=['assword',shutit.get_default_expect()],check_exit=False) == 0:
				shutit.send(config_dict[self.module_id]['gitpassword'])
		shutit.pause_point('')
		shutit.send('cd /opt/themortgagemeter')
		shutit.send('git submodule init')
		shutit.send('git submodule update')
		shutit.send('cd /opt/themortgagemeter/simple_mailer')
		shutit.send('git pull origin master')
		shutit.send('chmod 600 /opt/themortgagemeter/conf/mailpass')
		shutit.send('echo -n "' + shutit.cfg[self.module_id]['mailpass'] + '" > /opt/themortgagemeter/conf/mailpass')
		shutit.logout()
		shutit.send("perl -p -i -e 's/Require all denied/Require all granted/' /etc/apache2/apache2.conf")
		shutit.send('cp /opt/themortgagemeter/website/apache2/sites-enabled/000-default /etc/apache2/sites-available/000-default.conf')
		shutit.send('cp /opt/themortgagemeter/website/apache2/sites-enabled/000-default /etc/apache2/sites-available/000-default.conf')
		#change the perms on the log folders to 777 (the umask is applied on creation)
		shutit.send('chmod 777 /opt/themortgagemeter/retrieval/mortgages/logs')
		shutit.send('chmod 777 /opt/themortgagemeter/retrieval/data/logs')
		shutit.send('mkdir -p /opt/themortgagemeter/website/django/themortgagemeter/logs')
		shutit.send('touch /opt/themortgagemeter/website/django/themortgagemeter/logs/log.log')
		shutit.send('chmod 777 /opt/themortgagemeter/website/django/themortgagemeter/logs')
		shutit.send('chmod 777 /opt/themortgagemeter/website/django/themortgagemeter/logs/log.log')
		##install the database
		shutit.login('postgres')
		shutit.send('psql postgres < /opt/themortgagemeter/sql/CREATE_DATABASE.sql')
		##set the postgres and themortgagemeter password (as postgres):
		shutit.send_and_expect('/opt/themortgagemeter/bin/create_user.sh')
		shutit.send('psql themortgagemeter < /opt/themortgagemeter/sql/archive/SCHEMA_CURRENT.sql')
		shutit.send('psql themortgagemeter < /opt/themortgagemeter/sql/archive/DATA_CURRENT.sql')
		shutit.logout()
		shutit.add_line_to_file('#!/bin/bash','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('/root/start_postgres.sh','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('apache2ctl restart','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('service ssh start','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('service busybox-syslogd start','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('cron -f -L 8','/root/start_themortgagemeter.sh')
		shutit.send('chmod +x /root/start_themortgagemeter.sh')
		shutit.send('cd /opt/themortgagemeter')
		# The below strings are deliberately broken up to ensure we don't overwrite them ourselves :)
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/THEMORTGAGEMETER" + "_ADMINEMAIL/" + shutit.cfg[self.module_id]['adminemail'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/THEMORTGAGEMETER" + "_SENDEREMAIL/" + shutit.cfg[self.module_id]['senderemail'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/THEMORTGAGEMETER" + "_SITENAME/" + shutit.cfg[self.module_id]['sitename'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/THEMORTGAGEMETER" + "_GITPASSWORD/" + shutit.cfg[self.module_id]['gitpassword'] + "/g'")
		return True

	def start(self,shutit):
		shutit.send('apache2ctl restart')
		shutit.send('service postgresql start')
		shutit.send('service busybox-syslogd start')
		return True

	def stop(self,shutit):
		shutit.send('apache2ctl stop')
		shutit.send('service postgresql stop')
		shutit.send('service busybox-syslogd stop')
		return True

	def get_config(self, shutit):
		shutit.get_config(self.module_id, 'gitpassword','defaultgitpassword')
		shutit.get_config(self.module_id, 'gitrepo')
		shutit.get_config(self.module_id, 'mailpass')
		shutit.get_config(self.module_id, 'adminemail')
		shutit.get_config(self.module_id, 'senderemail')
		shutit.get_config(self.module_id, 'sitename')
		shutit.get_config(self.module_id, 'containerpass')
		print shutit.cfg
		return True

	def test(self, shutit):
		return True

def module():
	return themortgagemeter(
		'com.themortgagemeter.setup', 1003189494.56,
		description='Builds the mortgage comparison site',
		depends=['shutit.tk.setup','shutit.tk.postgres.postgres','shutit.tk.phantomjs.phantomjs','shutit.tk.casperjs.casperjs']
	)


