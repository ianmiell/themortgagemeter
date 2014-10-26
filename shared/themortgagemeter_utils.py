# vim: set fileencoding=utf-8
# Utility functions
import urllib2
import html5lib
import re
import string
import logging
import themortgagemeter_queries
import logging
import json
import pickle
import sys
import themortgagemeter_db
import pexpect
from bs4 import BeautifulSoup

def isnumber(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def remove_non_ascii(s): return "".join(filter(lambda x: ord(x)<128, s))

# Records an error in the alert table.
# Handles rollback for you.
def record_error(s,logger,db_connection,cursor):
	logger.critical("Recording error: " + s)
	db_connection.rollback()
	record_alert(s,logger,db_connection,cursor)
	db_connection.commit()
	cursor.close()
	db_connection.close()

# Records an alert.
# Assumes transaction is ok to continue. If it later rolls back, this will be lost.
# Perhaps this could be extended to record separately.
def record_alert(s,logger,db_connection,cursor):
	logger.critical("Recording alert: " + s)
	cursor.execute(themortgagemeter_queries.insert_alert,(s,))

def setup_logging(level,stdout=False):
	# Switch basic logging to DEBUG, then send it to dev null (can't find a better way to switch off base log).
	if stdout:
		logging.basicConfig(level=level,stream=sys.stdout)
	else:
		logging.basicConfig(level=level,filename='/dev/null')
	# File to log to.
	LOG_FILENAME = 'logs/retrieve.log'
	# TODO: use TimedRotatingFileHandler?
	handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
	handler.setLevel(level)
	handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(name)-12s %(message)s'))
	# Get our logger
	logger = logging.getLogger('retrieve')
	# Add the log message handler to the logger
	logger.addHandler(handler)
	# TODOs?
	# Logging config
	#logging.config.fileConfig('conf/logging.conf')
	return logger

# Get file's contents
def get_file_contents(file_name):
	f = open(file_name)
	contents = f.read()
	f.close()
	return contents

# Gets page and returns beautiful soup object.
# tostring - just return the page as a string (for xml)
# TODO: use pexpect and phantomjs to get string
def get_page(static,static_link,url,logger,tostring=False):
	# URL
	if static:
		logger.debug('In get_page, static link: %s',(static_link))
		f = open(static_link)
		the_page = f.read()
		f.close()
	else:
		logger.info('In get_page, url: %s',(url))
		req = urllib2.Request(url)
		# Make request.
		for i in range(0,10):
			try:
				response = urllib2.urlopen(req)
			except:
				if i > 8:
					logger.critical('Giving up')
					record_alert('ERROR: Giving up retrieval',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
					exit()
				logger.critical('Failed to open url, trying again: ' + url)
				logger.exception('Error was:')
				continue
			break
		# Get 'page' content.
		the_page = response.read()
	if tostring:
		return the_page
	else:
		the_page_list = string.split(the_page,sep='\n')
		while '' in the_page_list:
			the_page_list.remove('')
		# These two stripped lines could be on one.
		if the_page_list and re.match(r'^..xml version="1.0" encoding="iso-8859-1"...*$',string.strip(the_page_list[0])):
			the_page_list = string.split(string.join(the_page_list[1:],'\n'),sep='\n')
		#print string.strip(the_page_list[0])
		if the_page_list and re.match(r'^..DOCTYPE html.*$',string.strip(the_page_list[0])):
			the_page_list = string.split(string.join(the_page_list[1:],'\n'),sep='\n')
		the_page = string.join(the_page_list,'\n')
		logger.debug("Printing the page:")
		logger.debug(the_page)
		bsobj = BeautifulSoup(the_page,'html5lib')
		return bsobj

# Pretty print json object
def pretty_print_json(json_obj):
	s = json.dumps(json_obj,indent=4)
	print '\n'.join([l.rstrip() for l in  s.splitlines()])

# Save dict to filename
# For prototyping
def pickle_dict(d, f_name):
	pickle.dump(d, open(f_name,"wb"))

def unpickle_dict(f_name):
	return pickle.load(f_name)

# Given a string, extracts a percent value as a decimal string
# Returns blank string if none could be found
# Returns first percentage.
def get_percentage(s,logger):
	logger.debug('get_percentage: ' + s)
	res = re.match(r'^.*?[\s]*([.0-9]*)%.*$',s)
	if res:
		percent_val = res.group(1)
		logger.debug('1st regexp worked: ' + s + ' percent val: ' + percent_val)
	else:
		res = re.match(r'^([.0-9]*)%.*$',s)
		if res:
			logger.debug('2nd regexp worked: ' + s)
			percent_val = res.group(1)
		else:
			logger.debug('2nd regexp failed: ' + s)
			return ''
	return percent_val

# takes a string, returns last string that matches a float
# TODO: be non-greedy, need to regression test.
def get_money(s,logger):
	logger.debug('get_money: ' + s)
	res = re.match(r'^.*[\s]+£([.,0-9k]*).*$',s)
	if res:
		money_val = res.group(1)
		money_val = re.sub('k','000',money_val)
		logger.debug('1st regexp worked: ' + s + ' money val: ' + money_val)
	else:
		res = re.match(r'^£([.,0-9k]*).*$',s)
		if res:
			logger.debug('2nd regexp worked: ' + s)
			money_val = res.group(1)
			money_val = re.sub('k','000',money_val)
		elif s == "None":
			return "0"
		else:
			logger.debug('last regexp failed: ' + s)
			return ''
	# replace commas
	money_val = re.sub(',','',money_val)
	logger.debug('money val returned as: ' + money_val)
	return money_val

# Takes string like "5 years" and returns number of months
def get_months(s,logger):
	logger.debug('get_months: ' + s)
	period_lower = s.lower()
	res = re.match(r'^[^0-9]*([0-9]+)[\s]*([yearsmonth]+).*$',remove_non_ascii(period_lower))
	num = int(res.group(1))
	period = res.group(2)
	if period == 'years' or period == 'year':
		period = num * 12
	elif period == 'months' or period == 'month':
		period = num
	else:
		logger.critical('unable to determine months from period: ' + str(period) + ' and initial_period: ' + period_lower)
		record_alert('ERROR: unable to determine months from period',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
	return period


# Takes a beautiful soup object, extracts all the anchors, fetches, and returns a 
# dictionary of the url mapped to the bs objects of the pages.
# base_url is an optional argument should the links be relative on the page.
def get_anchors_pages(bsobj,regex,logger,base_url=''):
	pages = {}
	anchors = bsobj.find_all('a')
	for a in anchors:
		href = a.get('href')
		if href and re.match(regex,href):
			url = base_url+href
			# remove hashes
			url = url.split('#')[0]
			if not pages.has_key(url):
				bsobj = get_page(False,'',url,logger)
				pages.update({url : bsobj})
	return pages

# Use phantomjs to get a page, return a bs object
def get_page_headless(url,logger):
	child         = pexpect.spawn('/bin/bash')
	#the_page = pexpect.run('/opt/phantomjs/bin/phantomjs /opt/themortgagemeter/retrieval/mortgages/phantomjs/get_url.js ' + url)
	the_page = pexpect.run('curl -3 --insecure ' + url)
	the_page_list = string.split(the_page,sep='\n')
	while '' in the_page_list:
	        the_page_list.remove('')
	# These two stripped lines could be on one.
	if the_page_list and re.match(r'^..xml version="1.0" encoding="iso-8859-1"...*$',string.strip(the_page_list[0])):
	        the_page_list = string.split(string.join(the_page_list[1:],'\n'),sep='\n')
	#print string.strip(the_page_list[0])
	if the_page_list and re.match(r'^..DOCTYPE html.*$',string.strip(the_page_list[0])):
	        the_page_list = string.split(string.join(the_page_list[1:],'\n'),sep='\n')
	the_page = string.join(the_page_list,'\n')
	logger.debug("Printing the page:")
	logger.debug(the_page)
	bsobj = BeautifulSoup(the_page,'html5lib')
	return bsobj
