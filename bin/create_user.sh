if [ `whoami` != "postgres" ]
then
	echo "Need to be postgres to run this"
	exit
fi
createuser -s themortgagemeter
echo "alter user themortgagemeter with password 'postgres'" | psql postgres
