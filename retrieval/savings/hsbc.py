# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import re
import datetime
import logging

import main
import savings_db
import savings_util

import themortgagemeter_utils
import themortgagemeter_db

institution_code = 'HSBC'

def get_product_pages(static,base_url,ext):
	logger = logging.getLogger('retrieve')
	bsobj = themortgagemeter_utils.get_page(static,'static_html/hsbc/savings-accounts.html',base_url + ext,logger)
	# foreach item in the doormatCol, in the ul, get each li's a element href attribute.
	doormatCols = bsobj.find_all(attrs={'class' : 'doormatCol'})
	for d in doormatCols:
		anchors = d.find_all('a')
		for a in anchors:
			href = a.get('href')
			if href and re.match('.*savings-accounts/.*',href):
				url = base_url + href
				savings_data = savings_util.get_savings_data_object()
				# Set online to and branch to default to Y for HSBC
				savings_data['online'] = 'Y'
				savings_data['branch'] = 'Y'
				#print savings_data
				get_product_page_interest_rates(url + '/interest-rates',savings_data)
				get_product_page_details(url + '/details',savings_data)

def get_product_page_details(url,savings_data):
	logger = logging.getLogger('retrieve')
	#logger.info(url)
	bsobj = themortgagemeter_utils.get_page(False,'',url,logger)
	#logger.info(bsobj)


