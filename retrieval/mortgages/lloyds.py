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
import mortgagecomparison_utils

institution_code = 'LLOYDS'
r = re.compile(r'([0-9]+)%[\s]+of.*$')
term = str(12 * 25)

def get_product_pages(url,mortgage_type,ltv_percent,eligibilities,logger):
	resp = mortgagecomparison_utils.get_page(False,'',url,logger,tostring=True)
	json_obj = json.loads(resp)
	#print json_obj
	mortgage_list = json_obj['mortgageList']
	if mortgage_list == 'none':
		logger.info('URL returned nothing: ' + url)
		return
	for item in mortgage_list:
		#print item['mortgages']
		#mortgage_type #product_fee #ltv #offer #initial_rate #homeowner_variable_rate #repayment #erc #buyer_type #loan_size #overall_cost_for_comparison #payment #initial_term
		mortgage = item['mortgages']
		#print mortgage
		if mortgage['initial_term'] == None:
			#print "continuing"
			continue
		rate_percent = mortgage['initial_rate']['rate']
		svr_percent = mortgage['homeowner_variable_rate']['rate']
		apr_percent = mortgage['overall_cost_for_comparison']['rate']
		initial_period = str(int(float(mortgage['initial_term']) * 12))
		booking_fee = mortgage['product_fee']['rate']
		buyer_types = mortgage['buyer_type']
		for eligibility in eligibilities:
			mc_util.handle_mortgage_insert(institution_code,mortgage_type,rate_percent,svr_percent,apr_percent,ltv_percent,initial_period,booking_fee,term,'http://www.lloydsbank.com',eligibility,logger)

	

def lloyds_main(static,forcedelete,logger):
	property_value = "300000"
	for buyer_type in ('first_time_buyer','remortgaging','switching_deals'):
		for mortgage_type_name in ('fixed','variable'):
			if mortgage_type_name == 'fixed':
				mortgage_type = 'F'
			elif mortgage_type_name == 'variable':
				mortgage_type = 'V'
			for ltv in ('60','70','75','80','90','95','100'):
				deposit_amount = str(((100 - int(ltv)) * int(property_value)) / 100)
				url = "http://www.lloydsbank.com/tools/paymentsCalculator.asp?buyerType=first_time_buyer&mortgageType=" + mortgage_type_name + "&repaymentType=Repayment+Only&initialTerm=all&propertyValue=" + property_value  + "&depositAmount=" + deposit_amount + "&mortgageTerm=25&ltv=" + ltv + "&btnId=Find+Mortgages"
				if buyer_type == 'first_time_buyer':
					eligibilities = ['NFTB']
				elif buyer_type == 'remortgaging':
					eligibilities = ['ERM','NRM','EMH']
				elif buyer_type == 'switching_deals':
					eligibilities = ['EED']
				get_product_pages(url,mortgage_type,ltv,eligibilities,logger)
	mc_db.update_current(institution_code,main.today,forcedelete,logger)
# http://www.lloydsbank.com/tools/paymentsCalculator.asp?buyerType=first_time_buyer&mortgageType=fixed&repaymentType=Repayment+Only&initialTerm=all&propertyValue=300000&depositAmount=90000&mortgageTerm=25&ltv=70.00&btnId=Find+Mortgages
#buyerType: first_time_buyer = FTB
#           remortgaging
#           additional_borrowing
#           switching_deals
#           btl_property_purchase
#           btl_remortgaging
#           btl_borrowing_more
#           btl_switching_deals
#mortgageType: fixed, variable
#initialTerm: all
#propertyValue: 300000
#depositAmount: 
#mortgageTerm: 25
# result is json:


