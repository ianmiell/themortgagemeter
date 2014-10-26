#set fileencoding=utf-8
from django.http import HttpResponse
from themortgagemeterapp.models import Turl, Tmortgage, Tmortgagejrnl, Tinstitution, Tmailsubscriber, Tsavings
import json
# Caching
from django.core.cache import cache
from django.views.decorators.cache import cache_page, cache_control
import themortgagemeter_queries
import themortgagemeter_conversions
import logging
import datetime
import string
import time
	

def api(request):
	r = file('/opt/themortgagemeter/website/django/themortgagemeter/themortgagemeterapp/urls.py').read()
	return HttpResponse(r)

# Clear the cache
def clear_cache(request):
	#cache = get_cache('default')
	cache.clear()
	r = time.localtime()
	return HttpResponse(r)

# other graphs - SVR
@cache_page(60 * 30) # Caching
@cache_control(must_revalidate=True, no_cache=True)
def graphs(request):
	# Get the average results back:
	logger = logging.getLogger('file_logger')
	logger.critical("Building graphs")
	from django.db import connection, transaction
	cursor = connection.cursor()
	json_result = {}
	options_base = {"options":{"xaxis":{"mode":"time"},"lines":{"show":"true"},"legend":{"noColumns":100}}}
	args = [{"name":"fixed_rate_data","qry_args":[('%','F',6000,24,'2YR Fix 60% LTV'),('%','F',6000,60,'5YR Fix 60% LTV'),('%','F',7000,60,'5YR Fix 70% LTV'),('%','F',7000,24,'2YR Fix 70% LTV'),('%','F',7500,60,'5YR Fix 75% LTV'),('%','F',7500,24,'2YR Fix 75% LTV'),('%','F',8000,24,'2YR Fix 80% LTV'),('%','F',8000,60,'5YR Fix 80% LTV'),('%','F',9000,24,'2YR Fix 90% LTV'),('%','F',9000,60,'5YR Fix 90% LTV'),('%','F',9500,24,'2YR Fix 95% LTV'),('%','F',9500,60,'5YR Fix 95% LTV')]}]
	args.append({"name":"svr_data","qry_args":[('%','T',6000,300,'SVR 60% LTV'),('%','T',7000,300,'SVR 70% LTV'),('%','T',7500,300,'SVR 75% LTV'),('%','T',8000,300,'SVR 80% LTV'),('%','T',9000,300,'SVR 90% LTV'),('%','T',9500,300,'SVR 95% LTV')]})
	args.append({"name":"ftb_fixed_rate_data","qry_args":[('NFTB','F',6000,24,'2YR Fix 60% LTV'),('NFTB','F',6000,60,'5YR Fix 60% LTV'),('NFTB','F',7000,60,'5YR Fix 70% LTV'),('NFTB','F',7000,24,'2YR Fix 70% LTV'),('NFTB','F',7500,60,'5YR Fix 75% LTV'),('NFTB','F',7500,24,'2YR Fix 75% LTV'),('NFTB','F',8000,24,'2YR Fix 80% LTV'),('NFTB','F',8000,60,'5YR Fix 80% LTV'),('NFTB','F',9000,24,'2YR Fix 90% LTV'),('NFTB','F',9000,60,'5YR Fix 90% LTV'),('NFTB','F',9500,24,'2YR Fix 95% LTV'),('NFTB','F',9500,60,'5YR Fix 95% LTV')]})
	args.append({"name":"discount_rate_data","qry_args":[('%','T',6000,24,'2YR 60% LTV'),('%','T',7000,24,'2YR 70% LTV'),('%','T',7500,24,'2YR 75% LTV'),('%','T',8000,24,'2YR 80% LTV'),('%','T',9000,24,'2YR 90% LTV'),('%','T',9500,24,'2YR 95% LTV'),('%','T',6000,60,'5YR 60% LTV'),('%','T',7000,60,'5YR 70% LTV'),('%','T',7500,60,'5YR 75% LTV'),('%','T',8000,60,'5YR 80% LTV'),('%','T',9000,60,'5YR 90% LTV'),('%','T',9500,60,'5YR 95% LTV')]})
	for d in args:
		this_json_result = {}
		this_num_series = 0
		arg_arr = d["qry_args"]
		json_name = d["name"]
		for (eligibility,mortgage_type,ltv,initial_period,label) in arg_arr:
			cursor.execute(themortgagemeter_queries.avgs, (eligibility,mortgage_type,ltv,initial_period))
			dat = []
			options = options_base.copy()
			for row in cursor.fetchall():
				(avg_rate,stddev,num_mortgages,day) = row
				day_ms = time.mktime(datetime.date.timetuple(day)) * 1000
				dat.append([day_ms,float(avg_rate)/100])
			this_json_result.update({this_num_series:{"data":dat,"label":label}})
			this_num_series += 1
		this_json_result.update({"num_series":this_num_series})
		options.update({"legend":{"noColumns":this_num_series}})
		this_json_result.update(options)
		# Collate json_result
		json_result.update({json_name:this_json_result})
	response = json.JSONEncoder().encode(json_result)
	return HttpResponse(response)

