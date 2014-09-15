# vim: set fileencoding=utf-8
from bs4 import BeautifulSoup

import re
import logging
import string

import main
import savings_util
import savings_db
import mortgagecomparison_utils
import mortgagecomparison_db

institution_code = 'HLFX'
term = str(12 * 25)
def get_product_pages(static,base_url,ext_url,logger):
	url = base_url + ext_url
	urls_seen = []
	bsobj = mortgagecomparison_utils.get_page(static,'static_html/halifax/savings-accounts.html',url,logger)
	# let's see how much info we can extract from the page
	# Get all the sortable tables and divine as much info as possible from that.
	sortable_tables = doormatCols = bsobj.find_all(attrs={'class' : 'sortableTable'})
	for table in sortable_tables:
		#print table
		for tr in table.find_all('tr'):
			td_idx = 0
			savings_data = savings_util.get_savings_data_object()
			for td in tr.find_all('td'):
				td_text = td.text.encode('utf-8').strip().lower()
				if td_idx == 0:
					# title of account - Junior == child
					#re.match('/product/A[0-9]+.*',href)
					##0 ##<td style="text-align: left;"><a href="/savings/accounts/cash-isas/isa-saver-online/">ISA Saver Online</a></td>
					##1 ##<td style="text-align: left;"><strong class="apr">1.35%</strong> tax free/AER variable including 12 month fixed bonus of<strong> </strong>1.10%</td>
					##2 ##<td>£1</td>
					##3 ##<td>Variable</td>
					##4 ##<td>Unlimited</td>
					##5 ##<td style="text-align: center;"><img alt="Online" src="/common/images/icons/mousegrey.gif" title="Online"/></td>
					##6 ##<td><a href="/savings/accounts/cash-isas/isa-saver-online/"><img alt="Find out more" src="/common/images/Buttons/primary_find_out_more.gif"/></a></td>
					#print "0: " + td_text
					if re.match('^.*isa.*$',td_text):
						savings_data['isa'] = 'Y'
					if re.match('^.*junior.*$',td_text):
						savings_data['child'] = 'Y'
				elif td_idx == 1:
					#print "1: " + td_text
					# We don't bother with this at the moment - TODO - sort this out
					#if re.match('.*bonus.*',td_text):
					#	savings_data['bonus'] = 'Y'
					pass
				elif td_idx == 2:
					#print "2: " + td_text
					# minimum investment, max is always infinity
					min_amt = mortgagecomparison_utils.get_money(td_text,logger)
					savings_data['min_amt'] = min_amt
				elif td_idx == 3:
					#print "3: " + td_text
					# Variable/Fixed
					if re.match('.*variable.*',td_text):
						savings_data['variability'] = 'V'
					elif re.match('.*fixed.*',td_text):
						savings_data['variability'] = 'F'
					else:
						mortgagecomparison_utils.record_alert('ERROR: unknown variability: ' + td_text,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
						exit()
				elif td_idx == 4:
					#print "4: " + td_text
					# Let's assume we'll get this info from the sub-page.
					# Withdrawals allowed: "None, by closure only", "Unlimited", "None, until child is 18"
					pass
				elif td_idx == 5:
					#print "5: " + td_text
					for img in td.find_all('img'):
						title = img.get('title').lower().strip()
						if title == 'online':
							savings_data['online'] = 'Y'
						elif title == 'branch':
							savings_data['branch'] = 'Y'
							# I'm going to ignore "phone"
						elif title == 'phone':
							pass
				elif td_idx == 6:
					#print "6: " + td_text
					# more details link
					new_url = base_url + td.find_all('a')[0].get('href')
					if new_url in urls_seen:
						continue
					savings_array = process_more_info_page(savings_data,new_url,logger)
					print new_url
					for this_savings_data in savings_array:
						# insert savings here TODO.
						print this_savings_data
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
					urls_seen.insert(0,new_url)
				else:
					mortgagecomparison_utils.record_alert('ERROR: too many tds in tr: ' + tr,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
					exit()
				td_idx = td_idx + 1

def process_more_info_page(savings_data,url,logger):
	bsobj = mortgagecomparison_utils.get_page(False,'static_html/halifax/savings-accounts.html',url,logger)
	#print bsobj
	savings_array = []
	#print "Passed in:"
	#print savings_data
	print url
	if savings_data['isa'] == 'Y':
		for i1 in bsobj.find_all("h2",text="Summary box"):
			for i2 in i1.parent():
				if i2.find_all("table") != []:
					tabs = i2.find_all("table")
					if re.match(".*isa-saver-fixed.*",url):
						if len(tabs) != 2:
							mortgagecomparison_utils.record_alert('ERROR: too many tabs in isa',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
							exit()
						else:
							tabs.pop(0)
						for tab in tabs:
							tbody = tab.find_all("tbody")[0]
							trs = tbody.find_all("tr")
							for tr in trs:
								savings_data_tmp = savings_data.copy()
								tds = tr.find_all("td")
								savings_data_tmp['savings_period'] = mortgagecomparison_utils.get_months(tds[0].text.strip().encode('utf-8'),logger)
								savings_data_tmp['aer_percent'] = mortgagecomparison_utils.get_percentage(tds[1].text.strip().encode('utf-8'),logger)
								savings_data_tmp['gross_percent'] = savings_data_tmp['aer_percent']
								savings_array.append(savings_data_tmp)
					else:
						if len(tabs) > 1:
							#print tabs
							mortgagecomparison_utils.record_alert('ERROR: too many tabs in isa',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
							exit()
						for tab in tabs:
							#print tab
							for tr in tab.find_all("tr"):
								ths = tr.find_all("th")
								tds = tr.find_all("td")
								if len(ths) > 0 and len(tds) > 0:
									th = tr.find_all("th")[0]
									td = tr.find_all("td")[0]
									th_text = th.text.lower()
									td_text = td.text.lower()
									if re.match('interest rates.*',th_text):
										#print "IR:" + td_text
										pc = mortgagecomparison_utils.get_percentage(td_text,logger)
										savings_data_tmp = savings_data.copy()
										savings_data_tmp['gross_percent'] = pc
										savings_data_tmp['aer_percent'] = pc
										savings_array.append(savings_data_tmp)
								else:
									if len(ths) == 0 and len(tds) > 0:
										td1 = tds[0]
										td2 = tds[1]
										td1_text = td1.text.lower()
										td2_text = td2.text.lower()
										if re.match('interest rates.*',td1_text):
											pc = mortgagecomparison_utils.get_percentage(td2_text,logger)
											savings_data_tmp = savings_data.copy()
											savings_data_tmp['gross_percent'] = pc
											savings_data_tmp['aer_percent'] = pc
											savings_array.append(savings_data_tmp)
									else:
										mortgagecomparison_utils.record_alert('ERROR: unhandled case: ' + url,logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
										exit()
	elif re.match('.*fixed-online-saver.*',url) or re.match('.*tracker-bond.*',url) or re.match('.*fixed-saver.*',url):
		if re.match('.*fixed-online-saver.*',url) or re.match('.*fixed-saver.*',url):
			#print bsobj
			code = "FOS"
			i1s = bsobj.find_all("h3",text="Current Rates")
			if i1s== []:
				i1s = bsobj.find_all("h3",text="Current rates")
		elif re.match('.*tracker-bond.*',url):
			#print bsobj
			code = "TB"
			i1s = []
			res = bsobj.find_all("h4")
			for i in res:
				#print i.text
				if i.text == "Current rates and apply":
					i1s.append(i)
					break
		if i1s == []:
			mortgagecomparison_utils.record_alert('No items from expected h3/4 match!',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		for i1 in i1s:
			for i2 in i1.parent():
				tbodys = i2.find_all("tbody")
				# if this is tracker bond, discard the first table
				if len(tbodys) == 0:
					continue
				if code == "TB":
					ok = False
					for tbody in tbodys:
						for tr in tbody.find_all("tr"):
							tds = tr.find_all("td")
							if tds[0].text == "Term":
								ok = True
					if not ok:
						continue
				for tbody in tbodys:
					tr_count = -1
					table_savings_period = "unset"
					for tr in tbody.find_all("tr"):
						tr_count = tr_count + 1
						if code == "TB" and tr_count == 0:
							# skip the first row
							continue
						# clone the savings_data ready to write to
						savings_data_tmp = savings_data.copy()
						# First td is time only on first row for TB
						if code == "TB" and tr_count > 1:
							td_count = 1
						else:
							td_count = 0
						if code == "TB" and tr_count > 1:
							if table_savings_period == "unset":
								mortgagecomparison_utils.record_alert('ERROR: table_savings_period should not be unset',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
								exit()
							savings_data_tmp['savings_period'] = table_savings_period
						for td in tr.find_all("td"):
							# 0 - term
							# 1 - balance 
							# 2 - Gross
							# 3 - AER
							# 4 - NET (ignore)
							# Ignore remainder of cols
							text = td.text.lower().strip().encode('utf-8')
							if td_count == 0:
								# store this in a variable for use on next row if necessary
								table_savings_period = mortgagecomparison_utils.get_months(text,logger)
								savings_data_tmp['savings_period'] = table_savings_period
							elif td_count == 1:
								res = savings_util.get_money_range(text,logger)
								savings_data_tmp['min_amt'] = res[0]
								savings_data_tmp['max_amt'] = res[1]
							elif td_count == 2:
								savings_data_tmp['gross_percent'] = mortgagecomparison_utils.get_percentage(text,logger)
							elif td_count == 3:
								savings_data_tmp['aer_percent'] = mortgagecomparison_utils.get_percentage(text,logger)
								# and then break out
								break
							td_count = td_count + 1
						savings_array.append(savings_data_tmp)
	elif re.match('.*/online-saver/',url):
		# TODO: need to set this for other types
		savings_data['interest_paid'] = 'Y'
		#print bsobj
		# get the apr class element, as that contains the text we need
		apr = bsobj.find_all(attrs={'class':'apr'})[0].parent.parent.text.encode('utf-8')
		# split this line by \n
		apr = apr.split('\n')
		lines = []
		for l in apr:
			if re.match('.* or [0-9].*',l):
				for l2 in l.split(' or ',1):
					lines.append(l2)
			else:
				lines.append(l)
		while '' in lines:
			lines.remove('')
		for l in lines:
			# copy 
			savings_data_tmp = savings_data.copy()
			#print l
			# get percentage
			savings_data_tmp['gross_percent'] = mortgagecomparison_utils.get_percentage(l,logger)
			savings_data_tmp['aer_percent'] = savings_data_tmp['gross_percent']
			# get_money range
			res = savings_util.get_money_range(l,logger)
			savings_data_tmp['min_amt'] = res[0]
			savings_data_tmp['max_amt'] = res[1]
			# append to savings_array
			savings_array.append(savings_data_tmp)
	elif re.match('.*/regular-saver/',url):
		# TODO: need to set this for other types
		savings_data['interest_paid'] = 'Y'
		savings_data['regular_saver_frequency_period'] = '1'
		savings_data['regular_saver_frequency_type'] = 'M'
		savings_data['regular_saver'] = 'Y'
		# Always fixed
		savings_data['variability'] = 'F'
		#print bsobj
		# get the apr class element, as that contains the text we need
		apr = bsobj.find_all(attrs={'class':'apr'})[0].parent.parent.text.encode('utf-8')
		# split this line by \n
		apr = apr.split('\n')
		lines = []
		for l in apr:
			if re.match('.* or [0-9].*',l):
				for l2 in l.split(' or ',1):
					lines.append(l2)
			else:
				lines.append(l)
		while '' in lines:
			lines.remove('')
		for l in lines:
			# copy 
			savings_data_tmp = savings_data.copy()
			# get percentage
			savings_data_tmp['gross_percent'] = mortgagecomparison_utils.get_percentage(l,logger)
			if savings_data_tmp['gross_percent'] == '':
				# abandon ship!
				continue
			savings_data_tmp['aer_percent'] = savings_data_tmp['gross_percent']
			# Hard-code to 25-250 for now, this seems standard
			savings_data_tmp['regular_saver_min_amt'] = '25'
			savings_data_tmp['regular_saver_max_amt'] = '250'
			# append to savings_array
			savings_array.append(savings_data_tmp)
	elif re.match('.*/everyday-saver/',url):
		# This one's quite simple (I think)
		# TODO: need to set this for other types
		savings_data['interest_paid'] = 'Y'
		#print bsobj
		# get the apr class element, as that contains the text we need
		apr = bsobj.find_all(attrs={'class':'apr'})[0].parent.parent.text.encode('utf-8')
		#print apr
		# split this line by \n
		apr = apr.split('\n')
		lines = []
		for l in apr:
			if re.match('.*gross.*',l):
				lines.append(l)
		while '' in lines:
			lines.remove('')
		for l in lines:
			# copy 
			savings_data_tmp = savings_data.copy()
			#print l
			# get percentage
			savings_data_tmp['gross_percent'] = mortgagecomparison_utils.get_percentage(l,logger)
			savings_data_tmp['aer_percent'] = savings_data_tmp['gross_percent']
			# TODO: bonus_frequency_period set to 1, or get from data?
			# append to savings_array
			savings_array.append(savings_data_tmp)
	elif re.match('.*/branch-accounts/.*',url):
		return savings_array
	else:
		logger.info('unhandled:' + url)
		exit()
	if savings_array == []:
		mortgagecomparison_utils.record_alert('ERROR: returning nothing from a page',logger,mortgagecomparison_db.db_connection,mortgagecomparison_db.cursor)
		exit()
	# Return the savings_array
	logger.info('returning savings_array:' + str(savings_array))
	return savings_array
	

def set_savings_array(savings_array,n,v,logger):
	for savings in savings_array:
		savings[n] = v

def halifax_main(static,forcedelete,logger):
	get_product_pages(static,'http://www.halifax.co.uk/','savings/accounts/',logger)
	savings_db.update_savings_current(institution_code,main.today,forcedelete,logger)

## #OLD STUFF
					# Let's assume we'll get this data from the sub-page.
					## contains the %, tax status, and bonus info, isa status
					## MORE COMPLEX ONE TODO
					## <td style="text-align: left;">1.69% gross/<span class="apr">1.70%</span> AER variable on balances £500 - £49,999.<br/>1.79% gross/<strong>1.80%</strong> AER variable for £50,000+</td>
					## Continue this loop until there are no more "gross"es
					#savings_array_idx = len(savings_array) - 1
					#while True:
					#	td_text_idx = td_text.find('gross')
					#	if td_text_idx == -1:
					#		break
					#	# get the string up to the "gross" and grab the percent.
					#	td_text_pc = td_text[:td_text_idx]
					#	#print savings_array_idx
					#	savings_array[savings_array_idx]['gross_percent'] = mortgagecomparison_utils.get_percentage(td_text_pc,logger)
					#	# Get the remaining string.
					#	td_text = td_text[td_text_idx+5:]
					#	# Get the first aer from the remaining string, get string up to that point.
					#	# If aer doesn't exist, then set it to the same as gross_percent
					#	# If aer does exist, but no percent, do same
					#	# then get string up to lowest of next gross... TODO
					#	# Add item to savings array
					#	savings_array.append(savings_array[savings_array_idx].copy())
					#	savings_array_idx = savings_array_idx + 1
					## We assume at this point that there's only one item in the savings_array.
					#if savings_array[savings_array_idx]['gross_percent'] == -1:
					#	gross_percent = mortgagecomparison_utils.get_percentage(td_text,logger)
					#	set_savings_array(savings_array,'gross_percent',gross_percent,logger)
					## If there are any percents left, then and no gross percent exists, look for a percent.
					## If gross percent doesn't exist, 
