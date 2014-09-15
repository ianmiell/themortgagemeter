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

institution_code = 'SNTNDR'
# Sometimes svr is N/A - this makes no sense, so use the last-seen svr
# if available as a workaround. Defaults to 0.0.
global_svr = "0.0"

def get_product_pages(static,url):
	logger = logging.getLogger('retrieve')
	logger.debug('In get_product pages, base_url: %s',(url))
	# URL
	if static:
		f = open('static_html/santander/productInfo.js')
		the_page = f.read()
		f.close()
	else:
		req = urllib2.Request(url)
		# Make request.
		response = urllib2.urlopen(req)
		# Get 'page' content.
		the_page = response.read()
	logger.debug('In get_product pages, response: \n%s',(the_page))
	r = re.compile('\[.*')
	for l in the_page.split('\n'):
		#print l
		if re.match(r,l):
			# FORMAT OF ARRAY
			# // array format ["OUR INPUT","Product","Maximum loan size formatted","Rate Type","Product Type","Eligibility","Customer Type","Benefit solution","Maximum LTV","Initial rate","Differential to BBR","Standard Variable Rate","APR","Maximum loan size","Booking fee","Charge end date"]]
			# ["N907H","DIRECT 2 yr Fixed Homebuyer","&pound;1m","Fixed","2 year Fixed rate","All","Mover|FTB","Free valuation  and &pound;250 cashback","0.60","0.0239","n/a","0.0474","0.0460","1000000","1995","03/12/2014","6000"]
			def strip_quotes(x): return x.strip('"')
			if len(map(strip_quotes,l.strip('[],').split(','))) == 17:
				(ref,product,max_loan_size,rate_type,product_type,eligibility,customer_type,benefit_solution,ltv,initial_rate,differential_to_bbr,svr,apr,max_loan_size,booking_fee,end_date,mystery_num) = map(strip_quotes,l.strip('[],').split(','))
			else:
				logger.critical("Len of array wrong! Continuing. If there are too many of these, fix the bug")
				logger.critical(l)
				continue
			logger.info('ref: ' + ref + ' product: ' + product + ' max_loan_size: ' + max_loan_size + ' rate_type: ' + rate_type+ ' product_type: ' + product_type+ ' eligibility: ' + eligibility+ ' customer_type: ' + customer_type + ' benefit_solution: ' + benefit_solution+ ' ltv: ' + ltv+ ' initial_rate: ' + initial_rate+ ' differential_to_bbr: ' + differential_to_bbr+ ' svr: ' + svr + ' apr: ' + apr+ ' max_loan_size: ' + max_loan_size+ ' booking_fee: ' + booking_fee+ ' end_date: ' + end_date)
			#- rate (%)
			#- fixed/tracker/discount (fixed/tracker/discount)
			#- fix period (n months)
			#- fee (n)
			#- LTV (%)
			#- APR for comparison (%)
			#- term (eg 25 years) (n months)
			# term (months)
			# assume default of 25 years
			mortgage_eligibility_dict = mc_util.get_mortgage_eligibility_dict()
			eligibilities=[]
			if eligibility == 'Loyalty':
				mortgage_eligibility_dict['existing_customer'] = 'T'
			elif eligibility== 'All':
				mortgage_eligibility_dict['existing_customer'] = 'B'
			elif eligibility== 'Non-loyalty':
				mortgage_eligibility_dict['existing_customer'] = 'F'
			elif eligibility== 'Current Account Exclusive':
				# Count this as "existing customer"
				mortgage_eligibility_dict['existing_customer'] = 'T'
			elif eligibility== 'Existing Mover Exclusive':
				# Count this as "existing customer"
				mortgage_eligibility_dict['existing_customer'] = 'T'
			else:
				raise Exception('Unrecognised eligibility: ' + eligibility, eligibility, l)
			for ct in customer_type.split('|'):
				c = mortgage_eligibility_dict.copy()
				if ct == 'Mover':
					c['moving_home'] = 'T'
					eligibilities += mc_util.validate_eligibility_dict(c,[])
				elif ct.split()[0].strip() == 'FTB':
					c['ftb'] = 'T'
					c['existing_customer'] = 'F'
					eligibilities += mc_util.validate_eligibility_dict(c,[])
				elif ct == 'Remortgage':
					c['remortgage'] = 'T'
					eligibilities += mc_util.validate_eligibility_dict(c,[])
				elif ct == 'FTBRemortgage':
					c['remortgage'] = 'T'
					c['ftb'] = 'T'
					eligibilities += mc_util.validate_eligibility_dict(c,[])
				else:
					raise Exception('Unrecognised customer type: ', ct, l)
			term = str(25 * 12)
			rate_percent = str(float(initial_rate) * 100)
			if product_type.find('Fixed') != -1:
				mortgage_type = 'F'
			elif product_type.find('Offset') != -1:
				mortgage_type = 'O'
			elif product_type.find('Tracker') != -1:
				mortgage_type = 'T'
			else:
				raise Exception('Product type not recognised: ', product_type, l)
			if end_date == 'Lifetime Tracker':
				initial_period = term
			elif product_type.find('year') != -1:
				years = re.match(r'^([0-9]+).*$',product_type).group(1)
				initial_period = str(int(years) * 12)
			elif end_date.find('anniversary') != -1:
				years = re.match(r'^([0-9]+).*$',end_date).group(1)
				initial_period = str(int(years) * 12)
			elif end_date.find('N/A') != -1 or end_date == 'd-M':
				initial_period = term
			else:
				raise Exception('Unrecognised fix period: ', end_date, l)
			ltv_percent = str(float(ltv) * 100)
			apr_percent = str(float(apr) * 100)
			if svr == "n/a" or svr == "N/A":
				svr_percent = global_svr
			else:
				svr_percent = str(float(svr) * 100)
				global_svr = svr_percent
			for eligibility in eligibilities:
				mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)

def santander_main(static,forcedelete,logger):
	#get_product_pages(static,'http://www.santander-products.co.uk/mortgages/mortgage-calculator/js/productInfo.js')
	get_product_pages(static,'http://www.santander-products.co.uk/mortgages/mortgage-calculator/productInfo.php')
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