# Subscribe for mortgage updates.
def subscribe_email(request,email):
	logger = logging.getLogger('file_logger')
	logger.critical('subscribe_email')
	response = ''
	logger.critical(email)
	#logger.critical(Tmailsubscriber.objects.filter(email_address=email))
	if Tmailsubscriber.objects.filter(email_address=email):
		logger.critical('here1')
		logger.critical('already there' + email)
		response = 'Thanks, we already have your email address!'
	else:
		try:
			e1 = Tmailsubscriber(email_address=email)
			logger.critical('saving')
			e1.save()
			logger.critical('saved')
			response = 'Thanks!'
		except Exception as e:
			logger.critical(e)
	display = {'result':response}
	json_display = json.JSONEncoder().encode(display)
	return HttpResponse(json_display)

# Get 
# request - django request object
# num_results - number of results to return - capped to 10
# mortgage_type - must be in valid list
@cache_page(60 * 30) # Caching
@cache_control(must_revalidate=True, no_cache=True)
def best_mortgages(request,num_results,mortgage_type,eligibility,institution_code,ltv,initial_period):
	logger = logging.getLogger('file_logger')
	# num_results - number of results to return - capped to 30
	if num_results == '0' or int(num_results) > 30:
		num_results = '30'
	if mortgage_type in themortgagemeter_conversions.mortgage_types.keys():
		mortgage_type_arg = ' = \'' + mortgage_type + '\''
	else:
		mortgage_type_arg = ' like \'%%\' '
	if eligibility in themortgagemeter_conversions.eligibility_types.keys():
		eligibility_arg = ' = \'' + eligibility + '\''
	else:
		eligibility_arg = 'like \'%%\''
	if institution_code != 'X':
		institutions = get_institutions()
		if institution_code in institutions.keys():
			institution_code_arg = ' = \'' + institution_code + '\''
		else:
			institution_code_arg = 'like \'%%\''
	else:
		institution_code_arg = 'like \'%%\''
	if ltv == '9000':
		ltv_arg = ">= 9000"
	elif ltv == '8000':
		ltv_arg = ">= 8000"
	elif ltv == '7000':
		ltv_arg = ">= 7000"
	elif ltv == '6000':
		ltv_arg = ">= 6000"
	else:
		ltv_arg = '> 0'
	if int(initial_period) == 0:
		initial_period_arg = '>= 0'
	else:
		initial_period_arg = '= ' + initial_period
	order_by_arg = 'm1.rate asc, m1.apr asc, m1.svr asc, m1.ltv asc, m1.initial_period asc, m1.booking_fee asc'
	#logger.debug(themortgagemeter_queries.best_mortgages % (mortgage_type_arg, eligibility_arg, institution_code_arg, ltv_arg, order_by_arg, num_results))
	best_mortgages = Tmortgage.objects.raw(themortgagemeter_queries.best_mortgages % (mortgage_type_arg, eligibility_arg, institution_code_arg, ltv_arg, initial_period_arg, order_by_arg, num_results))
	display = []
	for tmortgage in best_mortgages:
		display.append(get_mortgage_ds(tmortgage))
	json_display = json.JSONEncoder().encode(display)
	return HttpResponse(json_display)

@cache_page(60 * 15) # Caching
@cache_control(must_revalidate=True, no_cache=True)
def get_conversions(request):
	logger = logging.getLogger('file_logger')
	institutions = get_institutions()
	themortgagemeter_conversions.add_dict('institution',**institutions)
	themortgagemeter_conversions.update_conversions()
	json_display = json.JSONEncoder().encode(themortgagemeter_conversions.conversions_display)
	return HttpResponse(json_display)

