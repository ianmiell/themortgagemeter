import sys
sys.path.append('../../simple_mailer')
sys.path.append('../../shared')
import simple_mailer
import mortgagecomparison_db
import mortgagecomparison_utils
import logging
import os
import time
import random

# TODO: logging

sender                  = 'SENDEREMAIL'
contentfile             = None
subject                 = 'Change to rates on themortgagemeter.com'
mortgage_change_content = 'There has been a change of rates on http://themortgagemeter.com. Go to:\n\nhttp://themortgagemeter.com/#/latest_changes\n\nto see what\'s changed.\n\nIf you have any comments about the site or wish to unsubscribe, please reply to this mail.'
error_content           = 'There has been an error in the logs.'
passfile                = '/opt/mortgagecomparison/conf/mailpass'
hostname                = os.uname()[1]

qry_get_mortgage_change_alerts = """
	select alert_id, alert
	from talert
	where 
	cr_date > current_date
	and alert like 'MORTGAGE_CHANGE%'
	and status = 'A'
	limit 1
"""

qry_get_error_alerts = """
	select alert_id, alert
	from talert
	where 
	cr_date > current_date
	and alert like 'ERROR%'
	and status = 'A'
	limit 1
"""

qry_delete_mortgage_change_alerts = """ update talert set status = 'D' where alert like 'MORTGAGE_CHANGE%' """
qry_delete_error_alerts = """ update talert set status = 'D' where alert like 'ERROR%' """

qry_get_mailsubscribers = """
	select email_address
	from tmailsubscriber
"""

def main():
	global sender
	global contentfile
	global subject
	global mortgage_change_content
	global error_content
	global passfile
	mortgagecomparison_db.open_db()
	# Perform qry_get_mortgage_change_alerts query
	# for each alert_id, send an email
	# If the email is successful, delete the row from the table, commit and continue.

	# Now mortgage change alerts.
	mortgagecomparison_db.cursor.execute(qry_get_mortgage_change_alerts)
	alert_rows = mortgagecomparison_db.cursor.fetchall()
	mortgagecomparison_db.cursor.execute(qry_get_mailsubscribers)
	subscriber_rows = mortgagecomparison_db.cursor.fetchall()
	print "Rows returned"
	print alert_rows
	for alert_row in alert_rows:
		print "alert row"
		print alert_row
		alert_id = alert_row[0]
		alert = alert_row[1]
		print "subscriber rows"
		for subscriber_row in subscriber_rows:
			print subscriber_row
			to = subscriber_row[0]
			# Send alert to subscriber
			# Wait a random length of time in case this triggers spam filters.
			time.sleep(random.randint(10,20))
			simple_mailer.main(sender,to,passfile,subject,contentfile,mortgage_change_content)
	# if we are here, we assume all has gone OK, and we delete the relevant alerts
	mortgagecomparison_db.cursor.execute(qry_delete_mortgage_change_alerts)

	# Now errors.
	mortgagecomparison_db.cursor.execute(qry_get_error_alerts)
	alert_rows = mortgagecomparison_db.cursor.fetchall()
	for alert_row in alert_rows:
		alert_id = alert_row[0]
		alert = alert_row[1]
		simple_mailer.main(sender,'MORTGAGECOMPARISON_ADMINEMAIL',passfile,subject,contentfile,error_content)
	# if we are here, we assume all has gone OK, and we delete the relevant alerts
	mortgagecomparison_db.cursor.execute(qry_delete_error_alerts)

	# cleanup
	mortgagecomparison_db.commit_db()



if __name__ == '__main__':
	main()
