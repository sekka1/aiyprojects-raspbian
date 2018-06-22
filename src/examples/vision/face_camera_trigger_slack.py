#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Trigger PiCamera when face is detected."""

from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection
from picamera import PiCamera

import urllib.request
import json

import boto3

import string
import random

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def main():
    with PiCamera() as camera:
        # Configure camera
        camera.resolution = (1640, 922)  # Full Frame, 16:9 (Camera v2)
        camera.start_preview()

        # Do inference on VisionBonnet
        with CameraInference(face_detection.model()) as inference:
            for result in inference.run():
                if len(face_detection.get_faces(result)) >= 1:
                    print("Face detected")

                    random_string = id_generator()

                    camera.capture('/tmp/faces.jpg')

                    # Send message to slack
                    url = "https://hooks.slack.com/services/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"

                    data_slack = {
                        "channel":"#visionbot",
                        "username":"webhookbot",
                        "text": "There was a face detected",
                        "attachments": [
                                {
                                    "fallback": "Required plain-text summary of the attachment.",
                                    "color": "#2eb886",
                                    "pretext": "Optional text that appears above the attachment block",
                                    "author_name": "VisionBonnet",
                                    "author_link": "http://www.devops.bot",
                                    "author_icon": "http://flickr.com/icons/bobby.jpg",
                                    "title": "VisionBonnet has detected a face",
                                    "title_link": "http://www.devops.bot",
                                    "text": "Optional text that appears within the attachment",
                                    "fields": [
                                        {
                                            "title": "Priority",
                                            "value": "High",
                                            "short": "false"
                                        }
                                    ],
                                    "image_url": "https://s3.amazonaws.com/visionbot/"+random_string+".png",
                                    "thumb_url": "https://s3.amazonaws.com/visionbot/"+random_string+".png",
                                    "footer": "VisionBonnet",
                                    "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
                                }
                            ]
                        }

                    print("Uploading picture to s3: https://s3.amazonaws.com/visionbot/"+random_string+".png")

                    # upload file to s3
                    s3 = boto3.resource('s3')
                    data_picture = open('/tmp/faces.jpg', 'rb')
                    s3.Bucket('visionbot').put_object(Key=random_string+'.png', Body=data_picture)

                    print("Sending Slack message")

                    # Send slack message
                    params = json.dumps(data_slack).encode('utf8')
                    req = urllib.request.Request(url, data=params,
                                                 headers={'content-type': 'application/json'})
                    response = urllib.request.urlopen(req)


        # Stop preview
        camera.stop_preview()


if __name__ == '__main__':
    main()
