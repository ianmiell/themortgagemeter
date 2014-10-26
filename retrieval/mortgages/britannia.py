# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import urllib2
import argparse
import re
import datetime
import html5lib
import pgdb
import logging

import main
import mc_util
import mc_db
import themortgagemeter_utils

institution_code = 'BRTN'

# easier to have a global pages_so_far so that the recursion check
# works and stops duplication across multiple calls
pages_so_far = []

def get_product_pages(static,base_url,suffix_url,logger):
	logger.info("In get_product_pages: " + base_url + suffix_url)
	bsobj = themortgagemeter_utils.get_page(static,'NA',base_url + suffix_url,logger)
	pages_so_far.append(suffix_url)
	for anchor in bsobj.find_all('a'):
		href = anchor.get('href')
		if href and re.match('.*/products/.*',href):
			logger.info("HREF:" + href)
			if href in pages_so_far:
				# Already done this page.
				continue
			get_mortgage_page_details(static,base_url,href,logger)

def get_mortgage_page_details(static,base_url,suffix_url,logger):
	bsobj = themortgagemeter_utils.get_page(static,'NA',base_url + suffix_url,logger)
	mtgtables = bsobj.find_all(id='mtgTableData')
	if len(mtgtables) == 0:
		# We're in a product page with potentially further product pages and no mortgage info,
		# so give up and pass back through get_product_pages.
		get_product_pages(static,base_url,suffix_url,logger)
		return
	url = base_url + suffix_url
	# assume default of 25 years
	logger.info("URL:" + url)
	if re.match('.*fixed.*',url):
		mortgage_type = 'F'
	elif re.match('.*offset.*',url):
		mortgage_type = 'O'
	elif re.match('.*tracker.*',url):
		mortgage_type = 'T'
	else:
		# default to variable
		logger.critical("Couldn't identify url: " + url)
		mortgage_type = 'V'
	term = str(25 * 12)
	trs = bsobj.find_all(id='mtgTableData')[0].find_all('tbody')[0].find_all('tr')
	for tr in trs:
		tds = tr.find_all('td')
		logger.info(tds)
		for td in tds:
			# Row 1: tells you type of mortgage and fix period "until dd/mm/year"
			pass
	#mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)

def britannia_main(static,forcedelete,logger):
	base_url = 'http://www.britannia.co.uk/'
	get_product_pages(static,base_url,'_site/channels/mortgage/index.html',logger)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
