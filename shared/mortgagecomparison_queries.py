# changes - ie deletions replaced by creations with the same: 
# insitution_code, mortgage_type, ltv, initial_period and eligibility
# should reveal changes in apr or rate
# 
# First select gets us all deleted rows where there is a mortgage record 
# with the same creation date as the deleted date and "same" details as above
# _and_ has not itself been deleted.
# 
# Then union that with rows with no delete date where there exists a
# row with non-null delete dates that are identical with the same information.
#
# Order it by the change date, key information, then last_retrieved date, then booking_fee (the least significant attribute).
#
# TODO: same row, but include later replacements. That would mean 
# checking that there exists no "same" mortgage record with a date 
# earlier than the one returned and later than the deleted date.
# 
# Must include the primary key for django.
replacement_mortgages = """
select change_date, institution_code, mortgage_type, eligibility, ltv, initial_period, booking_fee, cr_date, delete_date, rate, svr, apr, last_retrieved, mortgage_id, institution_name, url, action_type
from replacement_mortgages_materialized_view
order by 1 desc, 2, 3, 4, 5, 6, 13, 10, 7
limit 200
"""

replacement_savings = """
select change_date, institution_code, variability, isa, child, online, branch, interest_paid, regular_saver, regular_saver_frequency_period, regular_saver_frequency_type, regular_saver_min_amt, regular_saver_max_amt, bonus, bonus_frequency_period, bonus_frequency_type, savings_period, min_amt, max_amt, gross_percent, aer_percent, last_retrieved, institution_name, url, savings_id, action_type, cr_date
from replacement_savings_materialized_view
order by 1 desc, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,22,20
limit 200
"""

# The "best" extant mortgages

# The "best" extant mortgages
best_mortgages = """
select
	m1.mortgage_id,
	m1.institution_code,
	m1.mortgage_type,
	m1.rate,
	m1.svr,
	m1.apr,
	m1.ltv,
	m1.initial_period,
	m1.booking_fee,
	m1.term,
	m1.eligibility,
	j1.cr_date,
	t1.institution_name,
	j1.delete_date,
	u1.url,
	j1.cr_date as change_date
from
	tmortgage m1,
	tmortgagejrnl j1,
	tinstitution t1,
	turl u1
where
	m1.mortgage_id = j1.mortgage_id
and u1.url_id = j1.url_id
and t1.institution_code = m1.institution_code
and j1.delete_date is null
and mortgage_type %s
and eligibility %s
and t1.institution_code %s
and ltv %s
and m1.initial_period %s
order by %s
limit %s
"""


avgs = """
select
	avg(rate) as avg_rate,
	stddev(rate) as stddev_rate,
	count(1) as num_mortgages,
	d1.day as day
from
	tmortgage m1,
	tmortgagejrnl j1,
	tretrievaldates d1
where
	m1.mortgage_id = j1.mortgage_id and
	j1.cr_date <= d1.day and 
	(j1.delete_date is null or j1.delete_date > day) 
	and m1.eligibility like %s
    and m1.mortgage_type = %s
    and m1.ltv = %s
    and m1.initial_period = %s
	group by 4
	order by 4
"""

get_institution = """
select institution_name
from institution
where institution_code = %
"""

insert_alert = """
insert into talert (alert) values (%s)
"""
