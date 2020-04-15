#!/bin/bash

CUR_DIR=$(dirname "$0")

wget -o ${CUR_DIR}/_hofi.log -O ${CUR_DIR}/_hofi.pdf http://asp.mot.gov.il/SPA_HE/SQ/sq4.pdf
wget -o ${CUR_DIR}/equ.log -O ${CUR_DIR}/_equ.pdf http://asp.mot.gov.il/SPA_HE/SQ/sq5.pdf
wget -o ${CUR_DIR}/_mec.log -O ${CUR_DIR}/_mec.pdf http://asp.mot.gov.il/SPA_HE/SQ/sq6.pdf
wget -o /dev/null -o ${CUR_DIR}/_yam.log -O ${CUR_DIR}/_yam.pdf http://asp.mot.gov.il/SPA_HE/SQ/sq3.pdf
wget -o /dev/null -o ${CUR_DIR}/_yam_extra.log -O ${CUR_DIR}/_yam_extra.pdf http://asp.mot.gov.il/SPA_HE/SQ/sq11.pdf

RET=`md5sum ./*pdf ./original_files/*pdf | awk '{print $1}' | sort | uniq -u | wc -l`
if [ ${RET} -eq 0 ]; then
    echo "Everything is up to date"
    rm ${CUR_DIR}/*pdf
    rm ${CUR_DIR}/*log

    exit 0
fi

echo "Please update answer and question files"
exit 1
