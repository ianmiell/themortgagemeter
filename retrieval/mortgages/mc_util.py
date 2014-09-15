# vim: set fileencoding=utf-8
# Utility functions
import mc_db
import main
import urllib2
import html5lib
import re
import string
import mortgagecomparison_utils
import mortgagecomparison_db

# Given a string, extracts the percent value as a decimal string
# Returns blank string if none could be found


# Takes string like "5 years fixed" and returns mortgage type
def get_mortgage_type(s,logger):
	str_lower = s.lower()
	res = re.match(r'^.*(fixed|tracker|variable|discount).*$',mortgagecomparison_utils.remove_non_ascii(str_lower))
	type_str = res.group(1)
	if type_str == 'fixed':
		mortgage_type = 'F'
	elif type_str == 'tracker' or type_str == 'variable' or type_str == 'discount':
		mortgage_type = 'T'
	else:
		logger.critical('unable to determine mortgage_type from str: ' + type_str)
		mortgagecomparison_utils.record_alert('ERROR: unable to determine mortgage_type from str',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
	return mortgage_type


def check_data(rate_percent,booking_fee,ltv_percent,apr_percent,initial_period,logger):
	# Now we check that the values we have are the right type:
	if mortgagecomparison_utils.isnumber(rate_percent) != True:
		logger.critical('problem with rate_percent:' + rate_percent)
		mortgagecomparison_utils.record_alert('ERROR: problem with rate_percent',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	elif booking_fee.isdigit() != True:
		logger.critical('problem with booking_fee:' + booking_fee)
		mortgagecomparison_utils.record_alert('ERROR: problem with booking_fee',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	elif mortgagecomparison_utils.isnumber(ltv_percent) != True:
		logger.critical('problem with ltv_percent: ' + ltv_percent)
		mortgagecomparison_utils.record_alert('ERROR: problem with ltv_percent',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	elif mortgagecomparison_utils.isnumber(apr_percent) != True:
		logger.critical('problem with apr_percent: ' + apr_percent)
		mortgagecomparison_utils.record_alert('ERROR: problem with apr_percent',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	# mortgage type must be ok
	elif str(initial_period).isdigit() != True:
		logger.critical('problem with initial_period: ' + str(initial_period))
		mortgagecomparison_utils.record_alert('ERROR: problem with initial_period',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()


# Handle the insert of mortgage details, not adding if already there and inserting retrieval record.
# 
# percents are expected to be a string, and decimal, eg 4.50
# 
def handle_mortgage_insert(institution_code, mortgage_type, rate_percent, svr_percent, apr_percent, ltv_percent, initial_period, booking_fee, term, url, eligibility, logger):
	logger.debug(institution_code)
	logger.debug(mortgage_type)
	logger.debug(rate_percent)
	logger.debug(svr_percent)
	logger.debug(apr_percent)
	logger.debug(ltv_percent)
	logger.debug(initial_period)
	logger.debug(booking_fee)
	logger.debug(term)
	logger.debug(url)
	logger.debug(eligibility)
	check_data(rate_percent,booking_fee,ltv_percent,apr_percent,initial_period,logger)
	rate_percent_int = int(float(rate_percent) * 100)
	apr_percent_int = int(float(apr_percent) * 100)
	ltv_percent_int = int(float(ltv_percent) * 100)
	svr_percent_int = int(float(svr_percent) * 100)
	if mc_db.is_mortgage_there(institution_code, mortgage_type, rate_percent_int, svr_percent_int, apr_percent_int, ltv_percent_int, initial_period, booking_fee, term, eligibility) == 0:
		logger.debug('Mortgage being added')
		mortgage_id = mc_db.insert_mortgage(institution_code, mortgage_type, rate_percent_int, svr_percent_int, apr_percent_int, ltv_percent_int, initial_period, booking_fee, term, eligibility)
		main.update_changes(True,institution_code,logger)
	else:
		logger.debug('Mortgage already there')
		mortgage_id = mc_db.get_mortgage_id(institution_code, mortgage_type, rate_percent_int, svr_percent_int, apr_percent_int, ltv_percent_int, initial_period, booking_fee, term, eligibility)
	# Get the url id:
	url_id = mc_db.get_url_id_insert_if_there(url)
	mc_db.update_jrnl(main.today,mortgage_id,url_id,institution_code)


# Returns a basic eligibility dict
# See conversions.py in shared
#   <type> = Truth value of: existing_customer,ftb,moving_home,borrowing_more,remortgage,switching
#   NFTB   = F,T,F,F,F,F
#   NMH    = F,F,T,F,F,F
#   NRM    = F,F,F,F,T,F
#   EDE    = T,F,F,F,T,F
#   EMH    = T,F,T,F,F,F
#   EBM    = T,F,F,T,F,F
#   EED    = T,F,F,F,F,T

# Return a raw mortgage eligibility dict
def get_mortgage_eligibility_dict():
	return {'existing_customer' : 'F', 'ftb' : 'F', 'moving_home' : 'F', 'borrowing_more' : 'F', 'remortgage' : 'F', 'switching' : 'F'}

# Takes a list of eligibility data - and returns list of matching eligibilities.
# eg if a deal is open to existing and new customers, it will return the E* and N* codes
# eg if a deal if true for all it will return all codes.
# B = "Both"
# T = "True"
# F = "False"
def validate_eligibility_dict(eligibility_dict,list_so_far):
	#print eligibility_dict
	#print list_so_far
	for key in eligibility_dict.keys():
		if eligibility_dict[key] == 'B':
			a = eligibility_dict.copy()
			b = eligibility_dict.copy()
			a[key] = 'T'
			b[key] = 'F'
			return validate_eligibility_dict(a,list_so_far) + validate_eligibility_dict(b,list_so_far)
	if eligibility_dict == {'existing_customer' : 'F', 'ftb' : 'T', 'moving_home' : 'F', 'borrowing_more' : 'F', 'remortgage' : 'F', 'switching' : 'F'}:
		return list_so_far + ['NFTB']
	elif eligibility_dict == {'existing_customer' : 'F', 'ftb' : 'F', 'moving_home' : 'T', 'borrowing_more' : 'F', 'remortgage' : 'F', 'switching' : 'F'}:
		return list_so_far + ['NMH']
	elif eligibility_dict == {'existing_customer' : 'F', 'ftb' : 'F', 'moving_home' : 'F', 'borrowing_more' : 'F', 'remortgage' : 'T', 'switching' : 'F'}:
		return list_so_far + ['NRM']
	elif eligibility_dict == {'existing_customer' : 'T', 'ftb' : 'F', 'moving_home' : 'F', 'borrowing_more' : 'F', 'remortgage' : 'T', 'switching' : 'F'}:
		return list_so_far + ['EDE']
	elif eligibility_dict == {'existing_customer' : 'T', 'ftb' : 'F', 'moving_home' : 'T', 'borrowing_more' : 'F', 'remortgage' : 'F', 'switching' : 'F'}:
		return list_so_far + ['EMH']
	elif eligibility_dict == {'existing_customer' : 'T', 'ftb' : 'F', 'moving_home' : 'F', 'borrowing_more' : 'T', 'remortgage' : 'F', 'switching' : 'F'}:
		return list_so_far + ['EBM']
	elif eligibility_dict == {'existing_customer' : 'T', 'ftb' : 'F', 'moving_home' : 'F', 'borrowing_more' : 'F', 'remortgage' : 'F', 'switching' : 'T'}:
		return list_so_far + ['EED']
	else:
		return list_so_far