def get_product_page_interest_rates(url,savings_data):
	logger = logging.getLogger('retrieve ' + url)
	bsobj = themortgagemeter_utils.get_page(False,'',url,logger)
	#logger.info(url) #logger.info(bsobj)
	if re.match('.*isa.*',url):
		savings_data['isa'] = 'Y'
	for t in bsobj.find_all('table'):
		#logger.info("TABLE")# logger.info(t)
		# Get all tables, then match on summary == "Interest rates:.*", and set up variables accordingly.
		summary = t.get('summary').encode('utf-8').lower()
		if summary:
			# Set up data for this page
			summary_info = re.match('.*interest rates: (.*)',summary).group(1)
			#logger.info("summary info: " + summary_info)
			if summary_info in ("cash e-isa#"):
				savings_data['isa'] = 'Y'
			elif summary_info in ("fixed rate saver - monthly interest"):
				savings_data['variability'] = 'F'
				savings_data['interest_paid'] = 'M'
			elif summary_info in ("fixed rate saver - annual interest"):
				savings_data['variability'] = 'F'
				savings_data['interest_paid'] = 'Y'
			elif "regular saver" in summary_info:
				savings_data['regular_saver'] = 'Y'
				savings_data['interest_paid'] = 'Y'
			elif "online bonus" in summary_info:
				savings_data['bonus']  = 'Y'
				savings_data['branch'] = 'N'
				savings_data['bonus_frequency_period'] = '1'
				savings_data['bonus_frequency_type']   = 'M'
				# skip bonus for HSBC- it's complicated - probably needs its own function TODO
				continue
			elif "flexible saver" in summary_info:
				savings_data['variability']     = 'V'
			else:
				themortgagemeter_utils.record_alert('NEED TO HANDLE: ' + summary_info,logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
				exit()
			tr_count = 0
			for tr in t.find_all('tr'):
				# This is a new savings product, so clone the data at this point and use that from here.
				this_savings_data = savings_data.copy()
				#logger.info("TR " + str(tr_count)) #logger.info(tr)
				if this_savings_data['bonus'] == 'Y':
					#print "BONUS"
					#print tr
					pass
				if this_savings_data['regular_saver'] == 'Y':
					td_count = -1
				else:
					td_count = 0
				if tr_count >= 1:
					# If tax-free, this will be true
					for td in tr.find_all('td'):
						td_style = td.get('style')
						if td_style != None:
							td_style = td_style.lower().encode('utf-8').translate(None, ' ')
							if td_style == 'vertical-align:middle':
								continue
						#logger.info("TD" + str(td_count)) #logger.info(tr_count) #logger.info(td_count)
						logger.info(td)
						v = td.text.encode('utf-8').lower().strip()
						if td_count == 0:
							#logger.info(this_savings_data['regular_saver'])
							if this_savings_data['regular_saver'] == 'Y':
								logger.info('regular_saver: ' + v)
								this_savings_data['regular_saver_min_amt'] = v.split()[0][2:]
								this_savings_data['regular_saver_max_amt'] = v.split()[2][2:]
								if v.split()[4] == "month":
									this_savings_data['regular_saver_frequency_period'] = '1'
									this_savings_data['regular_saver_frequency_type'] = 'M'
								else:
									themortgagemeter_utils.record_alert('ERROR: reg saver not parsed: ' + v,logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
									exit()
							else:
								# if it's got a + at the end, it's a min, if it's "up to" it's a max.
								res = savings_util.get_money_range(v,logger)
								this_savings_data['min_amt'] = res[0]
								this_savings_data['max_amt'] = res[1]
								# TODO: remove this section
								#if re.match('^.*\+$',v):
								#	money_val = themortgagemeter_utils.get_money(v,logger)
								#	this_savings_data['min_amt'] = money_val
								#elif re.match('^.*up to.*$',v) or re.match('^.*under.*$',v):
								#	money_val = themortgagemeter_utils.get_money(v,logger)
								#	this_savings_data['max_amt'] = money_val
								#	this_savings_data['min_amt'] = 0
								#elif re.match('^.* - .*$',v):
								#	this_savings_data['min_amt'] = v.split()[0][2:].translate(None,',')
								#	this_savings_data['max_amt'] = v.split()[2][2:].translate(None,',')
								#else:
								#	#logger.info(t) #logger.info('value not handled: ' + v)
								#	themortgagemeter_utils.record_alert('ERROR: value wrong: ' + v,logger,themortgagemeter_db.db_connection,themortgagemeter_db.cursor)
								#	exit()
						elif td_count == 1:
							# we don't bother with net_percent
							pass
						elif td_count == 2:
							# gross %
							this_savings_data['gross_percent'] = v
						elif td_count == 3:
							this_savings_data['aer_percent'] = v
						td_count += 1
					# Some trs have no tds; we ignore those.
					if td_count > 0:
						# Now store this product
						# TODO: fixed savings?
						logger.info(this_savings_data)
						isa = this_savings_data['isa']
						regular_saver = this_savings_data['regular_saver']
						regular_saver_frequency_period = this_savings_data['regular_saver_frequency_period']
						regular_saver_frequency_type = this_savings_data['regular_saver_frequency_type']
						regular_saver_min_amt = this_savings_data['regular_saver_min_amt']
						regular_saver_max_amt = this_savings_data['regular_saver_max_amt']
						bonus = this_savings_data['bonus']
						bonus_frequency_period = this_savings_data['bonus_frequency_period']
						bonus_frequency_type = this_savings_data['bonus_frequency_type']
						online = this_savings_data['online']
						branch = this_savings_data['branch']
						variability = this_savings_data['variability']
						min_amt = this_savings_data['min_amt']
						max_amt = this_savings_data['max_amt']
						gross_percent = this_savings_data['gross_percent']
						aer_percent = this_savings_data['aer_percent']
						interest_paid = this_savings_data['interest_paid']
						child = this_savings_data['child']
						savings_period = this_savings_data['savings_period']
						savings_util.handle_savings_insert(institution_code, isa, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, online, branch, variability, savings_period, min_amt, max_amt, gross_percent, aer_percent, child, interest_paid, url, logger)
				else:
					tr_count += 1
					continue
				tr_count += 1
		else:
			#print url
			#print bsobj
			exit()
	#print "returning"







def hsbc_main(static,forcedelete,logger):
	base_url = 'https://www.hsbc.co.uk'
	ext = '/1/2/savings-accounts'
	get_product_pages(static,base_url,ext)
	savings_db.update_savings_current(institution_code,main.today,forcedelete,logger)
