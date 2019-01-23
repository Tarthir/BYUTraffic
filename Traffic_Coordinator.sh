#!/usr/bin/env bash
WD=$(pwd)

# an array of paths to files.
# 0 is to p0fer.py
# 1 is to getASN.py
# 2 is to the .pcap files
# 3 is the queries.log
paths=()

reader_loop(){
    idx=0
    while [[ -z "${loc// }" ]]
    do
        printf "That is not a correct path\n"
	    print_it
    done
    paths[$(idx)] = loc
    ((++idx))
}

print_it(){
    echo $1
    read loc
    reader_loop
}
print_it $("Please give the full path to p0fer.py")

print_it $("Please give the full path to getASN.py")

print_it $("Please give the full path to where the .pcap files are")

print_it $("Please give the full path to where the queries.log files are")
# delete all previous data files if they exist
if [-d "$WD/data/"]; then
    rm -rf $WD/data/*data
fi
# Run our parsing, give it the location of the queries.log files
python $WD/model/parser.py ${paths[3]} $WD/log_list_saved_data/ $WD/data/Byu/asnDataByu.asn
# Run p0fer.py, give path to .pcap files, where the unzipped files go, and final log files go
python $WD${paths[0]} ${paths[2]} $WD/data/unzipped_pcap/ $WD/data/p0f_files/
# Run getASN.py, give path to where we will put asnDataByu.asn and give where final p0f log files are
python $WD${paths[1]} $WD/data/Byu/asnDataByu.asn $WD/data/p0f_files/
# Get all the Byu asn data
netcat whois.cymru.com 43 < $WD/data/Byu/asnDataByu.asn | sort -n > $WD/data/finalByu/asnFinalDataByu.asn
# Get all the Root asn data
netcat whois.cymru.com 43 < $WD/data/Root/asnDataRoot.asn | sort -n > $WD/data/finalRoot/asnFinalDataRoot.asn
# Add all data we got from asn and p0f to our data sets
python $WD/model/DataAdder.py $WD/data/Root/asnDataRoot.asn $WD/data/Byu/asnDataByu.asn $WD/data/p0f_files/

# Venn diagram the ditl-2018 and byu authoritative traffic data
python $WD/ditl_byu_comparison.py path_to_ditl_file path_to_byu_authoritative_ips(data/Byu/asnDataByu.asn) Output_path