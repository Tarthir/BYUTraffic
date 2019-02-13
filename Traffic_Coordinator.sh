#!/usr/bin/env bash
WD=$(pwd)

# an array of paths to files.
# 0 is to the .pcap files
# 1 is the queries.log

echo "Please give the full path to where the .pcap files are"
read loc
echo "Please give the full path to where the queries.log files are"
read loc2
echo "Please give the full path to where the ditl .gz files are"
read loc3

# delete all previous data files if they exist
rm -rf $WD/data/*
mkdir $WD/data/unzipped_pcap/
mkdir $WD/data/p0f_files/
mkdir $WD/errorlogs/

# Run our parsing, give it the location of the queries.log files
echo "PARSER.PY"
python $WD/model/parser.py $loc2 $WD/data/ asnDataByu.asn 2> $WD/errorlogs/prser.err
# Run p0fer.py, give path to .pcap files, where the unzipped files go, and final log files go
echo "P0FER.PY"
python $WD/model/p0fer.py $loc $WD/data/unzipped_pcap/ $WD/data/p0f_files/ 2> $WD/errorlogs/p0fer.err
# Run getASN.py, give path to where we will put asnDataByu.asn and give where final p0f log files are
echo "GETASN.PY"
python $WD/model/getASN.py $WD/data/asnDataRoot.asn $WD/data/p0f_files/ 2> $WD/errorlogs/getASN.err
# Get all the Byu asn data
echo "BYU-ASN"
netcat whois.cymru.com 43 < $WD/data/asnDataByu.asn | sort -n > $WD/data/asnFinalDataByu.asn 2> $WD/errorlogs/cymruBYUASN.err
# Get all the Root asn data
echo "ROOT-ASN"
netcat whois.cymru.com 43 < $WD/data/asnDataRoot.asn | sort -n > $WD/data/asnFinalDataRoot.asn 2> $WD/errorlogs/cymruRootASN.err
# Venn diagram the ditl-2018 and byu authoritative traffic data
echo "DITL_BYU_COMPARISON.PY"
python $WD/model/ditl_byu_comparison.py $loc3 $WD/data/asnDataByu.asn $WD/data 2> $WD/errorlogs/ditlcomp.err
# Dig results - put them in a file
echo "TTL_DIG.PY"
python $WD/model/ttl_dig.py $WD/data/query_names_to_dig $WD/data/ 2> $WD/errorlogs/ditlError.err
# Add all data we got from asn and p0f to our data sets
echo "DATAADDER.PY"
python3 $WD/model/DataAdder.py $WD/data/asnFinalDataRoot.asn $WD/data/asnFinalDataByu.asn $WD/data/p0f_files/ $WD/data/ 2> $WD/errorlogs/dataAdderError.err

echo "DONE!"


