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
import mortgagecomparison_utils

institution_code = 'TSC'


def get_product_pages(static,url,logger):
	logger.debug("In get_product_pages: " + url)
	# Get the svr first (it's global)
	lines = mortgagecomparison_utils.get_page(False,'',url,logger,True).split('\n')
	# Now get the mortgage data
	if static:
		tree = ET.parse('static_html/tesco/Products.xml')
		root = tree.getroot()
	else:
		root = ET.fromstring(mortgagecomparison_utils.get_page(False,'',url,logger,True))
	term = str(25 * 12)
	for purchase in ('HousePurchase','Remortgage'):
		if purchase == 'HousePurchase':
			eligibilities = ['NFTB','NMH']
		elif purchase == 'Remortgage':
			eligibilities = ['NRM']
		for rate_type in ('FixedRate','TrackerRate'):
			if rate_type == 'FixedRate':
				mortgage_type = 'F'
			elif rate_type == 'TrackerRate':
				mortgage_type = 'T'
			rate_set = root.find(purchase).find(rate_type)
			for rate in rate_set.findall('LTV'):
				ltv_percent = rate.get('max')
				for mortgage in rate.findall('Mortgage'):
					#ET.dump(mortgage)
					#print "--------------------"
					rate_percent = mortgage.find('initialRate').text
					apr_percent = mortgage.find('APR').text
					svr_percent = mortgage.find('variableRate').text
					name = mortgage.find('name').text.split('\n')[0]
					initial_period = mortgagecomparison_utils.get_months(name,logger)
					booking_fee = str(int(mortgage.find('bookingFee').text) + int(mortgage.find('productFee').text))
					for eligibility in eligibilities:
						mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,'http://www.tescobank.com/personal/finance/mortgages',eligibility,logger)

def tesco_main(static,forcedelete,logger):
	get_product_pages(static,'http://www.tescobank.com/assets/sections/mortgages/selector/xml/Products.xml',logger)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
