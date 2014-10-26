HOST=`hostname`
if [ $HOST == "themortgagemeter" ]
then
    echo "Not running on live system!"
    exit
else
	echo "If role themortgagemeter doesn't exist, run ./create_user.sh as postgres first"
	cat ../sql/DROP_DATABASE.sql | psql postgres
	cat ../sql/CREATE_DATABASE.sql | psql postgres
	# Might reintroduce this in the future if we want to separate django tables.
	#./drop_db.sh
	psql themortgagemeter < ../sql/archive/SCHEMA_CURRENT.sql
	psql themortgagemeter < ../sql/archive/DATA_CURRENT.sql
fi
