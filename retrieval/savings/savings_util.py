# vim: set fileencoding=utf-8
# Utility functions
import main
import urllib2
import html5lib
import re
import string
import themortgagemeter_utils
import themortgagemeter_db
import savings_db

import unittest

# Given a string, extracts the percent value as a decimal string
# Returns blank string if none could be found

# Expected data are strings.
def check_data(isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid, logger):
	# Now we check that the values we have are the right type:
	if themortgagemeter_utils.isnumber(regular_saver_frequency_period) != True:
		logger.critical('problem with regular_saver_frequency_period - not a number:' + regular_saver_frequency_period)
		themortgagemeter_utils.record_alert('ERROR: problem with regular_saver_frequency_period - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(regular_saver_min_amt) != True:
		logger.critical('problem with regular_saver_min_amt - not a number: ' + regular_saver_min_amt)
		themortgagemeter_utils.record_alert('ERROR: problem with regular_saver_min_amt',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(regular_saver_max_amt) != True:
		logger.critical('problem with regular_saver_max_amt - not a number:' + regular_saver_max_amt)
		themortgagemeter_utils.record_alert('ERROR: problem with regular_saver_max_amt - not a number:',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(bonus_frequency_period) != True:
		logger.critical('problem with bonus_frequency_period - not a number:' + bonus_frequency_period)
		themortgagemeter_utils.record_alert('ERROR: problem with bonus_frequency_period - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(savings_period) != True:
		logger.critical('problem with savings_period - not a number:' + savings_period)
		themortgagemeter_utils.record_alert('ERROR: problem with savings_period - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(min_amt) != True:
		logger.critical('problem with min_amt - not a number:' + min_amt)
		themortgagemeter_utils.record_alert('ERROR: problem with min_amt - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(max_amt) != True:
		logger.critical('problem with max_amt - not a number:' + max_amt)
		themortgagemeter_utils.record_alert('ERROR: problem with max_amt - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(gross_percent) != True:
		logger.critical('problem with gross_percent - not a number:' + gross_percent)
		themortgagemeter_utils.record_alert('ERROR: problem with gross_percent - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	elif themortgagemeter_utils.isnumber(aer_percent) != True:
		logger.critical('problem with aer_percent - not a number:' + aer_percent)
		themortgagemeter_utils.record_alert('ERROR: problem with aer_percent - not a number: ',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()


# Handle the insert of savings details, not adding if already there and inserting retrieval record.
# 
# Expects data are strings, even
# percents and number are expected to be a string, and decimal, eg "4.50"
# 
def handle_savings_insert(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid, url, logger):
	logger.debug(institution_code)
	logger.debug(isa)
	logger.debug(regular_saver)
	logger.debug(regular_saver_frequency_period)
	logger.debug(regular_saver_frequency_type)
	logger.debug(regular_saver_min_amt)
	logger.debug(regular_saver_max_amt)
	logger.debug(bonus)
	logger.debug(bonus_frequency_period)
	logger.debug(bonus_frequency_type)
	logger.debug(online)
	logger.debug(branch)
	logger.debug(variability)
	logger.debug(savings_period)
	logger.debug(min_amt)
	logger.debug(max_amt)
	logger.debug(gross_percent)
	logger.debug(aer_percent)
	logger.debug(child)
	logger.debug(interest_paid)
	check_data(isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid, logger)
	regular_saver_frequency_period_int      = int(regular_saver_frequency_period)
	savings_period_int          = int(savings_period)
	regular_saver_min_amt_int   = int(float(regular_saver_min_amt) * 100)
	regular_saver_max_amt_int   = int(float(regular_saver_max_amt) * 100)
	bonus_frequency_period_int  = int(float(bonus_frequency_period) * 100)
	min_amt_int                 = int(float(min_amt) * 100)
	max_amt_int                 = int(float(max_amt) * 100)
	gross_percent_int           = int(float(gross_percent) * 100)
	aer_percent_int             = int(float(aer_percent) * 100)
	if savings_db.is_savings_there(institution_code, isa, regular_saver, regular_saver_frequency_period_int, regular_saver_frequency_type, regular_saver_min_amt_int, regular_saver_max_amt_int, bonus, bonus_frequency_period_int, bonus_frequency_type, online, branch, variability, savings_period_int, min_amt_int, max_amt_int, gross_percent_int, aer_percent_int, child, interest_paid) == 0:
		logger.debug('Savings being added')
		savings_id = savings_db.insert_savings(institution_code, isa, regular_saver, regular_saver_frequency_period_int, regular_saver_frequency_type, regular_saver_min_amt_int, regular_saver_max_amt_int, bonus, bonus_frequency_period_int, bonus_frequency_type, online, branch, variability, savings_period_int, min_amt_int, max_amt_int, gross_percent_int, aer_percent_int, child, interest_paid)
		main.update_changes(True,institution_code,logger)
	else:
		logger.debug('Savings already there')
		savings_id = savings_db.get_savings_id(institution_code, isa, regular_saver, regular_saver_frequency_period_int, regular_saver_frequency_type, regular_saver_min_amt_int, regular_saver_max_amt_int, bonus, bonus_frequency_period_int, bonus_frequency_type, online, branch, variability, savings_period_int, min_amt_int, max_amt_int, gross_percent_int, aer_percent_int, child, interest_paid)
	# Get the url id:
	url_id = savings_db.get_url_id_insert_if_there(url)
	savings_db.update_savings_jrnl(main.today,savings_id,url_id,institution_code)


# Returns a new instance of a savings data object.
def get_savings_data_object():
	savings_data = {}
	savings_data['isa']                              = 'N'
	savings_data['regular_saver']                    = 'N'
	savings_data['regular_saver_frequency_period']   = '-1'
	savings_data['regular_saver_frequency_type']     = 'M' #D/M/Y
	savings_data['regular_saver_min_amt']            = '-1'
	savings_data['regular_saver_max_amt']            = '-1'
	savings_data['bonus']                            = 'N'
	savings_data['bonus_frequency_period']           = '-1' #n
	savings_data['bonus_frequency_type']             = 'Y' #D/M/Y
	savings_data['online']                           = 'N'
	savings_data['branch']                           = 'N'
	# fixed/variable pages
	savings_data['variability']                      = 'V' #'F'ixed, 'V'ariable
	savings_data['savings_period']                   = '-1'
	savings_data['min_amt']                          = '1'
	# -1 == infinity
	savings_data['max_amt']                          = '-1'
	savings_data['gross_percent']                    = '-1'
	savings_data['aer_percent']                      = '-1'
	savings_data['child']                            = 'N'
	savings_data['interest_paid']                    = 'U' #'Y'early, 'M'onthly, 'U'nknown
	return savings_data

# Given a string, determine the lower and upper range of money
# returns two numbers as an array
# default min is "0", default max is "-1"
def get_money_range(s,logger):
	res = ["0","-1"]
	s = s.strip()
	if re.match('^.*\+$',s):
		money_val = themortgagemeter_utils.get_money(s,logger)
		res[0] = money_val
	elif re.match('^.*up to.*$',s) or re.match('^.*under.*$',s):
		money_val = themortgagemeter_utils.get_money(s,logger)
		res[1] = money_val
	elif re.match('^.*or more$',s):
		index = s.find("£")
		s = s[index:]
		res[0] = s.split()[0][2:].translate(None,',')
	elif re.match('^.* - .*$',s):
		index = s.find("£")
		s = s[index:]
		res[0] = s.split()[0][2:].translate(None,',')
		res[1] = s.split()[2][2:].translate(None,',')
	elif re.match('^.*[0-9] to .*$',s):
		index = s.find("£")
		s = s[index:]
		res[0] = s.split()[0][2:].translate(None,',')
		res[1] = s.split()[2][2:].translate(None,',')
	else:
		#logger.info(t) #logger.info('value not handled: ' + s)
		themortgagemeter_utils.record_alert('ERROR: value not properly parsed by get_money_range: ' + s,logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	return res


