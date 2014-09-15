-- EXAMPLE from mortgage
--SELECT j1.delete_date AS change_date,
--m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, 'REPLACED'::text AS action_type 
--FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 
--WHERE (((((m1.mortgage_id = j1.mortgage_id) AND (j1.url_id = u1.url_id)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (j1.delete_date IS NOT NULL)) AND 
--	(EXISTS 
--		(SELECT 1 
--				FROM tmortgage m2, tmortgagejrnl j2 
--				WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j1.delete_date = j2.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) 
--					AND (j2.delete_date IS NULL))
--		)
--	)
--) 
--UNION
--
--SELECT
--j1.cr_date AS change_date, 
--m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, 'REPLACING'::text AS action_type 
--FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 
--WHERE (((((m1.mortgage_id = j1.mortgage_id) AND (j1.url_id = u1.url_id)) AND (j1.delete_date IS NULL)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (
--	EXISTS (
--		SELECT 1
--			FROM tmortgagejrnl j2, tmortgage m2
--			WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j2.delete_date = j1.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) 
--				AND (j2.delete_date IS NOT NULL)))))) 
--UNION
--
--SELECT CASE WHEN (j1.delete_date IS NULL) THEN j1.cr_date WHEN (j1.delete_date IS NOT NULL) THEN j1.delete_date ELSE NULL::date END AS change_date, m1.institution_code, m1.mortgage_type, m1.eligibility, m1.ltv, m1.initial_period, m1.booking_fee, j1.cr_date, j1.delete_date, m1.rate, m1.svr, m1.apr, j1.last_retrieved, m1.mortgage_id, t1.institution_name, u1.url, 
--CASE WHEN (j1.delete_date IS NULL) THEN 'ADDED'::text WHEN (j1.delete_date IS NOT NULL) THEN 'DELETED'::text ELSE NULL::text END AS action_type 
--FROM tmortgage m1, tmortgagejrnl j1, tinstitution t1, turl u1 
--WHERE ((((m1.mortgage_id = j1.mortgage_id) AND (u1.url_id = j1.url_id)) AND ((t1.institution_code)::text = (m1.institution_code)::text)) AND (NOT (m1.mortgage_id IN (SELECT m1.mortgage_id FROM tmortgage m1, tmortgagejrnl j1 WHERE (((m1.mortgage_id = j1.mortgage_id) AND (j1.delete_date IS NOT NULL)) AND (EXISTS (SELECT 1 FROM tmortgage m2, tmortgagejrnl j2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j1.delete_date = j2.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) 
--AND (j2.delete_date IS NULL))))) UNION SELECT m1.mortgage_id FROM tmortgage m1, tmortgagejrnl j1 WHERE (((m1.mortgage_id = j1.mortgage_id) AND (j1.delete_date IS NULL)) AND 
--(EXISTS (SELECT 1 FROM tmortgagejrnl j2, tmortgage m2 WHERE (((((((((m2.mortgage_id = j2.mortgage_id) AND (j2.delete_date = j1.cr_date)) AND ((m2.institution_code)::text = (m1.institution_code)::text)) AND (m2.mortgage_type = m1.mortgage_type)) AND ((m2.eligibility)::text = (m1.eligibility)::text)) AND (m2.ltv = m1.ltv)) AND (m2.initial_period = m1.initial_period)) AND (m2.svr = m1.svr)) AND (j2.delete_date IS NOT NULL)))))))))
--ORDER BY 1 DESC, 2, 3, 4, 5, 6, 13, 10, 7;
---- 13 - last_retrieved
---- 10 - rate
---- 7 - booking fee





