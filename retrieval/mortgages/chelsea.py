# vim: set fileencoding=utf-8
import xml.etree.ElementTree as ET

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

institution_code = 'CHLS'


def get_product_pages(static,url,logger):
	logger.debug("In get_product_pages: " + url)
	# Get the svr first (it's global)
	lines = themortgagemeter_utils.get_page(False,'','http://www.thechelsea.co.uk/js/mortgage-finder.js',logger,True).split('\n')
	for line in lines:
		if re.match(r'^var chelseaSVR = "[^%]*%".*',line) != None:
			svr_percent = re.match(r'^var chelseaSVR = "([^%]*)%".*$',line).group(1)
			break
	# Now get the mortgage data
	if static:
		tree = ET.parse('static_html/chelsea/mortage-product-data-0031.xml')
		root = tree.getroot()
	else:
		root = ET.fromstring(themortgagemeter_utils.get_page(False,'',url,logger,True))
	term = str(25 * 12)
	for product in root.findall('product'):
		apr_percent = product.get('apr').split('%')[0]
		rate_percent = product.get('interestRate').split('%')[0]
		# No svr supplied, take apr
		ltv_percent = product.get('maxLTV').split('%')[0]
		mortgage_type_raw = product.get('mortgageType')
		name = product.get('name')
		booking_fee = product.get('completionFee')
		if booking_fee == '':
			booking_fee = '0'
		existing_borrower = product.get('existingBorrower')
		new_borrower = product.get('newBorrower')
		first_time_buyer = product.get('firstTimeBuyer')
		moving_home = product.get('movingHome')
		remortgaging = product.get('remortgaging')
		# Gathered data, now let's marshall before submitting.
		if mortgage_type_raw == 'fixed':
			mortgage_type = 'F'
		elif mortgage_type_raw == 'fixedoffset':
			mortgage_type = 'F'
		elif mortgage_type_raw == 'ftbfixed':
			mortgage_type = 'F'
		elif mortgage_type_raw == 'ftbfixedoffset':
			mortgage_type = 'F'
		elif mortgage_type_raw == 'fixedtracker':
			# Presumably fixed, then a tracker??
			mortgage_type = 'F'
		elif mortgage_type_raw == 'tracker':
			mortgage_type = 'T'
		elif mortgage_type_raw == 'trackeroffset':
			mortgage_type = 'T'
		elif mortgage_type_raw == 'offset':
			mortgage_type = 'T'
		elif mortgage_type_raw == 'mixedoffset':
			mortgage_type = 'T'
		elif mortgage_type_raw == 'rollover':
			# rollover? no example, but exists in the docs
			#print 'rollover'
			#ET.dump(product)
			mortgage_type = 'T'
		elif mortgage_type_raw == 'mixed':
			# WTF is mixed?
			mortgage_type = 'T'
		else:
			# default to variable
			#print mortgage_type_raw
			mortgage_type = 'V'

		# Get a mortgage eligibility dictionary to submit.
		mortgage_eligibility_dict = mc_util.get_mortgage_eligibility_dict()
		if existing_borrower == 'Y':
			mortgage_eligibility_dict['existing_customer'] = 'B'
		if new_borrower == 'Y':
			mortgage_eligibility_dict['moving_home'] = 'B'
		if first_time_buyer == 'Y':
			mortgage_eligibility_dict['ftb'] = 'B'
		if moving_home == 'Y':
			mortgage_eligibility_dict['moving_home'] = 'B'
		if remortgaging == 'Y':
			mortgage_eligibility_dict['remortgage']= 'B'
		eligibilities = mc_util.validate_eligibility_dict(mortgage_eligibility_dict,[])

		# use get_months to determine period
		initial_period = themortgagemeter_utils.get_months(name,logger)

		#ET.dump(product)
		#print eligibilities
		#print initial_period
		#print mortgage_eligibility_dict
		for eligibility in eligibilities:
			mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)
		#print '---------------'

def chelsea_main(static,forcedelete,logger):
	# http://www.thechelsea.co.uk/js/mortgage-data-ref.js 
	# get the xml file from there, then parse it, eg
	# http://www.thechelsea.co.uk/mortgages/mortage-product-data-0031.xml
	url = themortgagemeter_utils.get_page(False,'','http://www.thechelsea.co.uk/js/mortgage-data-ref.js',logger,True).split('"')[1]
	xml_url = url
	get_product_pages(static,'http://www.thechelsea.co.uk/' + xml_url,logger)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
