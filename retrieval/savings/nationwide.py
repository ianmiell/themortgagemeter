# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import urllib
import urllib2
import argparse
import re
import html5lib
import datetime
import pgdb
import logging

import main
import mc_util
import mc_db

institution_code = 'NTNWD'

#def get_product_pages(static,url,ltv_percent,eligibility):
#	logger = logging.getLogger('retrieve')
#	bsobj = mc_util.get_page(static,'static_html/nationwide/nationwide.html',url,logger)
#	#print url

def nationwide_main(static,forcedelete,logger):
	# http://www.nationwide.co.uk/savings/default.htm
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
