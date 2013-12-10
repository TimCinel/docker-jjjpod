#!/usr/local/bin/python

import re
import urllib2
import hashlib
import time
import cgi

def generateFeed(streamURL):
    try:
        response = urllib2.urlopen(streamURL)
        xml = response.read()
        
        #get feed title
        titlePattern = re.compile(r'<title>([^<]*)</title>', re.I | re.M)
        title = titlePattern.findall(xml)[1]
        
        #get feed link
        linkPattern = re.compile(r'<link>([^<]*)</link>', re.I | re.M)
        link = linkPattern.findall(xml)[0]
        
        #get media link(s)
        mediaPattern = re.compile(r'<media:content .*(http.*mp3).*bitrate="128".*>', re.I | re.M)
        urls = mediaPattern.findall(xml)
        
        datePattern = re.compile(r'.*-([0-9]+-[0-9]+-[0-9]+).mp3')
        
        output = u"""<?xml version="1.0" encoding="UTF-8"?>
        <rss>
            <channel>
        
            <title>%s</title>
            <link>%s</link>""" % (title, link)
        
        for url in urls:
        
            shortDate = datePattern.findall(url)[0]
            guid = hashlib.sha256(url).hexdigest()
            longDate = time.strftime("%a, %d %b %Y 00:00:00", time.strptime(shortDate, '%Y-%m-%d'))
        
            output += u"""
               <item>
                    <title>%s (%s)</title>
                    <enclosure url="%s" />
                    <guid>%s</guid>
                    <pubDate>%s</pubDate>
                </item>""" % (title, shortDate, url, guid, longDate)
        
        
        output += u"""
            </channel>
        </rss>"""
    except:
        output = "Error generating feed..."

    return output


# Used http://www.abc.net.au/triplej/feeds/iphone/iphone-app-config.xml for URLs

streams = {'kingsmill'            : 'http://www.abc.net.au/triplej/media/mod/kin1.xml'
           'home_and_hosed'       : 'http://www.abc.net.au/triplej/media/mod/hhsA.xml'
           'safran'               : 'http://www.abc.net.au/triplej/media/mod/sns1.xml'
           'hip_hop'              : 'http://www.abc.net.au/triplej/media/mod/hip1.xml'
           'house_party'          : 'http://www.abc.net.au/triplej/media/mod/hpy1.xml'
           'mix_up'               : 'http://www.abc.net.au/triplej/media/mod/mixA.xml'
           'friday_night_shuffle' : 'http://www.abc.net.au/triplej/media/mod/fns1.xml'
           'roots_n_all'          : 'http://www.abc.net.au/triplej/media/mod/rna1.xml'
           'the_racket'           : 'http://www.abc.net.au/triplej/media/mod/rac1.xml'
           'short_fast_loud'      : 'http://www.abc.net.au/triplej/media/mod/sfl1.xml'
           'soundlab'             : 'http://www.abc.net.au/triplej/media/mod/slb1.xml'}


arguments = cgi.FieldStorage()
stream = arguments["stream"].value
streamURL = streams[stream]

print """Content-Type: application/rss+xml;charset=utf-8
"""
print generateFeed(streamURL)
