#!/bin/sh

set -xe

URL='https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/GMFCTR/IZQODZ'
FILENAME=dataset.csv

# Download the dataset
wget -v "$URL" -O "${FILENAME}-wget"

# Remove the first 5 columns
cut --complement -d, -f1,2,3,4,5 "${FILENAME}-wget" > "${FILENAME}-cut"

# Remove the trailing comma and '\r' characters
sed 's/[,\r]*$//' "${FILENAME}-cut" > "${FILENAME}-sed"

# Remove the first line containing the header
tail -n +2 "${FILENAME}-sed" > "${FILENAME}-tail"

# Remove invalid UTF-8 characters
cat "${FILENAME}-tail" \
    | iconv -c -f utf8 -t ascii//TRANSLIT//IGNORE > "$FILENAME"

# Remove temporary files
rm "${FILENAME}-"*
