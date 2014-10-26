# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import logging
import string
import json

import main
import mc_util
import mc_db
import themortgagemeter_utils

institution_code = 'NTWST'
term = str(12 * 25)

def process_page(static,url,mortgage_type,eligibility):
	logger = logging.getLogger('retrieve')
	resp = themortgagemeter_utils.get_page(static,'static_html/natwest/fix_ftb.html',url,logger,tostring=True)
	json_obj = json.loads(resp)
	if json_obj['Mortgages'] == None:
		logger.info('URL returned nothing: ' + url)
		return
	#themortgagemeter_utils.pretty_print_json(json_obj)
	mortgages = json_obj['Mortgages']['mortgage']
	for mortgage in mortgages:
		rate_percent = mortgage['initialRate']['value']
		svr_percent = mortgage['followOnRate']
		apr_percent = mortgage['overallCostAPR']
		ltv_percent = mortgage['LTV']
		initial_period = str(int(mortgage['initialRate']['duration']) * 12)
		booking_fee = mortgage['arrangementFee']
		mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,url,eligibility,logger)

def natwest_main(static,forcedelete,logger):
	# TODO: Are there more categories to consider? See end
	# TODO: BTL - lots of categories here
	categorytypes = ['Fixed','Variable']
	mortgage_types = ['F','T']
	mortgage_types_tuples = zip(categorytypes,mortgage_types)
	customertypes = ['ftb','remo','pur','ecmh','ecss','fa']
	eligibilities = ['NFTB','NRM','NMH','EMH','EMH','EBM']
	types_tuples = zip(customertypes,eligibilities)
	for mortgage_types_tuple in mortgage_types_tuples:
		categorytype = mortgage_types_tuple[0]
		mortgage_type = mortgage_types_tuple[1]
		for types_tuple in types_tuples:
			customertype = types_tuple[0]
			eligibility = types_tuple[1]
			process_page(static,'http://www.natwest.com/webservices.ashx?service=2&responseformat=json&mortgageterm=25&mortgagetype=' + categorytype + '&customertype=' + customertype,mortgage_type,eligibility)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)

#        "categories": {
#            "category": [
#                {
#                    "id": "ftb",
#                    "label": "First Time Buyer"
#                },
#                {
#                    "id": "btl",
#                    "label": "Buy to Let"
#                },
#                {
#                    "id": "fa",
#                    "label": "Existing Customer (borrowing more)"
#                },
#                {
#                    "id": "remo",
#                    "label": "Remortgage"
#                },
#                {
#                    "id": "pr",
#                    "label": "Private"
#                },
#                {
#                    "id": "bu",
#                    "label": "Business"
#                },
#                {
#                    "id": "ap",
#                    "label": "Select Platinum"
#                },
#                {
#                    "id": "ab",
#                    "label": "Advantage Business"
#                },
#                {
#                    "id": "ag",
#                    "label": "Advantage Gold"
#                },
#                {
#                    "id": "pur",
#                    "label": "House Purchase (New Customer)"
#                },
#                {
#                    "id": "eccd",
#                    "label": "Changing Deal (Existing Customer)"
#                },
#                {
#                    "id": "ecss",
#                    "label": "(Existing Customer) Standard Switcher"
#                },
#                {
#                    "id": "ecmh",
#                    "label": "(Existing Customer) Moving Home"
#                },
#                {
#                    "id": "ecdb",
#                    "label": "(Existing Customer) In Deal Breaker"
#                },
#                {
#                    "id": "svr",
#                    "label": "SVR (for calculator)"
#                },
#                {
#                    "id": "ca",
#                    "label": "NatWest Current Account"
#                },
#                {
#                    "id": "rcdt",
#                    "label": "Remove changing deal text"
#                },
#                {
#                    "id": "blck",
#                    "label": "Black Account"
#                },
#                {
#                    "id": "sltsilver",
#                    "label": "Select Silver"
#                },
#                {
#                    "id": "resapply",
#                    "label": "Restrictions apply"
#                },
#                {
#                    "id": "cashinc",
#                    "label": "Cashback included"
#                },
#                {
#                    "id": "mnbnk",
#                    "label": "Customers who use us as their main bank - terms apply."
#                },
#                {
#                    "id": "btlletout",
#                    "label": "Buy to let: I am buying a property to let out"
#                },
#                {
#                    "id": "btlremo",
#                    "label": "Buy to let: Remortgage to NatWest"
#                },
#                {
#                    "id": "btlcd",
#                    "label": "Buy to let: changing deal"
#                },
#                {
#                    "id": "btled",
#                    "label": "Buy to let: ending deal early"
#                },
#                {
#                    "id": "btlbm",
#                    "label": "Buy to let: borrowing more on existing property"
#                },
#                {
#                    "id": "fix",
#                    "label": "Fixed"
#                },
#                {
#                    "id": "var",
#                    "label": "Variable"
#                },
#                {
#                    "id": "lt",
#                    "label": "Lifetime"
#                },
#                {
#                    "id": "off",
#                    "label": "Offset"
#                }
#
