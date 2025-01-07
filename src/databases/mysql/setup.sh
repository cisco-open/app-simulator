#!/bin/bash
APP_CONFIG="$(</config.json)" php /tmp/setup.php
mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" </tmp/create.sql
