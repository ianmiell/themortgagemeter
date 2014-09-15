# vim: set fileencoding=utf-8
import argparse, logging, logging.handlers, datetime, sys

# Import local modules
# Set up today's date
today = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
# Argument parsing
def main():
	import mortgagecomparison_db
	import mortgagecomparison_utils
	mortgagecomparison_db.open_db()
	if args.logging == 'DEBUG':
		logger = mortgagecomparison_utils.setup_logging(logging.DEBUG)
	elif args.logging == 'INFO':
		logger = mortgagecomparison_utils.setup_logging(logging.INFO)
	elif args.logging == 'WARNING':
		logger = mortgagecomparison_utils.setup_logging(logging.WARNING)
	elif args.logging == 'ERROR':
		logger = mortgagecomparison_utils.setup_logging(logging.ERROR)
	elif args.logging == 'CRITICAL':
		logger = mortgagecomparison_utils.setup_logging(logging.CRITICAL)
	logger.info('Program starting: %s', args.institution)
	try:
		if args.institution == 'ONS':
			import ons
			ons.ons_main()
			print 'asd'
		else:
			raise Exception('Need to supply an institution','')
		if not args.test:
			mortgagecomparison_db.db_connection.commit()
		else:
			logger.info('Not committing data, as --test passed in')
	except Exception as e:
		logger.critical('Error was thrown, quitting')
		logger.exception('Error was:')
	logger.info('Program complete for institution: %s', args.institution)
	mortgagecomparison_db.commit_db()

if __name__ == '__main__':
	sys.path.append('/opt/mortgagecomparison/shared')
	parser = argparse.ArgumentParser(description='Get mortgage rates')
	parser.add_argument('--institution', help='which institution code to do',required=True,choices=['ONS'])
	parser.add_argument('--test', help='test, ie do not commit data',default=False, action='store_true')
	parser.add_argument('--logging', help='logging level',default='INFO', choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
	args = parser.parse_args()
	main()

