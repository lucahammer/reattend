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

response = requests.get(url).content
#print response #show the response

r = json.loads(response)
print r

#test for friendships between attendees
