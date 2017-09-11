#!/usr/bin/python

import re
import urllib2
import hashlib
import time
import traceback

def showToFeed(showURLs):
    if not isinstance(showURLs, list):
        showURLs = [showURLs]

    episodes = []

    try:
        for showURL in showURLs:
            response = urllib2.urlopen(showURL)
            xml = response.read()

            #get show title
            titlePattern = re.compile(r'<title>(.*?)</title>', re.I | re.M)
            title = titlePattern.findall(xml)[1]

            #get show link
            linkPattern = re.compile(r'<link>(.*?)</link>', re.I | re.M)
            link = linkPattern.findall(xml)[0]


            #get show episodes
            episodePattern = re.compile(r'<item>(.*?)</item>', re.I | re.M | re.S)
            rawEpisodes = episodePattern.findall(xml)

            #get images
            imagePattern = re.compile(r'<image>.*<url>(.*)</url>.*<title>(.*)</title>.*<link>(.*)</link>.*</image>', re.I | re.M | re.S)
            showImage = imagePattern.findall(xml)[0]

            mediaPattern = re.compile(r'<media:content .*(http.*mp3).*bitrate="128".*>', re.I | re.M)
            datePattern = re.compile(r'.*-([0-9]+-[0-9]+-[0-9]+).mp3')

            for rawEpisode in rawEpisodes:

                #get media link
                url = mediaPattern.findall(rawEpisode)[0]
                date = datePattern.findall(url)[0]
                episodeTitle = titlePattern.findall(rawEpisode)[0]

                episodes.append ({'url':     url,
                                  'date':    date,
                                  'title':   episodeTitle})

    except Exception as e:
        output = "Error generating feed..."
        #traceback.print_exc()

    show = {'title':            title,
             'link':            link,
            'image':            showImage,
            'episodes':         episodes}

    return generateFeed(show)


def generateFeed(show):

    channelImage = """<image>
                <url>%s</url>
                <title>%s</title>
                <link>%s</link>
            </image>""" % tuple(show['image'])

    imageTag = """<itunes:image href="%s" />""" % (show['image'][0])

    output = u"""<?xml version="1.0" encoding="UTF-8"?>
    <rss
        xmlns:atom="http://www.w3.org/2005/Atom"
        xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
        xmlns:itunesu="http://www.itunesu.com/feed" version="2.0">

        <channel>
            <title>%s</title>
            <link>%s</link>
            %s
            %s""" % (show['title'], show['link'], channelImage, imageTag)

    for episode in show['episodes']:

        guid = hashlib.sha256(episode['url']).hexdigest()
        longDate = time.strftime("%a, %d %b %Y 00:00:00", time.strptime(episode['date'], '%Y-%m-%d'))

        output += u"""
            <item>
                <title>%s</title>
                <enclosure url="%s" />
                <guid>%s</guid>
                <pubDate>%s</pubDate>
                %s
            </item>""" % (episode['title'], episode['url'], guid, longDate, imageTag)


    output += u"""
        </channel>
    </rss>"""

    return output

def showFeedURL(showName):
    # Used http://www.abc.net.au/triplej/feeds/iphone/iphone-app-config.xml for URLs
    streams = {'kingsmill'            : 'http://www.abc.net.au/triplej/media/mod/kin.xml',
               'home_and_hosed'       : 'http://www.abc.net.au/triplej/media/mod/hhs.xml',
               'safran'               : 'http://www.abc.net.au/triplej/media/mod/sns.xml',
               'hip_hop'              : 'http://www.abc.net.au/triplej/media/mod/hip.xml',
               'house_party'          : 'http://www.abc.net.au/triplej/media/mod/hpy.xml',
               'mix_up'               : [
                                            'http://www.abc.net.au/triplej/media/mod/mix1.xml',
                                            'http://www.abc.net.au/triplej/media/mod/mix2.xml',
                                            'http://www.abc.net.au/triplej/media/mod/mix3.xml',
                                            'http://www.abc.net.au/triplej/media/mod/mix4.xml'
                                        ],
               'friday_night_shuffle' : 'http://www.abc.net.au/triplej/media/mod/fns.xml',
               'roots_n_all'          : 'http://www.abc.net.au/triplej/media/mod/rna.xml',
               'the_racket'           : 'http://www.abc.net.au/triplej/media/mod/rac.xml',
               'short_fast_loud'      : 'http://www.abc.net.au/triplej/media/mod/sfl.xml',
               'soundlab'             : 'http://www.abc.net.au/triplej/media/mod/slb.xml'}
    return streams[showName]
