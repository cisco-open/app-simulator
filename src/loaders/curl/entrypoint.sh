#!/bin/bash

LOADER_CONFIG="/config.json"

# Check if the file exists
if [[ ! -f "${LOADER_CONFIG}" ]]; then
  echo "Warning: $LOADER_CONFIG not found! Environment variables will be used instead."
else
  SLEEP=$(jq -r '.sleep' "$LOADER_CONFIG")
  WAIT=$(jq -r '.wait' "$LOADER_CONFIG")
  URLS=$(jq -r '.urls | join(" ")' "$LOADER_CONFIG")
fi


# Check if SLEEP and WAIT are numbers
if ! [[ "${SLEEP}" =~ ^[0-9]+$ ]]; then
  echo "Error: SLEEP is not a valid number: $SLEEP"
  exit 1
fi

if ! [[ "${WAIT}" =~ ^[0-9]+$ ]]; then
  echo "Error: WAIT is not a valid number: $WAIT"
  exit 1
fi

echo "Running CURL load in ${WAIT} seconds ..."
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