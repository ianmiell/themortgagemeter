# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import re
import logging
import string

import main
import mc_util
import mc_db
import mortgagecomparison_utils

institution_code = 'HLFX'
term = str(12 * 25)

def halifax_remortgage_page(static,url,mortgage_type,eligibility,logger):
	bsobj = mortgagecomparison_utils.get_page(static,'static_html/halifax/remortgage-fixed-75ltv.asp',url,logger)
	trs = bsobj.find_all('tr')
	for tr in trs:
		mortgage_details = []
		for d in tr.strings:
			mortgage_details.append(string.strip(d.encode('utf-8')))
		#['\n', 'Term', 'Initial rate', '\xc2\xa0', 'Halifax Homeowner Variable rate thereafter', '\xc2\xa0', 'For the remainder of the term from', '\xc2\xa0', 'The overall cost for comparison is', '\xc2\xa0', 'Product fee', '\xc2\xa0', 'LTV\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0 ', 'Early Repayment Charges until', '\xc2\xa0', 'Loan amount', '\n', 'Extra benefits', '\xc2\xa0', '\n', '\xc2\xa0', '\n']
		#['\n', '2 years', '\n', '4.44%', '\n', 'Currently', ' \xc2\xa03.99%', '\n', '30/11/2014', '\n', '4.3% APR', '\n', '\xc2\xa3995', '\n', '75-80%', '\n', '30/11/2014', '\n', '\xc2\xa30-\xc2\xa31m', '\n', 'Halifax Remortgage Service*', '\n', '\n']
		logger.debug(mortgage_details)
		if len(mortgage_details) > 19 and len(mortgage_details) < 25:
			if mortgage_details[3].find('%') != -1:
				rate_percent = mortgage_details[3][:-1]
				svr_percent = mortgage_details[6].split()[0][:-1].strip('\xc2').strip('\xa0')
				apr_percent = mortgage_details[10].split()[0][:-1]
				booking_fee = mortgage_details[12][2:].replace(',','')
				initial_period = mortgage_details[1]
				# handle special nonsense case
				if re.search(r'years',initial_period) and not re.search(r'[0-9]+ years',initial_period):
					years = initial_period[0]
					initial_period = str(int(years) * 12)
				elif re.search(r'months',initial_period) and not re.search(r'[0-9]+ month',initial_period):
					initial_period = initial_period[0:2]
				else:
					initial_period = str(mortgagecomparison_utils.get_months(initial_period,logger))
				ltv_percent = mortgage_details[14].split('-')[1].strip('%')
				mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
		elif len(mortgage_details) == 25:
			if mortgage_details[3].find('%') != -1:
				rate_percent = mortgage_details[3][:-1]
				svr_percent = mortgage_details[8].split()[0][:-1].strip('\xc2').strip('\xa0')
				apr_percent = mortgage_details[12].split()[0][:-1]
				booking_fee = mortgage_details[14][2:].replace(',','')
				initial_period = mortgage_details[1]
				if re.search(r'years',initial_period) and not re.search(r'[0-9]+ years',initial_period):
					years = initial_period[0]
					initial_period = str(int(years) * 12)
				elif re.search(r'months',initial_period) and not re.search(r'[0-9]+ month',initial_period):
					initial_period = initial_period[0:2]
				else:
					initial_period = str(mortgagecomparison_utils.get_months(initial_period,logger))
				ltv_percent = mortgage_details[16].split('-')[1].strip('%')
				# handle special nonsense case
				mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
		elif len(mortgage_details) > 3:
			logger.debug('Should this be handled?: %s',(mortgage_details))

def halifax_ftb_page(static,url,mortgage_type,eligibility,logger):
	logger = logging.getLogger('retrieve')
	bsobj = mortgagecomparison_utils.get_page(static,'static_html/halifax/fixed.html',url,logger)
	trs = bsobj.find_all('tr')
	for tr in trs:
		mortgage_details = []
		for d in tr.strings:
			mortgage_details.append(string.strip(d.encode('utf-8')))
			if len(mortgage_details) > 19 and len(mortgage_details) < 25:
				if mortgage_details[3].find('%') != -1:
					initial_period = mortgage_details[1]
					if initial_period[0] == 'x':
						# handle special case of "dummy row"
						continue
					rate_percent = mortgage_details[3][:-1]
					svr_percent = mortgage_details[6].split()[0][:-1].strip('\xc2').strip('\xa0')
					apr_percent = mortgage_details[10].split()[0][:-1]
					booking_fee = mortgage_details[12][2:].replace(',','')
					# handle special nonsense case
					if re.search(r'years',initial_period) and not re.search(r'[0-9]+ years',initial_period):
						years = initial_period[0]
						initial_period = str(int(years) * 12)
					elif re.search(r'months',initial_period) and not re.search(r'[0-9]+ month',initial_period):
						initial_period = initial_period[0:2]
					else:
						initial_period = str(mortgagecomparison_utils.get_months(initial_period,logger))
					#print mortgage_details
					if len(mortgage_details[14].split('-')) > 1:
						ltv_percent = str(100 - int(mortgage_details[14].split('-')[0]))
					else:
						ltv_percent = str(100 - int(mortgage_details[14][0:2]))
					mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
	

def halifax_main(static,forcedelete,logger):
	halifax_ftb_page(static,'http://www.halifax.co.uk/mortgages/first-time-buyers/fixed/?tag=But_fix_FTBHP','F','NFTB',logger)
	halifax_remortgage_page(static,'http://www.halifax.co.uk/mortgages/remortgage-fixed-75ltv.asp','F','NRM',logger)
	halifax_remortgage_page(static,'http://www.halifax.co.uk/mortgages/remortgage-fixed-60-75LTV.asp','F','NRM',logger)
	halifax_remortgage_page(static,'http://www.halifax.co.uk/mortgages/remortgage-tracker-75ltv.asp','T','NRM',logger)
	halifax_remortgage_page(static,'http://www.halifax.co.uk/mortgages/remortgage-tracker-60-75LTV.asp','T','NRM',logger)
	halifax_remortgage_page(static,'http://www.halifax.co.uk/mortgages/existing-customers/switch-to-a-new-deal/','F','EED',logger)
	# TODO - BTL
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