# Get active mortgage institutions
def get_institutions():
	institutions_rs = Tinstitution.objects.all()
	institutions = {}
	for institution in institutions_rs:
		if institution.mortgage_status == 'A':
			institutions.update({institution.institution_code:institution.institution_name})
	return institutions
	

# Collect the latest changes.
@cache_page(60 * 15) # Caching
@cache_control(must_revalidate=True, no_cache=True)
def latest_n_changes(request,num_changes):
	logger = logging.getLogger('file_logger')
	#logger.critical('Received latest_n_changes request')
	if num_changes == '0' or int(num_changes) > 50:
		num_changes = 50
	num_changes = int(num_changes)
	# It seems not to matter whether you have Tmortgage or Tmortgagejrnl below
	replacement_mortgages_qry_key = 'latest_changes_qry'
	replacement_mortgages_qry_cache_time = (60 * 15)
	# Not sure how useful all this cacheing is..
	if cache.get(replacement_mortgages_qry_key) == None:
		logger.critical('Running latest_n_changes query')
		latest_changes = Tmortgage.objects.raw(themortgagemeter_queries.replacement_mortgages)
		cache.set(replacement_mortgages_qry_key,latest_changes,replacement_mortgages_qry_cache_time)
	else:
		logger.critical('Retrieved latest_n_changes query from cache')
		latest_changes = cache.get(replacement_mortgages_qry_key)
	# Mortgages being replaced
	old_mortgages = []
	# New mortgages
	new_mortgages = []
	# Set of changes count
	changes_index = 0
	# Diffs dict
	diffs_dict = {}
	# List containing data for display
	display = []
	for tmortgage in latest_changes:
		action_type = tmortgage.action_type
		# For each row in here, if delete_date is not null, we have a new set.
		# The not null row is the "deleted mortgage", and the next rows until next not null are "replacement mortgages"
		#logger.debug(str(tmortgage) + " " + str(action_type))
		if action_type in ("DELETED","ADDED","REPLACED"):
			# If there are any new mortgages "left" then we just hit the end of a change set.
			if new_mortgages != []:
				# sort out previous set for display
				# Get the differences between the items
				diffs_dict = get_ds_diffs(old_mortgages,new_mortgages)
				display.append(diffs_dict)
				# re-set up initial state.
				new_mortgages  = []
				old_mortgages  = []
				diffs_dict     = []
				changes_index  += 1
				# If we've gone through n changes, break out.
				if changes_index >= num_changes and tmortgage.change_date < datetime.date.today() - datetime.timedelta(1):
					#logger.critical('Dropping out on index' + str(changes_index))
					break
		if action_type == "DELETED":
			old_mortgages.append(get_mortgage_ds(tmortgage))
			display.append({'old_mortgage' : old_mortgages})
			# re-set
			old_mortgages = []
			changes_index += 1
		elif action_type == "ADDED":
			# add new mortgage
			new_mortgages.append(get_mortgage_ds(tmortgage))
			display.append({'new_mortgage' : new_mortgages})
			# re-set
			new_mortgages = []
			changes_index += 1
		elif action_type == 'REPLACED':
			old_mortgages.append(get_mortgage_ds(tmortgage))
		elif action_type == 'REPLACING':
			new_mortgages.append(get_mortgage_ds(tmortgage))
		else:
			logger.critical('THERE WAS A PROBLEM, EXPECTING action_type in (DELETED, ADDED, REPLACING, REPLACED)')
			continue
	#logger.critical('Processed RS')
	json_display = json.JSONEncoder().encode(display)
	return HttpResponse(json_display)


