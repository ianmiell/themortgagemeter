# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import logging
import string

import main
import mc_util
import mc_db
import themortgagemeter_utils

institution_code = 'NRTHNR'
term = str(12 * 25)

def process_page(static,base_url,url_suffix,eligibility):
	logger = logging.getLogger('retrieve')
	bsobj = themortgagemeter_utils.get_page(static,'static_html/northernrock/First-Time-Buyer',base_url + url_suffix,logger)
	anchors = bsobj.find_all(attrs={'class' : 'continue moreinfo'})
	for anchor in anchors:
		url = base_url + anchor['href']
		logger.info(url)
		anchor_bsobj = themortgagemeter_utils.get_page(static,'static_html/northernrock/5yr_everyday_fixed_5ct5',url,logger)
		title = anchor_bsobj.find_all('h1')[0].string
		for class_str in ('fixedpanel','trackerpanel'):
			trs = anchor_bsobj.find_all('tr','list ' + class_str)
			if trs:
				(initial_period,mortgage_type) = process_title(title,logger)
				#print title
				#print initial_period
				#print mortgage_type
				# TODO get time period and type from title
				# TODO: I think this is wrong! fixedpanel is different from trackerpanel!
				#print trs
				for tr in trs:
					spans = tr.find_all('span')
					count = 0
					for span in spans:
						# Skip the first one.
						#print span
						#print count
						count += 1
						if count > 5:
							continue
						else:
							s = span.string
						if count == 1:
							if s == None:
								s = span.em.string
							rate_percent = s.split('%')[0]
						elif count == 2:
							svr_percent = s.split('%')[0]
						elif count == 3:
							apr_percent = s.split('%')[0]
						elif count == 4:
							booking_fee = s[1:].replace(',','')
						elif count == 5:
							ltv_percent = s.split('%')[0].replace(',','')
					#print spans
					if spans:
						mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
						#print 'rate_percent:' + rate_percent + ' apr_percent:' + apr_percent + ' booking_fee:' + booking_fee + ' ltv_percent:' + ltv_percent + ' mortgage_type:' + mortgage_type + ' initial_period:' + initial_period + ' svr_percent:' + svr_percent
					else:
						logger.critical('No data from url: ' + url)

def process_title(title,logger):
	# Take the title, and break down into initial_period and mortgage type
	# mortgage_type:
	# If it contains Fixed = F, Tracker = T, "Freedom to Fix"?, "Fixed Cashback"?, "Flexi Tracker"?
	initial_period = str(themortgagemeter_utils.get_months(title,logger))
	mortgage_type = mc_util.get_mortgage_type(title,logger)
	return (initial_period,mortgage_type)

def northernrock_main(static,forcedelete,logger):
	# From: http://www.northernrock.co.uk/mortgages/
	# Assumed these are new customers, since there's an extra section on "existing customers"
	# http://www.northernrock.co.uk/Mortgages/Find/Find-A-Mortgage/First-Time-Buyer
	process_page(static,'http://www.northernrock.co.uk','/Mortgages/Find/Find-A-Mortgage/First-Time-Buyer','NFTB')
	# http://www.northernrock.co.uk/Mortgages/Find/Find-A-Mortgage/Moving-Home
	process_page(static,'http://www.northernrock.co.uk/','Mortgages/Find/Find-A-Mortgage/Moving-Home','NMH')
	# http://www.northernrock.co.uk/Mortgages/Find/Find-A-Mortgage/Remortgage
	process_page(static,'http://www.northernrock.co.uk/','Mortgages/Find/Find-A-Mortgage/Remortgage','NRM')
	# TODO - BTL
	# http://www.northernrock.co.uk/Mortgages/Find/Find-A-Mortgage/Buy-To-Let
	mc_db.update_current(institution_code,main.today,forcedelete,logger)

