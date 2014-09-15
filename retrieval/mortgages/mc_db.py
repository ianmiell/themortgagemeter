# vim: set fileencoding=utf-8
import pgdb
import logging
import mortgagecomparison_db
import mortgagecomparison_queries
import mortgagecomparison_utils
import main

# SQL
sql_is_mortgage_there                 = '''
	select count(*)
	from tmortgage
	where
	institution_code = %s and
	mortgage_type = %s and
	rate = %s and
	svr = %s and
	apr = %s and
	ltv = %s and
	initial_period = %s
	and booking_fee = %s and
	term = %s and
	eligibility = %s'''
sql_get_mortgage_there                = '''
	select mortgage_id 
	from tmortgage 
	where 
	institution_code = %s and mortgage_type = %s and
	rate = %s and
	svr = %s and
	apr = %s and
	ltv = %s and
	initial_period = %s and
	booking_fee = %s and
	term = %s and
	eligibility = %s'''
sql_insert_mortgage                   = '''
	insert into tmortgage 
	(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility)
	values 
	(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
sql_is_jrnl_there = '''
	select count(*) from tmortgagejrnl where delete_date is null and mortgage_id = %s
'''
sql_count_jrnl_institution_there = '''
	select count(*) from tmortgagejrnl j, tmortgage m where m.mortgage_id = j.mortgage_id and delete_date is null and institution_code = %s
'''
sql_get_jrnl_there = '''
	select mortgage_jrnl_id from tmortgagejrnl where delete_date is null and mortgage_id = %s
'''
sql_update_mortgage_jrnl_delete           = '''
	update tmortgagejrnl set delete_date = %s where delete_date is null and mortgage_id = %s
'''
sql_update_mortgage_jrnl_retrieval           = '''
	update tmortgagejrnl set last_retrieved = %s, url_id = %s where delete_date is null and mortgage_id = %s
'''
sql_insert_mortgage_jrnl           = '''
	insert into tmortgagejrnl (cr_date,mortgage_id,last_retrieved,url_id) values (%s,%s,%s,%s)
'''
sql_get_mortgages_not_retrieved_on_date = '''
	select m.mortgage_id
	from tmortgagejrnl mj, tmortgage m
	where
	m.institution_code = %s and m.mortgage_id = mj.mortgage_id and mj.delete_date is null and mj.last_retrieved != %s'''
sql_is_url_there                      = '''select count(*) from turl where url = %s'''
sql_get_url_id                        = '''select url_id from turl where url = %s'''
sql_insert_url                        = '''insert into turl (url) values (%s)'''

def get_url_id_insert_if_there(url):
	if not mortgagecomparison_db.is_item_there(sql_is_url_there,(url,)):
		mortgagecomparison_db.run_sql(sql_insert_url,(url,))
	return mortgagecomparison_db.get_item_id(sql_get_url_id,(url,))

# Returns 1 if the mortgage is already there, else 0
def is_mortgage_there(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility):
	return mortgagecomparison_db.is_item_there(sql_is_mortgage_there,(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility))

# Will insert the mortgage if needed, returning the mortgage_id
def insert_mortgage(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility):
	logger = logging.getLogger('retrieve')
	logger.info('Inserting mortgage: %s %s %s %s %s %s %s %s %s %s', institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility)
	mortgagecomparison_db.run_sql(sql_insert_mortgage,(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility))
	return get_mortgage_id(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility)

def update_jrnl(date,mortgage_id,url_id,institution_code):
	logger = logging.getLogger('retrieve')
	logger.info('%s Updating retrieval mortgage %s', institution_code, mortgage_id)
	# insert if not there.
	if not mortgagecomparison_db.is_item_there(sql_is_jrnl_there,(mortgage_id,)):
		mortgagecomparison_db.run_sql(sql_insert_mortgage_jrnl,(date,mortgage_id,date,url_id))
	else:
		mortgage_jrnl_id = mortgagecomparison_db.get_item_id(sql_get_jrnl_there,(mortgage_id,))
		mortgagecomparison_db.run_sql(sql_update_mortgage_jrnl_retrieval,(date,url_id,mortgage_id))


# Gets the mortgage id that matches the mortgage details.
def get_mortgage_id(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term, eligibility):
	return mortgagecomparison_db.get_item_id(sql_get_mortgage_there,(institution_code, mortgage_type, rate, svr, apr, ltv, initial_period, booking_fee, term,  eligibility))

def delete_mortgages_not_current(institution_code,date,forcedelete,logger):
	logger = logging.getLogger('retrieve')
	logger.info('In delete_mortgages_not_current')
	mortgagecomparison_db.cursor.execute(sql_count_jrnl_institution_there,(institution_code,))
	row = mortgagecomparison_db.cursor.fetchone()
	count = int(row[0])
	deletecount = 0
	logger.info('There are %s mortgages currently',count)
	mortgagecomparison_db.cursor.execute(sql_get_mortgages_not_retrieved_on_date,(institution_code,date))
	for row in mortgagecomparison_db.cursor.fetchall():
		mortgage_id = row[0]
		logger.info('Deleting current mortgage: %s %s %s', institution_code, date, mortgage_id)
		mortgagecomparison_db.run_sql(sql_update_mortgage_jrnl_delete,(date, mortgage_id))
		deletecount += 1
		main.update_changes(True,institution_code,logger)
	logger.info('%s mortgages deleted',(int(deletecount)))
	if count > 0 and deletecount == count and forcedelete == False:
		mortgagecomparison_utils.record_error('ERROR: Would have deleted all mortgages for ' + institution_code + ', check logs',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	return

# Updates current data for today
def update_current(institution_code,today,forcedelete,logger):
	delete_mortgages_not_current(institution_code,today,forcedelete,logger)
