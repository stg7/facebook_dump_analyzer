facebook_dump_analyzer
======================

Analyze facebook dump, build diagrams, statistics...

requiements
-----------
* just testen on linux
* python3
* gource (for video)
* ffmpeg (for creation of video file)
* facebook dump
    * request a facebook dump
    * facebook will send you a download link, so download and extract dump files

why?
----
Everyone who is using facebook generates a lot of data, that are stored on facebook servers.
Facebook can analyze this data better than this small programm, it should give you just an overview about what is possible.
My facebook message dump has just a size of 8 mb, so it is just a small sector of the possibilities.

### video
In the video you can see your chat behavior. Image an analyze could show that you are using facebook mostly at night, or with witch person you have chatted a lot, so this is an important person in your live. Think about
data that is not stored in this facebook dumps, e.g. geo spatial data. So it could be possible to get your
chatting places, and predict when and where you will start a chat.

### message analyzing
Your language skills can be analyzed, e.g. you are using much complicated words, or words from a specific field.
So based on this special words it could be predictible wich kind of facebook user you are: using for work only,
private user,... In which topics you are interested- could be extracted.
Do you always reply on written messages- how large are your answers. Or which persons do you not answer - do you not like.

How do you feel? Based on smileys/idicator words it could be analyzed.


### group analyze
based on chat groups, it could be extracted which persons are friends.
Which topics are important for this groups.
How does this comunities change in time?

general
-------
facebook is just one example where such logs are stored. There are a lot of other data sources, e.g. amazon ordering,
ebay auctions, xmpp chat logs, twitter messages, emails, surf behaivior, whatsapp logs.
