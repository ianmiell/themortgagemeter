# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup
import re
import datetime
import pgdb
import logging
import string

import main
import mc_util
import mc_db

institution_code = 'ONS'

def get_page():
	logger = logging.getLogger('retrieve')
	req = urllib2.Request('http://www.ons.gov.uk/ons/datasets-and-tables/downloads/csv.csv?dataset=mm23&cdid=CHAW')
	resp = urllib2.urlopen(req)
	print resp
	#bsobj = mc_util.get_page(False,'',url,logger)

def ons_main():
	print 'asd'
	get_page()
