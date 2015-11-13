#!/bin/bash
if [ ! -f "commstream.txt" ]; then
    echo -e "\033[91m[ERROR] \033[0mfirst start analysing"
    exit 1
fi
gource -1280x720 -c 4 -s 0.1 --log-format custom commstream.txt -o - \
    | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4

