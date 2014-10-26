cd ../retrieval/savings
python main.py --institution HLFX $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution HSBC $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
wait
## Insert the current date into the retrieval_dates table
# TODO: work out where to store this - maybe in dedicated table, or with "type" column in tretrievaldates
#echo "insert into tretrievaldates (day) values (current_date);" | psql themortgagemeter
## Refresh materialized views
#echo "select refresh_matview('replacement_mortgages_materialized_view');" | psql themortgagemeter
## Clear the cache
#cd -
#clear_cache.sh
