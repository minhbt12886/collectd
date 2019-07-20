#!/bin/bash
HOSTNAME="${COLLECTD_HOSTNAME:-localhost}"
INTERVAL="${COLLECTD_INTERVAL:-10}"
USER="**"
PASSWORD="**"
DBS="A B"
DB_AUTH="admin"
MONGO_SERVER="***:27017"
while sleep "$INTERVAL";do
	for db in $DBS;do
		collections=$(mongo --quiet ${MONGO_SERVER}/${db} --authenticationDatabase $DB_AUTH -u${USER} -p${PASSWORD} --eval 'db.getCollectionNames()'|sed 's/\[//g'|sed 's/\]//g'|sed 's/"//g'|sed 's/,//g')
		for collection in $collections;do
			query="db.${collection}.count()"
			res=$(mongo --quiet ${MONGO_SERVER}/${db} --authenticationDatabase $DB_AUTH -u${USER} -p${PASSWORD} --eval "$query")
			echo "PUTVAL \"$HOSTNAME/test1-mongo-$db-${collection}/gauge-documents\" interval=$INTERVAL N:$res"
		done
	done
done
