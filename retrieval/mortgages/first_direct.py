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

institution_code = 'FRSTDRCT'


def get_product_page(static,url):
	logger = logging.getLogger('retrieve')
	bsobj = themortgagemeter_utils.get_page(static,'static_html/first_direct/mortgage-rates',url,logger)
	print bsobj
	sections = bsobj.find_all(attrs={'class':'section'})
	for section in sections:
		#print section
		#print "============================="
		tbodys = section.find_all("tbody")
		for tbody in tbodys:
			print tbody
			trs = tbody.find_all("tr")
			for tr in trs:
				tds = tr.find_all("td")
				booking_fee_int = 0
				count = 0
				for td in tds:
					# assume default of 25 years
					term = str(25 * 12)
					td_text = td.text.strip().encode('utf-8')
					#print count
					#print td
					if count == 0:
						#initial_period
						initial_period = themortgagemeter_utils.get_months(td_text,logger)
						#mortgage_type F/D/T/O/V
						mortgage_type = mc_util.get_mortgage_type(td_text,logger)
						#eligibility
						print td_text
						pass
					elif count == 1:
						#ltv_percent
						ltv_percent = themortgagemeter_utils.get_percentage(td_text,logger)
					elif count == 2:
						#rate_percent
						rate_percent = themortgagemeter_utils.get_percentage(td_text,logger)
					elif count == 3:
						#svr_percent
						svr_percent = themortgagemeter_utils.get_percentage(td_text,logger)
					elif count == 4:
						#apr_percent
						apr_percent = themortgagemeter_utils.get_percentage(td_text,logger)
					elif count == 5:
						booking_fee_int = booking_fee_int + int(themortgagemeter_utils.get_money(td_text,logger))
					elif count == 6:
						booking_fee_int = booking_fee_int + int(themortgagemeter_utils.get_money(td_text,logger))

					count = count + 1
				booking_fee = str(booking_fee_int)
			mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
#		for anchor in bsobj.find_all('a'):
#			# If the string matches the regexp: '.*product/A[0-9]+.*' then we get that.
#			href = anchor.get('href')
#			if href and re.match('/product/A[0-9]+.*',href):
#				product_url = base_url + href
#				get_mortgage_page_details(static,product_url,tup[1])
#
#def get_mortgage_page_details(static,url,eligibility):
#	logger = logging.getLogger('retrieve')
#	bsobj = themortgagemeter_utils.get_page(static,'static_html/hsbc/product_page.html',url,logger)
#	# assume default of 25 years
#	term = str(25 * 12)
#	#logger.info(bsobj)
#	# rate
#	rate_percent = bsobj.find_all(id='InterestRate',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.string.split('%')[0]
#	# fee(n)
#	booking_fee = bsobj.find_all(id='BookingFee',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.encode('utf_8')[2:].replace(',','')
#	if booking_fee == '':
#		booking_fee = str(0)
#	# LTV
#	ltv_percent = bsobj.find_all(id='maxLTV',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.split('%')[0]
#	# APR for comparison %
#	apr_percent = bsobj.find_all(id='OverallCost',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].strong.string.strip().split()[0]
#	# SVR - To test!
#	svr_percent = bsobj.find_all(id='RevertingVariableRate',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].string.strip().split('%')[0]
#	# Sometimes not displayed, presumably because not applicable so let's assume it's the headline rate.
#	if svr_percent == '-':
#		svr_percent = rate_percent
#	# fixed/tracker/discount/variable
#	desc_lower = bsobj.find_all(attrs={'class' : 'productResults'},limit=1)[0].div.h3.string.lower()
#	if desc_lower.find('fixed') != -1:
#		mortgage_type = 'F'
#	elif desc_lower.find('discount') != -1:
#		mortgage_type = 'D'
#	elif desc_lower.find('tracker') != -1:
#		mortgage_type = 'T'	
#	else:
#		# default to variable
#		mortgage_type = 'V'
#	# fix period (months)
#	for initial_period in (bsobj.find_all(id='RatePeriod',limit=1)[0].find_all(attrs={'class' : 'last'},limit=1)[0].children):
#		if initial_period == 'Term of Loan':
#			initial_period = term
#		else:
#			initial_period = themortgagemeter_utils.get_months(initial_period,logger)
#			break
#	mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)

def first_direct_main(static,forcedelete,logger):
	base_url = 'http://mortgages.firstdirect.com/mortgage-rates'
	get_product_page(static,base_url)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