@cache_page(60 * 15) # Caching
@cache_control(must_revalidate=True, no_cache=True)
def latest_n_changes_savings(request,num_changes):
	logger = logging.getLogger('file_logger')
	#logger.critical('Received latest_n_changes request')
	if num_changes == '0' or int(num_changes) > 50:
		num_changes = 50
	num_changes = int(num_changes)
	replacement_savings_qry_key = 'latest_changes_savings_qry'
	replacement_savings_qry_cache_time = (60 * 15)
	# Not sure how useful all this cacheing is..
	if cache.get(replacement_savings_qry_key) == None:
		logger.critical('Running latest_n_changes_savings query')
		latest_changes = Tsavings.objects.raw(themortgagemeter_queries.replacement_savings)
		cache.set(replacement_savings_qry_key,latest_changes,replacement_savings_qry_cache_time)
	else:
		logger.critical('Retrieved latest_n_changes_savings query from cache')
		latest_changes = cache.get(replacement_savings_qry_key)
	# Savings being replaced
	old_savings = []
	# New savings
	new_savings = []
	# Set of changes count
	changes_index = 0
	# Diffs dict
	diffs_dict = {}
	# List containing data for display
	display = []
	for tsavings in latest_changes:
		logger.critical("New iteration")
		logger.critical(display)
		action_type = tsavings.action_type
		# For each row in here, if delete_date is not null, we have a new set.
		# The not null row is the "deleted savings", and the next rows until next not null are "replacement savings"
		logger.debug(str(tsavings) + " " + str(action_type))
		if action_type in ("DELETED","ADDED","REPLACED"):
			# If there are any new savings "left" then we just hit the end of a change set.
			if new_savings != []:
				# sort out previous set for display
				# Get the differences between the items
				diffs_dict = get_ds_diffs(old_savings,new_savings)
				display.append(diffs_dict)
				# re-set up initial state.
				new_savings  = []
				old_savings  = []
				diffs_dict     = []
				changes_index  += 1
				# If we've gone through n changes, break out.
				if changes_index >= num_changes and tsavings.change_date < datetime.date.today() - datetime.timedelta(1):
					#logger.critical('Dropping out on index' + str(changes_index))
					break
		if action_type == "DELETED":
			old_savings.append(get_savings_ds(tsavings))
			display.append({'old_savings' : old_savings})
			#logger.critical("old savings appended")
			#logger.critical(display)
			# re-set
			old_savings = []
			changes_index += 1
		elif action_type == "ADDED":
			# add new savings
			new_savings.append(get_savings_ds(tsavings))
			display.append({'new_savings' : new_savings})
			# re-set
			new_savings = []
			changes_index += 1
		elif action_type == 'REPLACED':
			old_savings.append(get_savings_ds(tsavings))
		elif action_type == 'REPLACING':
			new_savings.append(get_savings_ds(tsavings))
		else:
			logger.critical('THERE WAS A PROBLEM, EXPECTING action_type in (DELETED, ADDED, REPLACING, REPLACED)')
			continue
	#logger.critical('Processed RS')
	#logger.critical(display)
	json_display = json.JSONEncoder().encode(display)
	return HttpResponse(json_display)


# Standardised return of a mortgage data structure.
def get_mortgage_ds(tmortgage):
	#logger = logging.getLogger('file_logger')
	#logger.critical(tmortgage)
	# change_date is actually marked in the query as delete_date.
	# Format of date: datetime.date.strftime(d,'%m')
	change_date = str(tmortgage.change_date)
	change_date_display = string.strip(datetime.date.strftime(tmortgage.change_date,'%e %b'))
	if tmortgage.initial_period % 12 == 0:
		initial_period_display = str(tmortgage.initial_period / 12) + ' years'
	else:
		initial_period_display = str(tmortgage.initial_period) +' months'
	return {'mortgage_id':tmortgage.mortgage_id,'institution_code':tmortgage.institution_code,'institution_name':tmortgage.institution_name,'mortgage_type':tmortgage.mortgage_type,'mortgage_type_display':themortgagemeter_conversions.mortgage_types.get(tmortgage.mortgage_type),'rate':tmortgage.rate,'rate_display':str(int(tmortgage.rate)/100.00)+'%','svr':tmortgage.svr,'svr_display':str(int(tmortgage.svr)/100.00)+'%','apr':tmortgage.apr,'apr_display':str(int(tmortgage.apr)/100.00)+'%','ltv':tmortgage.ltv,'ltv_display':str(int(tmortgage.ltv)/100.00)+'%','initial_period':tmortgage.initial_period,'initial_period_display':initial_period_display,'booking_fee':tmortgage.booking_fee,'booking_fee_display':'\xc2\xa3'+str(tmortgage.booking_fee),'term':tmortgage.term,'eligibility':tmortgage.eligibility,'eligibility_display':themortgagemeter_conversions.eligibility_types.get(tmortgage.eligibility),'cr_date':str(tmortgage.cr_date),'change_date':change_date,'change_date_display':change_date_display,'url':tmortgage.url}


