#!/usr/bin/env python3
import argparse
import sys
import os
import shelve
import re
import datetime
import time
import shelve

import loader

from log import *
from system import *
from nlp import *
from bs4 import BeautifulSoup

"""
weitere ideen:
    zeitlicher verlauf der chats, visualisierung mittels gource
"""

def convert_time_to_unix_timestamp(timestamp):
    # e.g. 'Tuesday, November 4, 2014 at 2:02pm UTC+01'
    tmp = timestamp.split(", ")

    mount_day = tmp[1] #  e.g. November 4

    tmp2 = tmp[2].split(" at ")
    year = tmp2[0]
    tmp3 = tmp2[1].split(" ")
    timestr = tmp3[0]
    utcdiff = tmp3[1].replace("UTC", "")

    mount_day_TIME = time.strptime(mount_day, "%B %d")

    time_TIME = time.strptime(timestr, "%I:%M%p")

    td = datetime.timedelta(hours=int(utcdiff))

    d = datetime.datetime(int(year), mount_day_TIME.tm_mon, mount_day_TIME.tm_mday, time_TIME.tm_hour, time_TIME.tm_min)
    d = d + td
    return (year, d.strftime("%s"))


def create_histo(listofmsg):
    histo = {}
    for m in listofmsg:
        tidy_m = re.sub("[^a-z0-9öäüß ]", " ", m.lower())
        words = [x for x in tidy_m.split(" ") if x != ""]
        for w in words:
            histo[w] = histo.get(w, 0) + 1
    return histo


def analyse_histo(histo):
    histo_list = []
    for k in histo:
        if k not in german_stop_words() and len(k) > 1 and not re.match("[0-9]", k):
            histo_list.append((k, histo[k]))
    histo_list.sort(key=lambda tup: tup[1], reverse=True)
    return [x[0] for x in histo_list]


def analyse_msg(msg):
    listofmsg = []
    for m in msg:
        if len(m) != 0:
            words = [x for x in m.split(" ") if x != ""]
            if len(words) == 0:
                print((words, m))

            listofmsg.append(words)

    min_len = min([len(x) for x in listofmsg])
    max_len = max([len(x) for x in listofmsg])
    count = len(listofmsg)
    sum_len = sum([len(x) for x in listofmsg])
    return (min_len, sum_len / count, max_len)


def main(args):

    # argument parsing
    parser = argparse.ArgumentParser(description='XYZ', epilog="stg7 2014")
    parser.add_argument('message_file', type=str, help='facebook message.htm filename')
    parser.add_argument('-y', dest='year', type=str, default="", help='selected year')
    parser.add_argument('-u', dest='user_name', type=str, default="", help='username')
    parser.add_argument('-a', dest='anonymize', action='store_true', help='anonymize output')

    argsdict = vars(parser.parse_args())

    selected_year = argsdict["year"]
    anonymize = argsdict["anonymize"]
    messages_file = argsdict["message_file"]
    user_name = argsdict["user_name"]


    c = 0
    stats = {}
    timeseries = []
    thread_ids = {}
    user_ids = {}
    message_groups = {"you":[], "other": []}

    lInfo("analyze " + messages_file)
    if os.path.isfile("cache" + selected_year):
        cache = shelve.open("cache" + selected_year)
    else:
        messages = read_file(messages_file, enc="utf-8")
        soup = BeautifulSoup(messages)
        for thread in soup.find_all("div", {"class": "thread"}):
            conversation_partners = thread.contents[0].split(", ")
            threadname = ",".join(conversation_partners)
            thread_ids[threadname] = str(len(thread_ids))
            count = {}

            for message in thread.find_all("div", {"class": "message"}):
                user = message.find("span", {"class": "user"}).get_text()
                timestamp = message.find("span", {"class": "meta"}).get_text()
                (year, unixtimestamp) = convert_time_to_unix_timestamp(timestamp)

                if selected_year == "" or year == selected_year:
                    text_msg = message.nextSibling.get_text().replace("\n", " ")
                    if user == user_name:
                        message_groups["you"].append(text_msg)
                    else:
                        message_groups["other"].append(text_msg)

                    timeseries.append([unixtimestamp, user, "A", threadname])
                    if user not in user_ids:
                        user_ids[user] = str(len(user_ids))
                    count[user] = count.get(user, 0) + 1

            stats[",".join(set(conversation_partners) - set([user_name]))] = count
            lInfo(str(c) + " thread processed")
            c += 1

        cache = shelve.open("cache" + selected_year)
        cache["timeseries"] = timeseries
        cache["user_ids"] = user_ids
        cache["stats"] = stats
        cache["thread_ids"] = thread_ids
        cache["message_groups"] = message_groups

    timeseries = cache["timeseries"]
    user_ids = cache["user_ids"]
    stats = cache["stats"]
    thread_ids = cache["thread_ids"]
    message_groups = cache["message_groups"]
    cache.close()

    lInfo("analyze messages: commstream.txt")
    # sort time series
    timeseries.sort(key=lambda tup: tup[0])
    user_ids[user_name] = "you"

    if anonymize:
        timeseries = [[x[0], user_ids[x[1]], x[2], thread_ids[x[3]]]  for x in timeseries]

    timeseries = [x if x[1] != "you" else [x[0], x[1], "M", x[3]] for x in timeseries]

    # output results
    f = open("commstream.txt", "w")
    for l in timeseries:
        f.write("|".join(l) + "\n")
    f.close()

    lInfo("create diagrams: commdia.html")
    tmp = []
    for threadname in stats:
        info = stats[threadname]
        you = 0
        if user_name in info:
            you = info[user_name]
        other = sum([info[x] for x in info if x != user_name])
        if you != 0 and other != 0:
            tmp.append((you + other, threadname, you, other))

    tmp.sort(key=lambda tup: tup[0], reverse=True)

    f = open("commdia.html", "w")
    f.write("""<!DOCTYPE html>
    <head>
    <meta charset="UTF-8">
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Thread', 'You', 'Other'],""" + "\n")

    i = 0
    for (c, threadname, you, other) in tmp:
        if anonymize:
            threadname = str(i)
        f.write("['{0}', {1}, {2}],\n".format(threadname, you, other))
        i += 1

    f.write("""

        ]);

        var options = {
          title: 'Communication stats """ + selected_year + """',
          isStacked: true
        };

        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: """ + str(len(stats) * 15) + """px;"></div>
  </body>
</html>

    """)
    f.close()

    lInfo("deep analyse messages:")
    lInfo("you wrote:{0} , other wrote:{1} ".format(len(message_groups["you"]),len(message_groups["other"])))
    lInfo("messages: you: min_len, avg_len, max_len: " + str(analyse_msg(message_groups["you"])))
    lInfo("messages: other: min_len, avg_len, max_len: " + str(analyse_msg(message_groups["other"])))

    # analyse most written words
    histo_you = create_histo(message_groups["you"])
    histo_other = create_histo(message_groups["other"])
    analyse_you = analyse_histo(histo_you)
    analyse_other = analyse_histo(histo_other)

    lInfo("histo[you]" + str(analyse_you[0:20]))
    lInfo("histo[other]" + str(analyse_other[0:20]))

    lInfo("histo[you-other]" + str(analyse_histo({x: histo_you[x] for x in histo_you if x not in histo_other})[0:20]))

    # chat group connection: also jede chatgruppe/thread communications partner kennen sich
    #   -> was ergibt sich dann als graph


if __name__ == "__main__":
    main(sys.argv[1:])
