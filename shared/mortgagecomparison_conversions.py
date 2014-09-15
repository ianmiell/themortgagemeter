# This file is both a reference and contains helper functions for converting codes in the system
# that are not stored in the database.

# TODO: get these from db as well as insitutions (see views.py in mortgagecomparisonapp)

# mortgage_types
mortgage_types = {'F':'Fixed', 'O':'Offset', 'B':'Buy-To-Let', 'D':'Discount', 'T':'Tracker', 'V':'Variable'}
def get_mortgage_type_str(mortgage_type):
	return mortgage_types.get(mortgage_type)

# intiial_periods
initial_periods = {'12':'1 Year', '24':'2 Years', '36':'3 Years', '48':'4 years', '60':'5 Years', '72':'6 Years', '84':'7 Years', '96':'8 Years', '108':'9 Years', '120':'10 Years'}

# eligibility
#    -- NFTB (new customer first time buyer)
#    -- NMH (new customer moving home)
#    -- NRM (new customer remortgage)
#    -- ERM (existing customer remortgage/deal ended)
#    -- EMH (existing customer moving)
#    -- EBM (existing customer borrowing more)
#    -- EED (existing customer ending deal early/switching)
eligibility_types = {'NFTB':'First-Time Buyer','NMH':'Moving Home (New Customer)', 'NRM':'Remortgage (New Customer)', 'ERM':'Remortgage (Existing Customer)', 'EMH':'Moving Home (Existing Customer)', 'EBM':'Borrowing More (Existing Customer)', 'EED':'Switch Deal', 'EDE':'Deal Ending (Existing Customer)'}
def get_eligibilty_str(eligibility):
	return eligibility_types(eligibility)



# Function to allow dictionaries to be added to the conversions (eg from db queries, not static data).
# We don't want this to be tied to the db access method directly.
def add_dict(name,**kargs):
	global conversions
	# list for 3.0
	if not name in list(conversions.keys()):
		conversions.update({name : kargs})
		update_conversions()

# Update conversions for json object
def update_conversions():
	global conversions_display
	c = {}
	# list for 3.0
	for item in list(conversions.keys()):
		l = []
		# list for 3.0
		for key in list(conversions[item].keys()):
			d = {}
			d.update({'code' : key})
			d.update({'value' : conversions[item][key]})
			# Need to create a shallow copy.
			l.append(d.copy())
		l.sort()
		# Add to the dictionary
		c.update({item : l})
	# set this to replace the global one, wrapped in a list for angularjs JSON purposes.
	conversions_display = [c]
	
conversions = {'mortgage_type' : mortgage_types, 'eligibility' : eligibility_types, 'initial_period' : initial_periods}
# Conversions object for website display.
conversions_display = None
update_conversions()