# diffs between dicts, eg for mortgage dicts:
#       {'apr_display':{'replacing':['2.45','2.5'],'replaced':['3.0']},'insitution_code':{'shared':'HSBC'}}
# ready for displaying by javascript front end.
#
# format is: {key:{'type',[values]}+}} where type is replacing and replaced, or just shared
#
# a[0] must exist, else an empty dict is returned!
def get_ds_diffs(a,b):
	diff_dict = {}
	if len(a) < 1 or len(b) < 1:
		return diff_dict
	for key in a[0].keys():
		new_list = []
		for m in b:
			if m.get(key) not in new_list:
				new_list.append(m.get(key))
		old_list = []
		for m in a:
			if m.get(key) not in old_list:
				old_list.append(m.get(key))
		if old_list != new_list:
			diff_dict.update({key:{'new':new_list[:],'old':old_list[:]}})
		else:
			diff_dict.update({key:{'shared':[m.get(key)]}})
	return diff_dict


## SAVINGS
# Standardised return of a savings data structure.
def get_savings_ds(tsavings):
	logger = logging.getLogger('file_logger')
	logger.critical(tsavings)
	# change_date is actually marked in the query as delete_date.
	# Format of date: datetime.date.strftime(d,'%m')
	change_date = str(tsavings.change_date)
	change_date_display = string.strip(datetime.date.strftime(tsavings.change_date,'%e %b'))
# UP TO HERE!
	if tsavings.regular_saver_frequency_period % 12 == 0:
		regular_saver_frequency_period_display = str(tsavings.regular_saver_frequency_period / 12) + ' years'
	else:
		regular_saver_frequency_period_display = str(tsavings.regular_saver_frequency_period) + ' months'
	if tsavings.bonus_frequency_period % 12 == 0:
		bonus_frequency_period_display = str(tsavings.bonus_frequency_period / 12) + ' years'
	else:
		bonus_frequency_period_display = str(tsavings.bonus_frequency_period) + ' months'
	if tsavings.savings_period % 12 == 0:
		savings_period_display = str(tsavings.savings_period / 12) + ' years'
	else:
		savings_period_display = str(tsavings.savings_period) + ' months'
	# TODO: display items as below
	# TO DISPLAY: regular_saver_frequency_period, bonus_frequency_period, savings_period,change_date et al
	#return {'mortgage_type_display':themortgagemeter_conversions.mortgage_types.get(tmortgage.mortgage_type),rate_display':str(int(tmortgage.rate)/100.00)+'%','svr_display':str(int(tmortgage.svr)/100.00)+'%','apr_display':str(int(tmortgage.apr)/100.00)+'%','ltv_display':str(int(tmortgage.ltv)/100.00)+'%','initial_period_display':initial_period_display,'booking_fee_display':'\xc2\xa3'+str(tmortgage.booking_fee),'eligibility_display':themortgagemeter_conversions.eligibility_types.get(tmortgage.eligibility),'change_date_display':change_date_display,'url':tmortgage.url}
	return {'savings_id':tsavings.savings_id,'institution_code':tsavings.institution_code,'institution_name':tsavings.institution_name,'variability':tsavings.variability,'isa':tsavings.isa,'child':tsavings.child,'online':tsavings.online,'branch':tsavings.branch,'interest_paid':tsavings.interest_paid,'regular_saver':tsavings.regular_saver,'regular_saver_frequency_period':tsavings.regular_saver_frequency_period,'regular_saver_frequency_type':tsavings.regular_saver_frequency_type,'regular_saver_min_amt':tsavings.regular_saver_min_amt,'regular_saver_max_amt':tsavings.regular_saver_max_amt,'bonus':tsavings.bonus,'bonus_frequency_period':tsavings.bonus_frequency_period,'bonus_frequency_type':tsavings.bonus_frequency_type,'savings_period':tsavings.savings_period,'min_amt':tsavings.min_amt,'max_amt':tsavings.max_amt,'gross_percent':tsavings.gross_percent,'aer_percent':tsavings.aer_percent,'cr_date':str(tsavings.cr_date),'change_date':change_date,'url':tsavings.url}


