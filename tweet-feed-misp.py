import urllib3,requests
from pymisp import ExpandedPyMISP, MISPEvent, MISPAttribute
from datetime import datetime

misp_key = 'changeme'
misp_domain = 'changeme'
misp_verifycert = False

urllib3.disable_warnings()

today = datetime.now()

misp = ExpandedPyMISP(misp_domain, misp_key, misp_verifycert)

url_tweetfeed='https://api.tweetfeed.live/v1/today'

ioc_response=requests.get(url_tweetfeed).json()

if not ioc_response==[]:
    event = MISPEvent()
    event.info = 'TweetFeed IoCs - ' + str(today.strftime('%Y-%m-%d'))
    event.add_tag('tlp:white')
    event.distribution = 3
    event.analysis = 2
    misp.add_event(event)
    for ioc in ioc_response:
        attribute = MISPAttribute()
        tweet=ioc['tweet']
        if not ioc['tags']==[]:
            tag=ioc['tags'][0]
        else:
            tag=""
        if ioc['type'] == "ip":
            ioc_value=ioc['value']
            attribute.type = 'ip-dst'
        elif ioc['type'] == "domain":
            ioc_value=ioc['value']
            attribute.type = 'domain'
        elif ioc['type'] == "url":
            ioc_value=ioc['value']
            attribute.type = 'url'
        elif ioc['type'] == "md5":
            ioc_value=ioc['value']
            attribute.type = 'md5'
        elif ioc['type'] == "sha256":
            ioc_value=ioc['value']
            attribute.type = 'sha256'
        attribute.value = ioc_value
        attribute.comment=tweet
        if not tag=="":
            attribute.Tag=[str(tag)]
            event.add_attribute(attribute.type, attribute.value, comment=attribute.comment, Tag=attribute.Tag)
        else:
            event.add_attribute(attribute.type, attribute.value, comment=attribute.comment)
        misp.update_event(event)
    event.publish()
    misp.update_event(event)