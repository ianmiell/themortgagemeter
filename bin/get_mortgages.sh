cd /opt/themortgagmeter/retrieval/mortgages
python main.py --institution NTNWD $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution SNTNDR $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution HLFX $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution NTWST $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution CHLS $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution TSC $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution SKPTN $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution HSBC $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution LLOYDS $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
python main.py --institution YRKSHR $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
# changed pages
#python main.py --institution PSTFFC $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
#python main.py --institution NRTHNR $MORTGAGE_COMPARISON_RETRIEVAL_REGRESSION_TEST &
wait
# Insert the current date into the retrieval_dates table
echo "insert into tretrievaldates (day) values (current_date);" | psql mortgagecomparison
# Refresh materialized views
echo "select refresh_matview('replacement_mortgages_materialized_view');" | psql mortgagecomparison
# Clear the cache
echo "Moving to bin"
cd /opt/themortgagemeter/bin
echo "Clearing cache"
./clear_cache.sh
echo "Cleared cache"
