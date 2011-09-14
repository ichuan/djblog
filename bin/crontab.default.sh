#!/bin/bash

# report cmds
CMDS=( "ps auxk -rss" "free -m" "cat /proc/net/dev" "df -h" "uptime" )

# zip password
ZIP_PASS=55a8a0fae7b14756b3faf78b5f79c523d0aa95fe

# mysql
MYSQL_USER=root
MYSQL_PASS="faf78b5f"
MYSQL_DB=" db1 db2"

# from email address
FROM=backup@yoursite.com

# to email address
TO=youmail@gmailcom

# subject
SUBJECT="Report and Backup for `date +%F`"

exec_out(){
	for i in "${CMDS[@]}"; do
		[ -n "$i" ] && echo -e "\n\n" && echo "$i" && echo && $i
	done
}

export EMAIL=$FROM
f=/tmp/`date +%Y%m%d_%H%M%S`.sql.zip
mysqldump --add-drop-database -p"$MYSQL_PASS" -u$MYSQL_USER ${MYSQL_DB// / -B } | zip -9 -e -P "$ZIP_PASS" $f - && exec_out | mutt -s "$SUBJECT" -a $f -- $TO
rm $f
