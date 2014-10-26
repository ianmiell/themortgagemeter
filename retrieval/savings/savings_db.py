# vim: set fileencoding=utf-8
import pgdb
import logging
import themortgagemeter_db
import themortgagemeter_queries
import themortgagemeter_utils
import main

# SQL
sql_is_savings_there                 = '''
	select count(*)
	from tsavings
	where
	institution_code = %s and
	isa = %s and
	regular_saver = %s and
	regular_saver_frequency_period = %s and
	regular_saver_frequency_type = %s and
	regular_saver_min_amt = %s and
	regular_saver_max_amt = %s and
	bonus = %s and
	bonus_frequency_period = %s and
	bonus_frequency_type = %s and
	online = %s and
	branch = %s and
	variability = %s and
	savings_period = %s and
	min_amt = %s and
	max_amt = %s and
	gross_percent = %s and
	aer_percent = %s and
	child = %s and
	interest_paid = %s'''
sql_get_savings_there                = '''
	select savings_id 
	from tsavings
	where 
	institution_code = %s and
	isa = %s and
	regular_saver = %s and
	regular_saver_frequency_period = %s and
	regular_saver_frequency_type = %s and
	regular_saver_min_amt = %s and
	regular_saver_max_amt = %s and
	bonus = %s and
	bonus_frequency_period = %s and
	bonus_frequency_type = %s and
	online = %s and
	branch = %s and
	variability = %s and
	savings_period = %s and
	min_amt = %s and
	max_amt = %s and
	gross_percent = %s and
	aer_percent = %s and
	child = %s and
	interest_paid = %s'''
sql_insert_savings                   = '''
	insert into tsavings
	(institution_code,
	 isa,
	 regular_saver,
	 regular_saver_frequency_period,
	 regular_saver_frequency_type,
	 regular_saver_min_amt,
	 regular_saver_max_amt,
	 bonus,
	 bonus_frequency_period,
	 bonus_frequency_type,
	 online,
	 branch,
	 variability,
	 savings_period,
	 min_amt,
	 max_amt,
	 gross_percent,
	 aer_percent,
	 child,
	 interest_paid)
	values 
	(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
sql_is_savings_jrnl_there = '''
	select count(*) from tsavingsjrnl where delete_date is null and savings_id = %s
'''
sql_count_savings_jrnl_institution_there = '''
	select count(*) from tsavingsjrnl j, tsavings s where s.savings_id = j.savings_id and delete_date is null and institution_code = %s
'''
sql_get_savings_jrnl_there = '''
	select savings_jrnl_id from tsavingsjrnl where delete_date is null and savings_id = %s
'''
sql_update_savings_jrnl_delete           = '''
	update tsavingsjrnl set delete_date = %s where delete_date is null and savings_id = %s
'''
sql_update_savings_jrnl_retrieval           = '''
	update tsavingsjrnl set last_retrieved = %s, url_id = %s where delete_date is null and savings_id = %s
'''
sql_insert_savings_jrnl           = '''
	insert into tsavingsjrnl (cr_date,savings_id,last_retrieved,url_id) values (%s,%s,%s,%s)
'''
sql_get_savings_not_retrieved_on_date = '''
	select s.savings_id
	from tsavingsjrnl sj, tsavings s
	where
	s.institution_code = %s and s.savings_id = sj.savings_id and sj.delete_date is null and sj.last_retrieved != %s'''
sql_is_url_there                      = '''select count(*) from turl where url = %s'''
sql_get_url_id                        = '''select url_id from turl where url = %s'''
sql_insert_url                        = '''insert into turl (url) values (%s)'''

def get_url_id_insert_if_there(url):
	if not themortgagemeter_db.is_item_there(sql_is_url_there,(url,)):
		themortgagemeter_db.run_sql(sql_insert_url,(url,))
	return themortgagemeter_db.get_item_id(sql_get_url_id,(url,))

# Returns 1 if the mortgage is already there, else 0
def is_savings_there(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid):
	return themortgagemeter_db.is_item_there(sql_is_savings_there,(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid))

# Will insert the mortgage if needed, returning the mortgage_id
def insert_savings(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid):
	logger = logging.getLogger('retrieve')
	logger.info('Inserting savings %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s', institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid)
	themortgagemeter_db.run_sql(sql_insert_savings,(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid))
	return get_savings_id(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid)

def update_savings_jrnl(date,savings_id,url_id,institution_code):
	logger = logging.getLogger('retrieve')
	logger.info('%s Updating retrieval savings %s', institution_code, savings_id)
	# insert if not there.
	if not themortgagemeter_db.is_item_there(sql_is_savings_jrnl_there,(savings_id,)):
		themortgagemeter_db.run_sql(sql_insert_savings_jrnl,(date,savings_id,date,url_id))
	else:
		savings_jrnl_id = themortgagemeter_db.get_item_id(sql_get_savings_jrnl_there,(savings_id,))
		themortgagemeter_db.run_sql(sql_update_savings_jrnl_retrieval,(date,url_id,savings_id))


# Gets the mortgage id that matches the mortgage details.
def get_savings_id(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid):
	return themortgagemeter_db.get_item_id(sql_get_savings_there,(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid))

def delete_savings_not_current(institution_code,date,forcedelete,logger):
	logger = logging.getLogger('retrieve')
	logger.info('In delete_savings_not_current')
	themortgagemeter_db.cursor.execute(sql_count_savings_jrnl_institution_there,(institution_code,))
	row = themortgagemeter_db.cursor.fetchone()
	count = int(row[0])
	deletecount = 0
	logger.info('There are %s savings rows currently',count)
	themortgagemeter_db.cursor.execute(sql_get_savings_not_retrieved_on_date,(institution_code,date))
	for row in themortgagemeter_db.cursor.fetchall():
		savings_id = row[0]
		logger.info('Deleting current savings: %s %s %s', institution_code, date, savings_id)
		themortgagemeter_db.run_sql(sql_update_savings_jrnl_delete,(date, savings_id))
		deletecount += 1
		main.update_changes(True,institution_code,logger)
	logger.info('%s savings rows deleted',(int(deletecount)))
	if count > 0 and deletecount == count and forcedelete == False:
		themortgagemeter_utils.record_error('Would have deleted all savings rows for ' + institution_code + ', check logs',logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
		exit()
	return

# Updates current data for today
def update_savings_current(institution_code,today,forcedelete,logger):
	delete_savings_not_current(institution_code,today,forcedelete,logger)

