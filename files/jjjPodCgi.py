#!/usr/bin/python

import cgi
import jjjPod


arguments = cgi.FieldStorage()
show = arguments["show"].value

print """Content-Type: application/rss+xml;charset=utf-8
"""
print jjjPod.showToFeed(jjjPod.showFeedURL(show))
