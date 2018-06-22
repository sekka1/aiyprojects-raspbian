#!/usr/bin/env python3

import urllib.request
import json
import boto3

import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

random_string = id_generator()

url = "https://hooks.slack.com/services/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"

data_slack = {
    "channel":"#visionbot",
    "username":"webhookbot",
    "text": "test slack There was a face dected",
    "attachments": [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "color": "#2eb886",
                "pretext": "Optional text that appears above the attachment block",
                "author_name": "Bobby Tables",
                "author_link": "http://flickr.com/bobby/",
                "author_icon": "http://flickr.com/icons/bobby.jpg",
                "title": "Slack API Documentation",
                "title_link": "https://api.slack.com/",
                "text": "Optional text that appears within the attachment",
                "fields": [
                    {
                        "title": "Priority",
                        "value": "High",
                        "short": "false"
                    }
                ],
                "image_url": "https://s3.amazonaws.com/visionbot/"+random_string+".png",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "Slack API",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": 123456789
            }
        ]
    }

# Upload a new file
s3 = boto3.resource('s3')

# upload file
data_picture = open('/tmp/faces.jpg', 'rb')
s3.Bucket('visionbot').put_object(Key=random_string+'.png', Body=data_picture)

# Send slack message
params = json.dumps(data_slack).encode('utf8')
req = urllib.request.Request(url, data=params,
                             headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
