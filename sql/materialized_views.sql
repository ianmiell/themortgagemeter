-- creates the matview
select create_matview('replacement_mortgages_materialized_view', 'replacement_mortgages_view');
-- refreshes the matview
select refresh_matview('replacement_mortgages_materialized_view');
-- creates the matview
select create_matview('replacement_savings_materialized_view', 'replacement_savings_view');
-- refreshes the matview
select refresh_matview('replacement_savings_materialized_view');
