#!/bin/bash
if [ ! -f "commstream.txt" ]; then
    echo -e "\033[91m[ERROR] \033[0mfirst start analysing"
    exit 1
fi
gource --realtime --log-format custom commstream.txt
