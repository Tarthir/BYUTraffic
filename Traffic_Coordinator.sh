#!/usr/bin/env bash
WD=$(pwd)
idx=0
# an array of paths to files.
# 0 is to p0fer.py
# 1 is to getASN.py
# 2 is to the .pcap files
# 3 is the queries.log
paths=()

reader_loop(){
    while [[ -z "${loc// }" ]]
    do
        printf "That is not a correct path\n"
	    print_it
    done
    paths[$(idx)] = loc
}

print_it(){
    echo $1
    read loc
    reader_loop
}
print_it $("Please give the full path to p0fer.py")

print_it $("Please give the full path to getASN.py")

print_it $("Please give the full path to where the .pcap files are"

print_it $("Please give the full path to where the queries.log files are")
# delete all previous data files if they exist
if [-d "$(WD)/data/"]; then
    rm $(WD)/data/*
    rm $(WD)/data/final/*
fi
# Run our parsing, give it the location of the queries.log files
python $(WD)/model/parser.py ${paths[3]}
# Run p0fer.py, give path to .pcap files, and where the unzipped and final log files go
python $(WD)${paths[0]} ${paths[2]} $(WD)/data/ $(WD)/data/final/
# Run getASN.py, give path to where we will put asnData.data and give where final p0f log files are
# TODO still need to get the non .pcap data run through getASN.py, will take some refactoring
python $(WD)${paths[1]} $(WD)/data/asnData.data $(WD)/data/final/
# Get all the asn data
netcat whois.cymru.com 43 < $(WD)/data/asnData.asn | sort -n > $(WD)/data/final/asnFinalData.asn
