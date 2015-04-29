# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on morph.io for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.

import scraperwiki
import os
import requests
import json

baseUrl = 'https://graph.facebook.com/v2.3'
attendeesIds = [526490627,500496573,442029195936418,10204303330976622,825465727516732,847516601944095,100000133660323,984442261569764]
connections = []

def next(nextUrl):
  print nextUrl
  nextResponse = requests.get(nextUrl).content
  nR = json.loads(nextResponse)
  # print nR
  for attendee in nR['data']:
    attendeesIds.append(attendee['id']) #add ID to global list
    unique_keys = ['id']
    attendeeData = {
      'id': attendee['id'],
      'name': attendee['name']
      }
    scraperwiki.sql.save(unique_keys, attendeeData)
  try:
    next(nR['paging']['next'])
  except:
    print 'No next-link'

#get facebook token and evend ID from the morph.io settings
if 'MORPH_FBTOKEN' in os.environ: #make code conditional on existence of a secret variable
  fbToken = os.environ['MORPH_FBTOKEN'] #use the secret variable (you can get it from https://developers.facebook.com/tools/explorer/)
else:
  print 'Please add a Facebook Access Token with the name "MORPH_FBTOKEN" to the morph.io settings of this scraper'
if 'MORPH_FBEVENTID' in os.environ: #make code conditional on existence of a secret variable
  fbEvent = os.environ['MORPH_FBEVENTID'] #use the secret variable (just copy it from the event URL into the settings)
else:
  print 'Please add the ID of a Facebook event with the name "MORPH_FBEVENT" to the morph.io settings of this scraper'
  
#test if token and event were importet properly
#print fbEvent
#print fbToken

#get attendees of the event
url = baseUrl+'/'+fbEvent+"/attending?access_token="+fbToken
#print url #test if url was created properly
###next(url) #get first page of attendees

#test for friendships between attendees
for i, attendee in enumerate(attendeesIds):
    print "element", i, "is", attendee
    for y in range (i+1, len(attendeesIds)):
      rUrl = baseUrl+'/'+attendee+'/friends/'+attendeesIds[y]+'?access_token=fbToken' 
      print rUrl
      rel = requests.get(rUrl).content
      rr = json.loads(rel)
      print rr
