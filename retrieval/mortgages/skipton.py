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
import themortgagemeter_utils
import themortgagemeter_db

institution_code = 'SKPTN'
# global regexps
fr_re = re.compile(r'/mortgages/fixed_rate_mortgages/([0-9]+)yr_([0-9]+)ltv.aspx')
tracker_re = re.compile(r'/mortgages/tracker_mortgages/([0-9]+)yr_([0-9]+)ltv.aspx')
discount_re = re.compile(r'mortgages/Discount_mortgages/([0-9]+)yr_([0-9]+)ltv.aspx')
ftb_re = re.compile(r'/mortgages/first-time-buyer/([0-9]+)yr_([0-9]+)ltv.aspx')

def get_product_pages(static,base_url,suffix,mortgage_type,href_re):
	logger = logging.getLogger('retrieve')
	bsobj = themortgagemeter_utils.get_page(static,'static_html/skipton/fixed_rate_mortgages.html',base_url + suffix,logger)
	term = str(25 * 12)
	#print bsobj
	anchors = bsobj.find_all(href=href_re)
	for anchor in anchors:
		#print anchor
		# Get from the anchor the ltv and the term
		link = anchor.get('href')
		url = base_url + link
		# Still to get:
		rate_percent    = 0
		svr_percent     = 0
		apr_percent     = 0
		booking_fee     = 0
		application_fee = 0
		# eligibilities - first time buyers have own page, so all others?
		eligibilities   = ['NMH','NRM','ERM','EMH','EBM','EED']
		#print link
		if re.search(fr_re,link):
			initial_period = str(int(re.search(fr_re,link).group(1)) * 12)
			ltv_percent = str(int(re.search(fr_re,link).group(2)))
			# Now go to link
			subpage_bsobj = themortgagemeter_utils.get_page(static,'N/A',url,logger)
			table = subpage_bsobj.find_all(attrs={'id' : 'centralContent'},limit=1)[0].find_all('table',limit=1)[0]
			#print '==================================================='
			#print table
			tr_count = 0
			for tr in table.find_all('tr'):
				tr_count += 1
				if tr_count == 3:
					rate_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[1].string,logger)
				elif tr_count == 4:
					svr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[1].string,logger)
				elif tr_count == 5:
					apr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[0].string,logger)
				elif tr_count == 7:
					application_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
				elif tr_count == 8:
					booking_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
		elif re.search(tracker_re,link):
			initial_period = str(int(re.search(tracker_re,link).group(1)) * 10)
			ltv_percent = str(int(re.search(tracker_re,link).group(2)))
			# Now go to link
			subpage_bsobj = themortgagemeter_utils.get_page(static,'N/A',url,logger)
			#print subpage_bsobj
			table = subpage_bsobj.find_all(attrs={'id' : 'centralContent'},limit=1)[0].find_all('table',limit=1)[0]
			#print '==================================================='
			#print table
			tr_count = 0
			for tr in table.find_all('tr'):
				tr_count += 1
				if tr_count == 3:
					rate_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[0].string,logger)
				elif tr_count == 4:
					svr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[1].string,logger)
				elif tr_count == 5:
					apr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[0].string,logger)
				elif tr_count == 7:
					application_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
				elif tr_count == 8:
					booking_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
		elif re.search(discount_re,link):
			initial_period = str(int(re.search(discount_re,link).group(1)) * 10)
			ltv_percent = str(int(re.search(discount_re,link).group(2)))
			# Now go to link
			subpage_bsobj = themortgagemeter_utils.get_page(static,'N/A',url,logger)
			#print subpage_bsobj
			table = subpage_bsobj.find_all(attrs={'id' : 'centralContent'},limit=1)[0].find_all('table',limit=1)[0]
			#print '==================================================='
			#print table
			tr_count = 0
			for tr in table.find_all('tr'):
				tr_count += 1
				if tr_count == 3:
					rate_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[1].string,logger)
				elif tr_count == 4:
					svr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[1].string,logger)
				elif tr_count == 5:
					apr_percent = themortgagemeter_utils.get_percentage(tr.find_all('td')[0].string,logger)
				elif tr_count == 7:
					application_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
				elif tr_count == 8:
					booking_fee = tr.find_all('td')[0].string.encode('utf_8')[2:].replace(',','')
		elif re.search(ftb_re,link):
			themortgagemeter_utils.record_alert('ERROR: SKIPTON first time buyer seen for the first time',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
			continue
		else:
			raise Exception("Unhandled link " + url,'')
		# set up the booking fee
		# Sometimes it's "No Fee" on the page
		if booking_fee.strip() == "Fee":
			booking_fee = "0"
		if application_fee.strip() == "Fee":
			application_fee = "0"
		booking_fee = str(int(booking_fee) + int(application_fee))
		for eligibility in eligibilities:
			mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)


def skipton_main(static,forcedelete,logger):
	# BUY TO LET - TODO
	#http://www.skipton.co.uk/mortgages/buy-to-let_mortgages/
	#http://www.skipton.co.uk/mortgages/first-time-buyer - none yet seen assuming tracker - to do!
	#href_re = re.compile(r'.*/mortgages/first-time-buyer.*aspx')
	href_re = ftb_re
	get_product_pages(static,'http://www.skipton.co.uk','/mortgages/first-time-buyer','T',href_re)
	#href_re = re.compile(r'.*/mortgages/Discount_mortgages.*aspx')
	href_re = discount_re
	get_product_pages(static,'http://www.skipton.co.uk','/mortgages/discount_mortgages','D',href_re)
	#href_re = re.compile(r'.*/mortgages/tracker_mortgages.*aspx')
	href_re = tracker_re
	get_product_pages(static,'http://www.skipton.co.uk','/mortgages/tracker_mortgages','T',href_re)
	#href_re = re.compile(r'.*/mortgages/fixed_rate_mortgages.*aspx')
	href_re = fr_re
	get_product_pages(static,'http://www.skipton.co.uk','/mortgages/fixed_rate_mortgages','F',href_re)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
