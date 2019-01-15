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
# TODO we will need to tweak p0fer.py and getASN.py to be more flexible and less hardcoded

python $(WD)/model/parser.py ${paths[3]}

python $(WD)${paths[0]} ${paths[2]} $(WD)/data/

python $(WD)${paths[1]}
