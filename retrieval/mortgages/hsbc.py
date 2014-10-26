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

institution_code = 'HSBC'

def get_product_pages(static,base_url):
	logger = logging.getLogger('retrieve')
	data = [('/mortgage-rates','NRM'),('/mortgages/mortgage-rates/first-time-buyers','NFTB'),('/mortgages//mortgage-rates/moving-home','NMH'),('/mortgages/mortgage-rates/existing-customer-switching','EED'),('/mortgages/mortgage-rates/existing-customer-borrowing-more','EBM')]
	for tup in data:
		url = base_url + tup[0]
		bsobj = themortgagemeter_utils.get_page_headless(url,logger)
		print 'BSOBJ'
		print bsobj
		for anchor in bsobj.find_all('a'):
			# If the string matches the regexp: '.*product/A[0-9]+.*' then we get that.
			print anchor
			href = anchor.get('href')
			if href and re.match('/products?pcode=A[0-9]+.*',href):
				product_url = base_url + href
				get_mortgage_page_details(static,product_url,tup[1])

def get_mortgage_page_details(static,url,eligibility):
	logger = logging.getLogger('retrieve')
	bsobj = themortgagemeter_utils.get_page_headless(url,logger)
	# assume default of 25 years
	term = str(25 * 12)
	#logger.info(bsobj)
	# rate
	rate_percent = bsobj.find_all(id='InterestRate',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.string.split('%')[0]
	# fee(n)
	booking_fee = bsobj.find_all(id='BookingFee',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.encode('utf_8')[2:].replace(',','')
	if booking_fee == '':
		booking_fee = str(0)
	# LTV
	ltv_percent = bsobj.find_all(id='maxLTV',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.split('%')[0]
	# APR for comparison %
	apr_percent = bsobj.find_all(id='OverallCost',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].strong.string.strip().split()[0]
	# SVR - To test!
	svr_percent = bsobj.find_all(id='RevertingVariableRate',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.strip().split('%')[0]
	# Sometimes not displayed, presumably because not applicable so let's assume it's the headline rate.
	if svr_percent == '-':
		svr_percent = rate_percent
	# fixed/tracker/discount/variable
	desc_lower = bsobj.find_all(attrs={'class' : 'productResults'},limit=1)[0].div.h3.string.lower()
	if desc_lower.find('fixed') != -1:
		mortgage_type = 'F'
	elif desc_lower.find('discount') != -1:
		mortgage_type = 'D'
	elif desc_lower.find('tracker') != -1:
		mortgage_type = 'T'	
	else:
		# default to variable
		mortgage_type = 'V'
	# fix period (months)
	for initial_period in (bsobj.find_all(id='RatePeriod',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].children):
		if initial_period == 'Term of Loan':
			initial_period = term
		else:
			initial_period = themortgagemeter_utils.get_months(initial_period,logger)
			break
	mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)

def hsbc_main(static,forcedelete,logger):
	base_url = 'https://www.hsbc.co.uk/1/2'
	get_product_pages(static,base_url)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
