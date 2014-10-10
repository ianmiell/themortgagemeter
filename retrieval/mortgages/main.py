# vim: set fileencoding=utf-8
import argparse, logging, logging.handlers, datetime, sys

# Import local modules
# Set up today's date
today = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
# Keep track of whether there have been any changes
changes = False
# Argument parsing
def main():
	global changes
	import mortgagecomparison_db
	import mortgagecomparison_utils
	mortgagecomparison_db.open_db()
	if args.logging == 'DEBUG':
		logger = mortgagecomparison_utils.setup_logging(logging.DEBUG,stdout=args.stdout)
	elif args.logging == 'INFO':
		logger = mortgagecomparison_utils.setup_logging(logging.INFO,stdout=args.stdout)
	elif args.logging == 'WARNING':
		logger = mortgagecomparison_utils.setup_logging(logging.WARNING,stdout=args.stdout)
	elif args.logging == 'ERROR':
		logger = mortgagecomparison_utils.setup_logging(logging.ERROR,stdout=args.stdout)
	elif args.logging == 'CRITICAL':
		logger = mortgagecomparison_utils.setup_logging(logging.CRITICAL,stdout=args.stdout)
	elif args.logging == 'STDOUT':
		logger = mortgagecomparison_utils.setup_logging(logging.CRITICAL,stdout=args.stdout)
	logger.info('Program starting: %s', args.institution)
	try:
		if args.institution == 'HSBC':
			import hsbc
			hsbc.hsbc_main(args.static,args.forcedelete,logger)
		elif args.institution == 'NTNWD':
			import nationwide
			nationwide.nationwide_main(args.static,args.forcedelete,logger)
		elif args.institution == 'LLOYDS':
			import lloyds
			lloyds.lloyds_main(args.static,args.forcedelete,logger)
		elif args.institution == 'SNTNDR':
			import santander
			santander.santander_main(args.static,args.forcedelete,logger)
		elif args.institution == 'HLFX':
			import halifax
			halifax.halifax_main(args.static,args.forcedelete,logger)
		elif args.institution == 'NTWST':
			import natwest
			natwest.natwest_main(args.static,args.forcedelete,logger)
		elif args.institution == 'NRTHNR':
			import northernrock
			northernrock.northernrock_main(args.static,args.forcedelete,logger)
		elif args.institution == 'CHLS':
			import chelsea
			chelsea.chelsea_main(args.static,args.forcedelete,logger)
		elif args.institution == 'YRKSHR':
			import yorkshire
			yorkshire.yorkshire_main(args.static,args.forcedelete,logger)
		elif args.institution == 'TSC':
			import tesco
			tesco.tesco_main(args.static,args.forcedelete,logger)
		elif args.institution == 'SKPTN':
			import skipton
			skipton.skipton_main(args.static,args.forcedelete,logger)
		elif args.institution == 'PSTFFC':
			import post_office
			post_office.post_office_main(args.static,args.forcedelete,logger)
		elif args.institution == 'FRSTDRCT':
			import first_direct
			first_direct.first_direct_main(args.static,args.forcedelete,logger)
		else:
			raise Exception('Need to supply an institution','')
		if not args.test:
			mortgagecomparison_db.db_connection.commit()
		else:
			logger.info('Not committing data, as --test passed in')
			mortgagecomparison_db.db_connection.rollback()
	except Exception as e:
		logger.critical('Error was thrown, quitting')
		logger.exception('Error was:')
		mortgagecomparison_utils.record_alert('ERROR: ' + args.institution,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
	logger.info('Program complete for institution: %s', args.institution)
	# TOOD: why does this never seem to be set to true?
	global changes
	logger.info('Changes is: ' + str(changes))
	mortgagecomparison_db.commit_db()

def update_changes(val,institution_code,logger):
	global changes
	logger.info('Updating changes bool. Changes currently set to: ' + str(changes))
	if changes != val:
		import mortgagecomparison_db
		import mortgagecomparison_utils
		changes = val
		logger.info('Changes changed to: ' + str(val))
		mortgagecomparison_utils.record_alert('MORTGAGE_CHANGE: ' + institution_code,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)

if __name__ == '__main__':
	sys.path.append('/opt/themortgagemeter/shared')
	parser = argparse.ArgumentParser(description='Get mortgage rates')
	parser.add_argument('--static', help='whether to use static files for testing', default=False, action='store_true')
	parser.add_argument('--institution', help='which institution code to do',required=True,choices=['NTNWD','HSBC','LLOYDS','SNTNDR','HLFX','NTWST','NRTHNR','CHLS','YRKSHR','TSC','SKPTN','PSTFFC','FRSTDRCT'])
	parser.add_argument('--test', help='test, ie do not commit data',default=False, action='store_true')
	parser.add_argument('--logging', help='logging level',default='INFO', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
	parser.add_argument('--stdout', help='logging level',default=False, action='store_true')
	parser.add_argument('--forcedelete', help='force the delete of all mortgages for the insitution', default=False, action='store_true')
	args = parser.parse_args()
	main()

