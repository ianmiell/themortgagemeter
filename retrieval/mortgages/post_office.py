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
import mortgagecomparison_utils
import mortgagecomparison_db

#insert into tinstitution (institution_code,institution_type,institution_name) values('PSTFFC','BANK','The Post Office'); 

institution_code = 'PSTFFC'

def get_product_page(static,url,eligibilities):
	logger = logging.getLogger('retrieve')
	bsobj = mortgagecomparison_utils.get_page(static,'static_html/post_office/our-full-range.html',url,logger)
	#print bsobj
	term = str(25 * 12)
	ltv_elems = bsobj.find_all('h2')
	# foreach h2 element, determine the ltv.
	# then get the next element (which is the div, class displaytable). Then, for each tr:
	# td0 = years of fixed or tracker
	# td1 = initial rate
	# td2 = svr
	# td3 = apr
	# td4 = fees
	for ltv_elem in ltv_elems:
		# For post office, first reported % is 100 - LTV
		ltv_elem_str = ltv_elem.string
		if (ltv_elem_str):
			ltv_percent = mortgagecomparison_utils.get_percentage(ltv_elem_str,logger)
			if ltv_percent != '':
				ltv_percent = str(100 - int(ltv_percent))
			else:
				continue
		else:
			continue
		div = ltv_elem.fetchNextSiblings(attrs={'class' : 'displaytable'},limit=1)
		if (div):
			logger.debug('here')
			logger.debug(div)
			trs = div[0].find_all('tr')
			for tr in trs:
				logger.debug(tr)
				# initialise:
				rate_percent = ''
				svr_percent = ''
				apr_percent = ''
				booking_fee = ''
				tds = tr.find_all('td')
				i = 0
				# If there are tds and there are more than 1 of them then we can extract a mortgage...
				logger.debug(tr)
				if tds and len(tds) > 1:
					logger.debug(tds[0].text.encode('utf-8').split('\n'))
					s = tds[0].text.encode('utf-8').split('\n')
					# Sometimes we get empty fields - we remove them here.
					while '' in s:
						s.remove('')
					initial_period = str(mortgagecomparison_utils.get_months(s[i],logger))
					#logger.debug('type_str before split: ' + tds[i].text.encode('utf-8'))
					#logger.debug('tds i: ' + str(i) + ' tds: ' + str(tds))
					#logger.debug('tds i: ' + str(i) + ' tds[i]: ' + str(tds[i].text.encode('utf-8')))
					#logger.debug(re.sub('\xa0','',tds[i].text.encode('utf-8')).split())
					# TODO: generic text cleansing function
					type_str = re.sub('\xa0','',re.sub('\xc2',' ',tds[i].text.encode('utf-8'))).split()[2]
					logger.debug('type_str: ' + type_str)
					if type_str == 'fixed':
						mortgage_type = 'F'
					elif type_str == 'tracker':
						mortgage_type = 'T'
					else:
							mortgagecomparison_utils.record_alert('ERROR: PSTFFC neither fixed nor tracker: ' + type_str,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
					i+=1
					j = 0
					for td in tds[i].text.encode('utf-8').split('\n'):
						t = tds[i].text.encode('utf-8').split('\n')[j]
						rate_percent = mortgagecomparison_utils.get_percentage(t,logger)
						if rate_percent != '':
							break
						j += 1
					while svr_percent == '':
						i+=1
						for t in tds[i].text.encode('utf-8').split('\n'):
							svr_percent = mortgagecomparison_utils.get_percentage(t,logger)
							if svr_percent != '':
								break
					while apr_percent == '':
						i+=1
						for t in tds[i].text.encode('utf-8').split('\n'):
							apr_percent = mortgagecomparison_utils.get_percentage(t,logger)
							if apr_percent != '':
								break
					i+=1
					booking_fee = tds[i].text.strip().encode('utf-8')[2:].replace(',','')
					for eligibility in eligibilities:
						mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
		else:
			pass


def post_office_main(static,forcedelete,logger):
	# full range used to build - no oligibility
	#get_product_page(static,'http://www.postoffice.co.uk/our-full-range')
	get_product_page(static,'http://www.postoffice.co.uk/existing-customers',['EED','EDE','EMH'])
	get_product_page(static,'http://www.postoffice.co.uk/remortgaging',['ERM','NRM','NMH'])
	get_product_page(static,'http://www.postoffice.co.uk/first-time-buyer',['NFTB'])
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
