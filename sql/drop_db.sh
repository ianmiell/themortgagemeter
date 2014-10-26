if [ `hostname` = "themortgagemeter" ]
then
	echo "Not running on live!"
	exit
else
	psql themortgagemeter < DROP_TABLES.sql
fi
