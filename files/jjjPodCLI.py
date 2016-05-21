#!/usr/bin/python

import jjjPod
import sys

show = sys.argv[1]

print jjjPod.showToFeed(jjjPod.showFeedURL(show))
