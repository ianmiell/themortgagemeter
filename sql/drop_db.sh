if [ `hostname` = "themortgagemeter" ]
then
	echo "Not running on live!"
	exit
else
	psql mortgagecomparison < DROP_TABLES.sql
fi
