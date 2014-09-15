HOST=`hostname`
if [ $HOST = "themortgagemeter" ]
then
	DATE=`date +%Y%m%d`
	git config --global user.email "MORTGAGECOMPARISON_ADMINEMAIL"
	git config --global user.name "MORTGAGECOMPARISON_ADMINEMAIL"
	pg_dump mortgagecomparison -a > ../sql/archive/DATA_${DATE}.sql
	pg_dump mortgagecomparison -s > ../sql/archive/SCHEMA_${DATE}.sql
	cp ../sql/archive/SCHEMA_${DATE}.sql ../sql/archive/SCHEMA_CURRENT.sql
	cp ../sql/archive/DATA_${DATE}.sql ../sql/archive/DATA_CURRENT.sql
else
	echo "Not on live system!"
	exit
fi