-- SAVINGS QUERY IN PROGRESS
DROP VIEW replacement_savings_view;
CREATE VIEW replacement_savings_view AS
(
SELECT
	j1.delete_date AS change_date,
	s1.institution_code,
	s1.variability,
	s1.isa,
	s1.child,
	s1.online,
	s1.branch,
	s1.interest_paid,
	s1.regular_saver,
	s1.regular_saver_frequency_period,
	s1.regular_saver_frequency_type,
	s1.regular_saver_min_amt,
	s1.regular_saver_max_amt,
	s1.bonus,
	s1.bonus_frequency_period,
	s1.bonus_frequency_type,
	s1.savings_period,
	s1.min_amt,
	s1.max_amt,
	s1.gross_percent,
	s1.aer_percent,
	j1.last_retrieved,
	t1.institution_name,
	u1.url,
	s1.savings_id,
	j1.cr_date,
	'REPLACED'::text AS action_type
FROM tsavings s1, tsavingsjrnl j1, tinstitution t1, turl u1
WHERE s1.savings_id = j1.savings_id AND s1.institution_code = t1.institution_code AND j1.delete_date IS NOT NULL AND u1.url_id = j1.url_id AND (
	EXISTS (
		SELECT 1 
			FROM tsavings s2, tsavingsjrnl j2 
			WHERE ((((s2.savings_id = j2.savings_id) AND (j1.delete_date = j2.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND s2.variability = s1.variability AND s1.isa = s2.isa AND s1.child = s2.child AND s1.regular_saver = s2.regular_saver AND s1.regular_saver_frequency_period = s2.regular_saver_frequency_period AND s1.regular_saver_frequency_type = s2.regular_saver_frequency_type AND s1.regular_saver_min_amt = s2.regular_saver_min_amt AND s1.regular_saver_max_amt = s2.regular_saver_max_amt AND s1.bonus = s2.bonus AND s1.bonus_frequency_period = s2.bonus_frequency_period AND s1.bonus_frequency_type = s2.bonus_frequency_type AND s1.savings_period = s2.savings_period AND s1.min_amt = s2.min_amt AND s1.max_amt = s2.max_amt AND s1.interest_paid = s2.interest_paid 
				AND j2.delete_date IS NULL)
	)
)
UNION
SELECT
	j1.cr_date AS change_date,
	s1.institution_code,
	s1.variability,
	s1.isa,
	s1.child,
	s1.online,
	s1.branch,
	s1.interest_paid,
	s1.regular_saver,
	s1.regular_saver_frequency_period,
	s1.regular_saver_frequency_type,
	s1.regular_saver_min_amt,
	s1.regular_saver_max_amt,
	s1.bonus,
	s1.bonus_frequency_period,
	s1.bonus_frequency_type,
	s1.savings_period,
	s1.min_amt,
	s1.max_amt,
	s1.gross_percent,
	s1.aer_percent,
	j1.last_retrieved,
	t1.institution_name,
	u1.url,
	s1.savings_id,
	j1.cr_date,
	'REPLACING'::text AS action_type
FROM
	tsavings s1,
	tsavingsjrnl j1,
	tinstitution t1,
	turl u1
WHERE s1.savings_id = j1.savings_id AND s1.institution_code = t1.institution_code AND j1.delete_date IS NULL AND u1.url_id = j1.url_id AND (
	EXISTS (
			SELECT 1 
				FROM tsavings s2, tsavingsjrnl j2 
				WHERE ((((s2.savings_id = j2.savings_id) AND (j2.delete_date = j1.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) 
AND s2.variability = s1.variability AND s1.isa = s2.isa AND s1.child = s2.child AND s1.regular_saver = s2.regular_saver AND s1.regular_saver_frequency_period = s2.regular_saver_frequency_period AND s1.regular_saver_frequency_type = s2.regular_saver_frequency_type AND s1.regular_saver_min_amt = s2.regular_saver_min_amt AND s1.regular_saver_max_amt = s2.regular_saver_max_amt AND s1.bonus = s2.bonus AND s1.bonus_frequency_period = s2.bonus_frequency_period AND s1.bonus_frequency_type = s2.bonus_frequency_type AND s1.savings_period = s2.savings_period AND s1.min_amt = s2.min_amt AND s1.max_amt = s2.max_amt AND s1.interest_paid = s2.interest_paid 
				AND j2.delete_date IS NOT NULL)))
UNION

SELECT
	CASE WHEN (j1.delete_date IS NULL) THEN j1.cr_date WHEN (j1.delete_date IS NOT NULL) THEN j1.delete_date ELSE NULL::date END AS change_date,
	s1.institution_code,
	s1.variability,
	s1.isa,
	s1.child,
	s1.online,
	s1.branch,
	s1.interest_paid,
	s1.regular_saver,
	s1.regular_saver_frequency_period,
	s1.regular_saver_frequency_type,
	s1.regular_saver_min_amt,
	s1.regular_saver_max_amt,
	s1.bonus,
	s1.bonus_frequency_period,
	s1.bonus_frequency_type,
	s1.savings_period,
	s1.min_amt,
	s1.max_amt,
	s1.gross_percent,
	s1.aer_percent,
	j1.last_retrieved,
	t1.institution_name,
	u1.url,
	s1.savings_id,
	j1.cr_date,
	CASE WHEN (j1.delete_date IS NULL) THEN 'ADDED'::text WHEN (j1.delete_date IS NOT NULL) THEN 'DELETED'::text ELSE NULL::text END AS action_type 
FROM
	tsavings s1,
	tsavingsjrnl j1,
	tinstitution t1,
	turl u1 
WHERE ((((s1.savings_id = j1.savings_id) AND (u1.url_id = j1.url_id)) AND ((t1.institution_code)::text = (s1.institution_code)::text)) AND (NOT (s1.savings_id IN (SELECT s1.savings_id FROM tsavings s1, tsavingsjrnl j1 WHERE (((s1.savings_id = j1.savings_id) AND (j1.delete_date IS NOT NULL)) AND (EXISTS (SELECT 1 FROM tsavings s2, tsavingsjrnl j2 WHERE ((((s2.savings_id = j2.savings_id) AND (j1.delete_date = j2.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND s2.variability = s1.variability AND s1.isa = s2.isa AND s1.child = s2.child AND s1.regular_saver = s2.regular_saver AND s1.regular_saver_frequency_period = s2.regular_saver_frequency_period AND s1.regular_saver_frequency_type = s2.regular_saver_frequency_type AND s1.regular_saver_min_amt = s2.regular_saver_min_amt AND s1.regular_saver_max_amt = s2.regular_saver_max_amt AND s1.bonus = s2.bonus AND s1.bonus_frequency_period = s2.bonus_frequency_period AND s1.bonus_frequency_type = s2.bonus_frequency_type AND s1.savings_period = s2.savings_period AND s1.min_amt = s2.min_amt AND s1.max_amt = s2.max_amt AND s1.interest_paid = s2.interest_paid 
AND (j2.delete_date IS NULL)))))
UNION SELECT s1.savings_id FROM tsavings s1, tsavingsjrnl j1 WHERE (((s1.savings_id = j1.savings_id) AND (j1.delete_date IS NULL)) AND 
(EXISTS (SELECT 1 FROM tsavingsjrnl j2, tsavings s2 WHERE (((((((((s2.savings_id = j2.savings_id) AND (j2.delete_date = j1.cr_date)) AND ((s2.institution_code)::text = (s1.institution_code)::text)) AND s2.variability = s1.variability AND s1.isa = s2.isa AND s1.child = s2.child AND s1.regular_saver = s2.regular_saver AND s1.regular_saver_frequency_period = s2.regular_saver_frequency_period AND s1.regular_saver_frequency_type = s2.regular_saver_frequency_type AND s1.regular_saver_min_amt = s2.regular_saver_min_amt AND s1.regular_saver_max_amt = s2.regular_saver_max_amt AND s1.bonus = s2.bonus AND s1.bonus_frequency_period = s2.bonus_frequency_period AND s1.bonus_frequency_type = s2.bonus_frequency_type AND s1.savings_period = s2.savings_period AND s1.min_amt = s2.min_amt AND s1.max_amt = s2.max_amt AND s1.interest_paid = s2.interest_paid AND j2.delete_date IS NOT NULL))) AND (j2.delete_date IS NOT NULL)))))))))))
)
ORDER BY 1 DESC, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,22,20