#mortgageList.product
#
#			{"mortgageList" : [
#
#{
#  "product": {
#    "footer": [],
#    "title": "5 Year Fixed Rate 75%",
#    "ID": "LM1121803523",
#    "product_detail": {
#      "title": "Find out more",
#      "extended_desc": [],
#      "link": "/mortgages/mortgage-products/M000108.asp",
#      "target": []
#    },
#    "apply_now": {
#      "title": "Start now",
#      "extended_desc": [],
#      "link": "/mortgages.asp#tab-row-6",
#      "target": []
#    }
#  },
#  "mortgages": {
#    "buyer_type": "first_time_buyer",
#    "payment": "1,107.30",
#    "loan_size": {
#      "content": "<p>Borrowing between £5,000 and £1,000,000</p>",
#      "summary": "This is our loan size table.",
#      "title": "Loan size",
#      "minimum": "5000",
#      "maximum": "1000000",
#      "compare": "true",
#      "tableClass": "loan_size",
#      "caption": "This is our loan size table."
#    },
#    "repayment": "repayment, interest_only",
#    "erc": {
#      "content": "5% until 31/08/2014, then 4% until 31/08/2015, then 3% until 31/08/2017, then 2% until 31/08/2018",
#      "summary": "This is our erc table.",
#      "title": "Early repayment charge",
#      "compare": "true",
#      "tableClass": "erc",
#      "caption": "This is our erc table."
#    },
#    "initial_rate": {
#      "content": "<span class=\"repAprLarge\">3.99%</span> fixed until 31/08/2018",
#      "summary": "This is our initial rate table.",
#      "title": "Initial rate",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "initial_rate",
#      "caption": "This is our initial rate table."
#    },
#    "overall_cost_for_comparison": {
#      "content": "<span class=\"repAprLarge\">4.1% APR</span>",
#      "summary": "This is our occ table.",
#      "title": "The overall cost for comparison is",
#      "rate": "4.1",
#      "compare": "true",
#      "tableClass": "occ",
#      "caption": "This is our occ table."
#    },
#    "offer": [],
#    "mortgage_type": "fixed",
#    "ltv": {
#      "content": "<p><span class=\"repAprLarge\">75%</span> max,   60% min</p>",
#      "summary": "This is our loan to value table.",
#      "title": "Loan to value",
#      "minimum": "60",
#      "maximum": "75",
#      "compare": "true",
#      "tableClass": "ltv",
#      "caption": "This is our loan to value table."
#    },
#    "initial_term": "5",
#    "homeowner_variable_rate": {
#      "content": "Homeowner Variable Rate currently <span class=\"repAprLarge\">3.99%</span> for the remainder of the term",
#      "summary": "This is our hvr table.",
#      "title": "Followed by",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "hvr",
#      "caption": "This is our hvr table."
#    },
#    "product_fee": {
#      "content": "<span class=\"repAprLarge\">None</span>",
#      "summary": "This is our fee table.",
#      "title": "Product fee",
#      "rate": "0",
#      "compare": "true",
#      "tableClass": "product_fee",
#      "caption": "This is our fee table."
#    }
#  }
#},{
#  "product": {
#    "footer": [],
#    "title": "2 Year Fixed Rate 75%",
#    "ID": "LM6207776333",
#    "product_detail": {
#      "title": "Find out more",
#      "extended_desc": [],
#      "link": "/mortgages/mortgage-products/M000334.asp",
#      "target": []
#    },
#    "apply_now": {
#      "title": "Start now",
#      "extended_desc": [],
#      "link": "/mortgages.asp#tab-row-6",
#      "target": []
#    }
#  },
#  "mortgages": {
#    "buyer_type": "first_time_buyer",
#    "payment": "962.32",
#    "loan_size": {
#      "content": "<p>Borrowing between £150,000 and £1,000,000</p>",
#      "summary": "This is our loan size table.",
#      "title": "Loan size",
#      "minimum": "150000",
#      "maximum": "1000000",
#      "compare": "true",
#      "tableClass": "loan_size",
#      "caption": "This is our loan size table."
#    },
#    "repayment": "repayment, interest_only",
#    "erc": {
#      "content": "3% until 31/08/2014, then 2% until 31/08/2015",
#      "summary": "This is our erc table.",
#      "title": "Early repayment charge",
#      "compare": "true",
#      "tableClass": "erc",
#      "caption": "This is our erc table."
#    },
#    "initial_rate": {
#      "content": "<span class=\"repAprLarge\">2.69%</span> fixed until 31/08/2015",
#      "summary": "This is our initial rate table.",
#      "title": "Initial rate",
#      "rate": "2.69",
#      "compare": "true",
#      "tableClass": "initial_rate",
#      "caption": "This is our initial rate table."
#    },
#    "overall_cost_for_comparison": {
#      "content": "<span class=\"repAprLarge\">4.0% APR</span>",
#      "summary": "This is our occ table.",
#      "title": "The overall cost for comparison is",
#      "rate": "4",
#      "compare": "true",
#      "tableClass": "occ",
#      "caption": "This is our occ table."
#    },
#    "offer": [],
#    "mortgage_type": "fixed",
#    "ltv": {
#      "content": "<p><span class=\"repAprLarge\">75%</span> max,   60% min</p>",
#      "summary": "This is our loan to value table.",
#      "title": "Loan to value",
#      "minimum": "60",
#      "maximum": "75",
#      "compare": "true",
#      "tableClass": "ltv",
#      "caption": "This is our loan to value table."
#    },
#    "initial_term": "2",
#    "homeowner_variable_rate": {
#      "content": "Homeowner Variable Rate currently <span class=\"repAprLarge\">3.99%</span> for the remainder of the term",
#      "summary": "This is our hvr table.",
#      "title": "Followed by",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "hvr",
#      "caption": "This is our hvr table."
#    },
#    "product_fee": {
#      "content": "<span class=\"repAprLarge\">£995</span>",
#      "summary": "This is our fee table.",
#      "title": "Product fee",
#      "rate": "995",
#      "compare": "true",
#      "tableClass": "product_fee",
#      "caption": "This is our fee table."
#    }
#  }
#},{
#  "product": {
#    "footer": [],
#    "title": "2 Year Fixed Rate 75%",
#    "ID": "LM8660009291",
#    "product_detail": {
#      "title": "Find out more",
#      "extended_desc": [],
#      "link": "/mortgages/mortgage-products/M000335.asp",
#      "target": []
#    },
#    "apply_now": {
#      "title": "Start now",
#      "extended_desc": [],
#      "link": "/mortgages.asp#tab-row-6",
#      "target": []
#    }
#  },
#  "mortgages": {
#    "buyer_type": "first_time_buyer",
#    "payment": "962.32",
#    "loan_size": {
#      "content": "<p>Borrowing between £5,000 and £1,000,000</p>",
#      "summary": "This is our loan size table.",
#      "title": "Loan size",
#      "minimum": "5000",
#      "maximum": "1000000",
#      "compare": "true",
#      "tableClass": "loan_size",
#      "caption": "This is our loan size table."
#    },
#    "repayment": "repayment, interest_only",
#    "erc": {
#      "content": "3% until 31/08/2014, then 2% until 31/08/2015",
#      "summary": "This is our erc table.",
#      "title": "Early repayment charge",
#      "compare": "true",
#      "tableClass": "erc",
#      "caption": "This is our erc table."
#    },
#    "initial_rate": {
#      "content": "<span class=\"repAprLarge\">2.69%</span> fixed until 31/08/2015",
#      "summary": "This is our initial rate table.",
#      "title": "Initial rate",
#      "rate": "2.69",
#      "compare": "true",
#      "tableClass": "initial_rate",
#      "caption": "This is our initial rate table."
#    },
#    "overall_cost_for_comparison": {
#      "content": "<span class=\"repAprLarge\">4.0% APR</span>",
#      "summary": "This is our occ table.",
#      "title": "The overall cost for comparison is",
#      "rate": "4",
#      "compare": "true",
#      "tableClass": "occ",
#      "caption": "This is our occ table."
#    },
#    "offer": {
#      "content": "Only available for First-time buyers",
#      "title": "First-time buyer exclusive",
#      "link_text": "First-time buyer exclusive"
#    },
#    "mortgage_type": "fixed",
#    "ltv": {
#      "content": "<p><span class=\"repAprLarge\">75%</span> max,   60% min</p>",
#      "summary": "This is our loan to value table.",
#      "title": "Loan to value",
#      "minimum": "60",
#      "maximum": "75",
#      "compare": "true",
#      "tableClass": "ltv",
#      "caption": "This is our loan to value table."
#    },
#    "initial_term": "2",
#    "homeowner_variable_rate": {
#      "content": "Homeowner Variable Rate currently <span class=\"repAprLarge\">3.99%</span> for the remainder of the term",
#      "summary": "This is our hvr table.",
#      "title": "Followed by",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "hvr",
#      "caption": "This is our hvr table."
#    },
#    "product_fee": {
#      "content": "<span class=\"repAprLarge\">£995</span>",
#      "summary": "This is our fee table.",
#      "title": "Product fee",
#      "rate": "995",
#      "compare": "true",
#      "tableClass": "product_fee",
#      "caption": "This is our fee table."
#    }
#  }
#},{
#  "product": {
#    "footer": [],
#    "title": "2 Year Fixed Rate 75%",
#    "ID": "LM9318184361",
#    "product_detail": {
#      "title": "Find out more",
#      "extended_desc": [],
#      "link": "/mortgages/mortgage-products/M000333.asp",
#      "target": []
#    },
#    "apply_now": {
#      "title": "Start now",
#      "extended_desc": [],
#      "link": "/mortgages.asp#tab-row-6",
#      "target": []
#    }
#  },
#  "mortgages": {
#    "buyer_type": "first_time_buyer",
#    "payment": "930.50",
#    "loan_size": {
#      "content": "<p>Borrowing between £150,000 and £1,000,000</p>",
#      "summary": "This is our loan size table.",
#      "title": "Loan size",
#      "minimum": "150000",
#      "maximum": "1000000",
#      "compare": "true",
#      "tableClass": "loan_size",
#      "caption": "This is our loan size table."
#    },
#    "repayment": "repayment, interest_only",
#    "erc": {
#      "content": "3% until 31/08/2014, then 1.5% until 31/08/2015",
#      "summary": "This is our erc table.",
#      "title": "Early repayment charge",
#      "compare": "true",
#      "tableClass": "erc",
#      "caption": "This is our erc table."
#    },
#    "initial_rate": {
#      "content": "<span class=\"repAprLarge\">2.39%</span> fixed until 31/08/2015",
#      "summary": "This is our initial rate table.",
#      "title": "Initial rate",
#      "rate": "2.39",
#      "compare": "true",
#      "tableClass": "initial_rate",
#      "caption": "This is our initial rate table."
#    },
#    "overall_cost_for_comparison": {
#      "content": "<span class=\"repAprLarge\">4.0% APR</span>",
#      "summary": "This is our occ table.",
#      "title": "The overall cost for comparison is",
#      "rate": "4",
#      "compare": "true",
#      "tableClass": "occ",
#      "caption": "This is our occ table."
#    },
#    "offer": [],
#    "mortgage_type": "fixed",
#    "ltv": {
#      "content": "<p><span class=\"repAprLarge\">75%</span> max,   60% min</p>",
#      "summary": "This is our loan to value table.",
#      "title": "Loan to value",
#      "minimum": "60",
#      "maximum": "75",
#      "compare": "true",
#      "tableClass": "ltv",
#      "caption": "This is our loan to value table."
#    },
#    "initial_term": "2",
#    "homeowner_variable_rate": {
#      "content": "Homeowner Variable Rate currently <span class=\"repAprLarge\">3.99%</span> for the remainder of the term",
#      "summary": "This is our hvr table.",
#      "title": "Followed by",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "hvr",
#      "caption": "This is our hvr table."
#    },
#    "product_fee": {
#      "content": "<span class=\"repAprLarge\">£1,995</span>",
#      "summary": "This is our fee table.",
#      "title": "Product fee",
#      "rate": "1995",
#      "compare": "true",
#      "tableClass": "product_fee",
#      "caption": "This is our fee table."
#    }
#  }
#},{
#  "product": {
#    "footer": [],
#    "title": "5 Year Fixed Rate 75%",
#    "ID": "LM9911098599",
#    "product_detail": {
#      "title": "Find out more",
#      "extended_desc": [],
#      "link": "/mortgages/mortgage-products/M000247.asp",
#      "target": []
#    },
#    "apply_now": {
#      "title": "Start now",
#      "extended_desc": [],
#      "link": "/mortgages.asp#tab-row-6",
#      "target": []
#    }
#  },
#  "mortgages": {
#    "buyer_type": "first_time_buyer",
#    "payment": "1,084.25",
#    "loan_size": {
#      "content": "<p>Borrowing between £5,000 and £1,000,000</p>",
#      "summary": "This is our loan size table.",
#      "title": "Loan size",
#      "minimum": "5000",
#      "maximum": "1000000",
#      "compare": "true",
#      "tableClass": "loan_size",
#      "caption": "This is our loan size table."
#    },
#    "repayment": "repayment, interest_only",
#    "erc": {
#      "content": "5% until 31/08/2014, then 4% until 31/08/2015, then 3% until 31/08/2017, then 2% until 31/08/2018",
#      "summary": "This is our erc table.",
#      "title": "Early repayment charge",
#      "compare": "true",
#      "tableClass": "erc",
#      "caption": "This is our erc table."
#    },
#    "initial_rate": {
#      "content": "<span class=\"repAprLarge\">3.79%</span> fixed until 31/08/2018",
#      "summary": "This is our initial rate table.",
#      "title": "Initial rate",
#      "rate": "3.79",
#      "compare": "true",
#      "tableClass": "initial_rate",
#      "caption": "This is our initial rate table."
#    },
#    "overall_cost_for_comparison": {
#      "content": "<span class=\"repAprLarge\">4.1% APR</span>",
#      "summary": "This is our occ table.",
#      "title": "The overall cost for comparison is",
#      "rate": "4.1",
#      "compare": "true",
#      "tableClass": "occ",
#      "caption": "This is our occ table."
#    },
#    "offer": [],
#    "mortgage_type": "fixed",
#    "ltv": {
#      "content": "<p><span class=\"repAprLarge\">75%</span> max,   60% min</p>",
#      "summary": "This is our loan to value table.",
#      "title": "Loan to value",
#      "minimum": "60",
#      "maximum": "75",
#      "compare": "true",
#      "tableClass": "ltv",
#      "caption": "This is our loan to value table."
#    },
#    "initial_term": "5",
#    "homeowner_variable_rate": {
#      "content": "Homeowner Variable Rate currently <span class=\"repAprLarge\">3.99%</span> for the remainder of the term",
#      "summary": "This is our hvr table.",
#      "title": "Followed by",
#      "rate": "3.99",
#      "compare": "true",
#      "tableClass": "hvr",
#      "caption": "This is our hvr table."
#    },
#    "product_fee": {
#      "content": "<span class=\"repAprLarge\">£995</span>",
#      "summary": "This is our fee table.",
#      "title": "Product fee",
#      "rate": "995",
#      "compare": "true",
#      "tableClass": "product_fee",
#      "caption": "This is our fee table."
#    }
#  }
#}
#			]}
#
