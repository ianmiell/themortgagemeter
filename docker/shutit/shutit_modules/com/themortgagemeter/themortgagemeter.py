from shutit_module import ShutItModule

class themortgagemeter(ShutItModule):

	def is_installed(self,shutit):
		shutit.send('export LANG=en_US.UTF-8')
		shutit.send('locale-gen en_US.UTF-8')
		shutit.send('update-locale LANG=en_US.UTF-8')
		return False

	def build(self,shutit):
		config_dict = shutit.cfg
		shutit.install('telnet')
		shutit.install('sudo')
		shutit.send('groupadd -g 1000 themortgagemeter')
		shutit.send('useradd -g themortgagemeter -d /home/themortgagemeter -s /bin/bash -m themortgagemeter')
		shutit.send('adduser themortgagemeter sudo')
		shutit.send('echo "%sudo ALL=(ALL:ALL) ALL" > /etc/sudoers.d/sudo')
		shutit.send('chmod 0440 /etc/sudoers.d/sudo')

		shutit.send('passwd','new UNIX password:')
		shutit.send(config_dict['host']['password'],'new UNIX password:',check_exit=False)
		shutit.send(config_dict['host']['password'],check_exit=False)
		for package in ('vim','expect','linux-tools-common','linux-tools','postgresql','libpq-dev','libpostgresql-jdbc-java','python-psycopg2','xml-twig-tools','html2text','tidy','git-core','python-pip','python-html5lib','python-beautifulsoup','python-pygresql','python-bs4','python-html5lib','npm','apache2','libapache2-mod-wsgi','python-django','python-pexpect','curl','git','sysklogd','cron','linux-image-virtual'):
			shutit.install(package,timeout=1200)
		shutit.send('pip install beautifulsoup4')
		shutit.send('pip install openpyxl')
		shutit.send('chmod 777 /opt')
		shutit.login('themortgagemeter')
		shutit.send('pushd /opt')
		if shutit.send('git clone ' + shutit.cfg[self.module_id]['gitrepo'],expect=['assword',shutit.get_default_expect()],check_exit=False) == 0:
			shutit.send(config_dict[self.module_id]['gitpassword'])
		shutit.send('pushd mortgagecomparison')
		shutit.send('git submodule init')
		shutit.send('git submodule update')
		shutit.send('cd simple_mailer')
		shutit.send('git pull origin master')
		shutit.send('chmod 600 /space/mortgagecomparison/conf/mailpass')
		shutit.send('echo -n "' + shutit.cfg[self.module_id]['mailpass'] + '" > /space/mortgagecomparison/conf/mailpass')
		shutit.send("""echo "
# m h  dom mon dow   command
00 16 * * * cd /opt/mortgagecomparison/bin; ./get_mortgages.sh 2>&1 > /tmp/get_mortgages.out; cd /opt/mortgagecomparison/retrieval/emailer; python emailer.py 2>&1 > /tmp/emailer.out
00 16 * * * cd /opt/mortgagecomparison/bin; ./get_savings.sh 2>&1 > /tmp/get_savings.out
00 19 * * * (cd /opt/mortgagecomparison/bin; ./backup_db.exp) > /tmp/backupout 2>&1" | crontab -""")
		shutit.logout()
		shutit.send("perl -p -i -e 's/Require all denied/Require all granted/' /etc/apache2/apache2.conf")
		shutit.send('cp /opt/mortgagecomparison/website/apache2/sites-enabled/000-default /etc/apache2/sites-available/000-default.conf')
		shutit.send('cp /space/mortgagecomparison/website/apache2/sites-enabled/000-default /etc/apache2/sites-available/000-default.conf')
		#change the perms on the log folders to 777 (the umask is applied on creation)
		shutit.send('chmod 777 /opt/mortgagecomparison/retrieval/mortgages/logs')
		shutit.send('chmod 777 /opt/mortgagecomparison/retrieval/data/logs')
		shutit.send('touch /opt/mortgagecomparison/website/django/mortgagecomparison/logs/log.log')
		shutit.send('chmod 777 /opt/mortgagecomparison/website/django/mortgagecomparison/logs/log.log')
		##install the database
		shutit.login('postgres')
		shutit.send('psql postgres < /opt/mortgagecomparison/sql/CREATE_DATABASE.sql')
		##set the postgres and themortgagemeter password (as postgres):
		shutit.send_and_expect('/opt/mortgagecomparison/bin/create_user.sh')
		shutit.send_and_expect('psql mortgagecomparison < /opt/mortgagecomparison/sql/archive/SCHEMA_CURRENT.sql')
		shutit.send_and_expect('psql mortgagecomparison < /opt/mortgagecomparison/sql/archive/DATA_CURRENT.sql')
		shutit.logout()
		shutit.add_line_to_file('#!/bin/bash','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('/root/start_postgres.sh','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('apache2ctl restart','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('/root/start_ssh_server.sh','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('service sysklogd start','/root/start_themortgagemeter.sh')
		shutit.add_line_to_file('cron -f -L 8','/root/start_themortgagemeter.sh')
		shutit.send('chmod +x /root/start_themortgagemeter.sh')
		shutit.send('pushd /opt/mortgagecomparison')
		# The below strings are deliberately broken up to ensure we don't overwrite them ourselves :)
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/MORTGAGECOMPARISON" + "_ADMINEMAIL/" + shutit.cfg[self.module_id]['adminemail'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/MORTGAGECOMPARISON" + "_SENDEREMAIL/" + shutit.cfg[self.module_id]['senderemail'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/MORTGAGECOMPARISON" + "_SITENAME/" + shutit.cfg[self.module_id]['sitename'] + "/g'")
		shutit.send("find . -type f -print0 | xargs -0 sed -i 's/MORTGAGECOMPARISON" + "_GITPASSWORD/" + shutit.cfg[self.module_id]['gitpassword'] + "/g'")
		shutit.send('popd')
		return True

	def start(self,shutit):
		shutit.send('apache2ctl restart')
		shutit.send('service postgresql start')
		shutit.send('service sysklogd start')
		return True

	def stop(self,shutit):
		shutit.send('apache2ctl stop')
		shutit.send('service postgresql stop')
		shutit.send('service sysklogd stop')
		return True

	def get_config(self, shutit):
		cp = shutit.cfg['config_parser']
		shutit.cfg[self.module_id]['gitpassword'] = cp.get(self.module_id,'gitpassword','defaultpass')
		shutit.cfg[self.module_id]['gitrepo']     = cp.get(self.module_id,'gitrepo')
		shutit.cfg[self.module_id]['mailpass']    = cp.get(self.module_id,'mailpass')
		shutit.cfg[self.module_id]['adminemail']   = cp.get(self.module_id,'adminemail')
		shutit.cfg[self.module_id]['senderemail']  = cp.get(self.module_id,'senderemail')
		shutit.cfg[self.module_id]['sitename']     = cp.get(self.module_id,'sitename')
		return True

	def test(self, shutit):
		return True

def module():
		return themortgagemeter(
				'com.themortgagemeter.setup', 1003189494.56,
				description='Builds the mortgage comparison site',
				depends=['shutit.tk.setup','shutit.tk.ssh_server.ssh_server','shutit.tk.postgres.postgres','shutit.tk.phantomjs.phantomjs','shutit.tk.casperjs.casperjs']
		)


