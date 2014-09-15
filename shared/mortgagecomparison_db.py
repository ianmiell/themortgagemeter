# vim: set fileencoding=utf-8
import pgdb
import logging
import mortgagecomparison_queries
import mortgagecomparison_utils

# Name of db - TODO: make this a parameter of init or something
# TODO: do we need a cursor that's global?
db_connection = None
cursor        = None

# Shut the db connection etc cleanly.
def open_db():
	global db_connection
	global cursor
	db_connection = pgdb.connect(host='''localhost''',database='''mortgagecomparison''',user='''themortgagemeter''',password='''postgres''')
	cursor = db_connection.cursor()

# Shut the db connection etc cleanly.
def commit_db():
	db_connection.commit()
	cursor.close()
	db_connection.close()
	
# Helper functions
def is_item_there(sql,args_tuple):
	logger = logging.getLogger('retrieve')
	logger.debug('Running sql: %s',(sql % args_tuple))
	cursor.execute(sql, args_tuple)
	row = cursor.fetchone()
	count = row[0]
	if count < 1:
		return False
	else:
		return True

def get_item_id(sql,args_tuple):
	logger = logging.getLogger('retrieve')
	logger.debug('Running sql: %s',(sql % args_tuple))
	cursor.execute(sql, args_tuple)
	row = cursor.fetchone()
	return row[0]

# Run some sql and foreget about it
def run_sql(sql,args_tuple):
	logger = logging.getLogger('retrieve')
	logger.debug('Running sql: %s',(sql % args_tuple))
	cursor.execute(sql, args_tuple)
	return

def record_error(s,cursor=None):
    logger = logging.getLogger('retrieve')
    if cursor == None:
        cursor = db_connection.cursor()
    mortgagecomparison_utils.record_error(s,logger,db_connection,cursor)

