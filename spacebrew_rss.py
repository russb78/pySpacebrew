#!/usr/bin/python
import time
import feedparser
from collections import deque
from spacebrewInterface.spacebrew import SpaceBrew

# time in second before sending another entry in the feed
updateTime = 3

# how many items will be stored at a time
feedlength = 50

# Using a deque and settting it's maximum length - http://docs.python.org/2/library/collections.html#deque-objects
feedDeque = deque(maxlen=feedlength)

# Set the feed to the default unless you receive a string for a new url
updatefeed = True

# Track where we are in the deque
currentplace = 0

# This feed will be loaded by default if no one sends a new url string
defaultfeed = "http://interactivestuff.tumblr.com/rss"

# We will always pay attention to the currentfeed, so fill that with the default for now
currentfeed = defaultfeed

# Construct a brew by passing in its name and the server you
# want to connect to.
brew1 = SpaceBrew("rssfeeder2",server="localhost")
pubs = ["title", "summary", "source", "author", "content", "link", "tags"]
# This brew will publish a string called "titles" containing the titles from the rss feed.
for pub in pubs:
    brew1.addPublisher(pub)
brew1.addSubscriber("feedurl")

# For any subscriber, you can define any number of functions
# that will get called with the sent value when a message arrives.
# Here's a simple example of a function that recieves a value.
def updateFeed(value):
    print "Changing feed to: ",value
    d = feedparser.parse(value)
    currentfeed = value
    feedDeque.extend(d.entries)
#    for item in d.entries:
#	i = {}
#        for pub in pubs:
#            try:
#                i[pub] = getattr(item, pub)
#            except:
#                i[pub] = ''
#        feedDeque.append(i)

# We call "subscribe" to associate a function with a subscriber.
brew1.subscribe("feedurl",updateFeed)

# Calling start on a brew starts it running in a separate thread.
brew1.start()

# We'll publish a value every few seconds. 
try:
    while True:
        time.sleep(updateTime)
        if (updatefeed == True):
            updatefeed = False
            if (currentfeed == defaultfeed):
                updateFeed(defaultfeed)

	if len(feedDeque) <= 0:
            updateFeed(currentfeed)
        item = feedDeque.popleft()
        for pub in pubs:
            try:
                brew1.publish(pub, getattr(item, pub))
            except:
                pass
except (KeyboardInterrupt, SystemExit) as e:
    # Calling stop on a brew disconnects it and waits for its
    # associated thread to finish.
    brew1.stop()

