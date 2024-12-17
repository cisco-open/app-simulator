#!/bin/sh
echo "Running CURL load in ${WAIT} seconds..."
echo "URLs to test"
echo "${URLS}"
echo "Sleep time in between requests ${SLEEP}"
sleep "${WAIT}"
while true; do
	ID=$(uuidgen)
	for URL in ${URLS}; do
		/usr/bin/curl -s "${URL}?unique_session_id=${ID}"
	done
	sleep "${SLEEP}"
done