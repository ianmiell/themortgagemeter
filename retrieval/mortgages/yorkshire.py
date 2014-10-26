# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup
import re
import datetime
import pgdb
import logging
import string
import json

import main
import mc_util
import mc_db
import themortgagemeter_utils

institution_code = 'YRKSHR'
term = str(25 * 12)

def process_page(url,logger):
#var mortgages = [
#{
#data: "65543",
#name: "2 year fixed",
#offer: " ",
#customer: "Existing Customer",
#type: "Fixed Rate",
#lowltv: 0,
#highltv: 60,
#initialrate: 2.19,
#until: 2,
#rateafter: 4.95,
#apr: 4.6,
#fee: 499,
#minloan: 1,
#maxloan: 1000000,
#links: "/personal/mortgages/all-our-mortgages/fixed-rate-mortgages/mortgages-fixed-rate-2year-60ltv"},{
#[...]
#data: "655434",
#name: "3 year fixed - Fee Offer ",
#offer: " ",
#customer: "First Time Buyer",
#type: "Fixed Rate",
#lowltv: 90,
#highltv: 95,
#initialrate: 4.99,
#until: 3,
#rateafter: 4.95,
#apr: 5.2,
#fee: 0,
#minloan: 1,
#maxloan: 1000000,
#links: "/personal/mortgages/all-our-mortgages/fixed-rate-mortgages/mortgages-three-year-fixed-rate-95ltv"}
#]

	resp = themortgagemeter_utils.get_page(False,'',url,logger,tostring=True)
	# Tidy up json
	# http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name
	resp = re.sub(r"{\s*'?(\w)", r'{"\1', resp)
	resp = re.sub(r",\s*'?(\w)", r',"\1', resp)
	resp = re.sub(r"(\w)'?\s*:", r'\1":', resp)
	resp = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', resp)
	json_obj = json.loads(resp[16:])
	print json_obj
	#mortgage_list = json_obj['mortgages']
	#if mortgage_list == 'none':
	#	logger.info('URL returned nothing: ' + url)
	#	return
	for mortgage in json_obj:
		customer = mortgage['customer']
		if customer == "Existing Customer":
			eligibilities = ("EMH","EBM","EDE","EED")
		elif customer == "First Time Buyer":
			eligibilities = ("NFTB",)
		elif customer == "New Customer":
			eligibilities = ("NRM","NMH")
		else:
			raise Exception('Unrecognised eligibility: ' + eligibility, eligibility, l)
		mortgage_type = mc_util.get_mortgage_type(mortgage['name'],logger)
		rate_percent = str(mortgage['initialrate'])
		svr_percent = str(mortgage['rateafter'])
		apr_percent = str(mortgage['apr'])
		initial_period = str(int(mortgage['until'] * 12.0))
		booking_fee = str(mortgage['fee'])
		ltv_percent = str(mortgage['highltv'])
		for eligibility in eligibilities:
			print eligibility
			mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,'http://www.nationwide.co.uk',eligibility,logger)

def yorkshire_main(static,forcedelete,logger):
	process_page('http://www.ybonline.co.uk/javascripts/personal-mortgages.js',logger)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
