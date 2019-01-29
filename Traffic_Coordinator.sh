#!/usr/bin/env bash
WD=$(pwd)

# an array of paths to files.
# 0 is to the .pcap files
# 1 is the queries.log

echo "Please give the full path to where the .pcap files are"
read loc
echo "Please give the full path to where the queries.log files are"
read loc2

# delete all previous data files if they exist
rm -rf $WD/data/*
mkdir $WD/data/unzipped_pcap/
mkdir $WD/data/p0f_files/


# Run our parsing, give it the location of the queries.log files
python $WD/model/parser.py $loc2 $WD/data/ $WD/data/asnDataByu.asn
# Run p0fer.py, give path to .pcap files, where the unzipped files go, and final log files go
python $WD/model/p0fer.py $loc $WD/data/unzipped_pcap/ $WD/data/p0f_files/
# Run getASN.py, give path to where we will put asnDataByu.asn and give where final p0f log files are
python $WD/model/getASN.py $WD/data/asnDataRoot.asn $WD/data/p0f_files/
# Get all the Byu asn data
netcat whois.cymru.com 43 < $WD/data/asnDataByu.asn | sort -n > $WD/data/asnFinalDataByu.asn
# Get all the Root asn data
netcat whois.cymru.com 43 < $WD/data/asnDataRoot.asn | sort -n > $WD/data/asnFinalDataRoot.asn
# Add all data we got from asn and p0f to our data sets
python3 $WD/model/DataAdder.py $WD/data/asnFinalDataRoot.asn $WD/data/asnFinalDataByu.asn $WD/data/p0f_files/ $WD/data/

# Venn diagram the ditl-2018 and byu authoritative traffic data
python $WD/ditl_byu_comparison.py path_to_ditl_file path_to_byu_authoritative_ips(data/Byu/asnDataByu.asn) Output_path
