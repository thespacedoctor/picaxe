#!/usr/local/bin/python
# encoding: utf-8
"""
work with the Flickr API to upload images, sort images, generate MD image reference links etc.
"""

import sys
import os
import re
import time
from os.path import expanduser
import requests
import yaml
import webbrowser
from requests_oauthlib import OAuth1

from fundamentals import tools


class picaxe():
    """
    *work with the Flickr API to upload images, sort images, generate MD image reference links etc*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``pathToSettingsFile`` -- path to the settings file
    """
    # Initialisation

    def __init__(
            self,
            log,
            settings=False,
            pathToSettingsFile=False
    ):
        self.log = log
        log.debug("instansiating a new 'picaxe' object")
        self.settings = settings
        self.pathToSettingsFile = pathToSettingsFile
        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions

        return None

    def authenticate(self):
        """
        *setup a Flickr API key to access a Flickr user account so picaxe can work on private images*

        **Return:**
            - ``None``

        **Usage:**

            To authenicate pixace against a Flickr account run the following (note this is interactive so a human needs to be present to respond to prompts!)

            .. code-block:: python 

                from picaxe import picaxe
                flickrClient = picaxe(
                    log=log,
                    settings=settings
                )
                flickrClient.authenticate()
        """
        self.log.info('starting the ``authenticate`` method')

        if not self.settings["flickr"] or "consumer_key" not in self.settings["flickr"] or "consumer_secret" not in self.settings["flickr"]:
            print "Navigate here <https://www.flickr.com/services/apps/create/apply/> and request a 'non-commerial key'"
            time.sleep(2)
            ## open in webbrowser
            webbrowser.open_new_tab(
                "https://www.flickr.com/services/apps/create/apply/")

            consumer_key = raw_input("What is your new API key value? \n  >  ")
            consumer_secret = raw_input(
                "What is your new API secret value? \n  >  ")

        else:
            consumer_key = str(self.settings["flickr"]["consumer_key"])
            consumer_secret = str(self.settings["flickr"]["consumer_secret"])

        auth = OAuth1(consumer_key, consumer_secret)

        try:
            response = requests.get(
                url="http://www.flickr.com/services/oauth/request_token",
                params={
                    "oauth_callback": "http://www.thespacedoctor.co.uk",
                },
                auth=auth
            )
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        oauthList = response.content.split("&")
        oauth_token = str(oauthList[1].split("=")[1])
        oauth_token_secret = str(oauthList[2].split("=")[1])

        print "Now to authorize picaxe against your personal flickr account"
        print "Navigate to https://www.flickr.com/services/oauth/authorize?oauth_token=" + oauth_token + " and click on 'OK, I'LL AUTHOURIZE IT'"
        time.sleep(1)
        webbrowser.open_new_tab(
            "https://www.flickr.com/services/oauth/authorize?oauth_token=" + oauth_token)

        oauth_verifier = raw_input(
            "What is the oauth_verifier value in URL you where redirected to? \n  >  ")
        oauth_verifier = str(oauth_verifier.strip())

        auth = OAuth1(consumer_key, consumer_secret,
                      oauth_token, oauth_token_secret)

        try:
            response = requests.get(
                url="https://www.flickr.com/services/oauth/access_token",
                params={
                    "oauth_verifier": oauth_verifier,
                    "oauth_callback": "http://www.thespacedoctor.co.uk"
                },
                auth=auth
            )
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        oauthList = response.content.split("&")
        oauth_token = oauthList[1].split("=")[1]
        oauth_token_secret = oauthList[2].split("=")[1]
        user_nsid = oauthList[3].split("=")[1]
        username = oauthList[4].split("=")[1]

        if not self.pathToSettingsFile:
            self.pathToSettingsFile = expanduser(
                "~") + "/.config/picaxe/picaxe.yaml"

        stream = file(self.pathToSettingsFile, 'r')
        yamlContent = yaml.load(stream)
        stream.close()

        yamlContent["flickr"] = {}
        yamlContent["flickr"]["consumer_key"] = consumer_key
        yamlContent["flickr"]["consumer_secret"] = consumer_secret
        yamlContent["flickr"]["oauth_token"] = oauth_token
        yamlContent["flickr"]["oauth_token_secret"] = oauth_token_secret
        yamlContent["flickr"]["user_nsid"] = user_nsid
        yamlContent["flickr"]["username"] = username

        stream = file(self.pathToSettingsFile, 'w')
        yaml.dump(yamlContent, stream, default_flow_style=False)
        stream.close()

        self.log.info('completed the ``authenticate`` method')
        return None

    def get_photo_metadata(
            self,
            url):
        """*get useful image metadata for the image found at a give Flickr share URL*

        **Key Arguments:**
            - ``url`` -- the share URL for the flickr image (or just the unique photoid)

        **Return:**
            - ``images`` -- a dictionary of the various image sizes that can be accessed (key is the width in pixels and value is the direct image URL)
            - ``title`` -- the title of the image as set by the user
            - ``desc`` -- the description of the image as set by the user
            - ``photoId`` -- the unique photoID of the image

        **Usage:**

            To get some associated metadata related to the image at a given Flcikr share URL run the `get_photo_metadata` method. Note the URL can be any of the various Flickr URL flavours.

            .. code-block:: python 

                from picaxe import picaxe
                flickr = picaxe(
                    log=log,
                    settings=settings
                )
                images, title, desc, photoId = flickr.get_photo_metadata(
                    url="https://www.flickr.com/photos/92344046@N06/30455210056")

                images, title, desc, photoId= flickr.get_photo_metadata(url="https://www.flickr.com/gp/923440134@N06/0930a6")

                images, title, desc, photoId = flickr.get_photo_metadata(url="http://flic.kr/p/NpdUV5")

                images, title, desc, photoId = flickr.get_photo_metadata(url=30455210056)

        """
        self.log.info('starting the ``get_photo_metadata`` method')

        if "oauth_token" not in self.settings["flickr"] or "oauth_token_secret" not in self.settings["flickr"]:
            self.authenticate()
            print "Now try again"

        consumer_key = str(self.settings["flickr"]["consumer_key"])
        consumer_secret = str(self.settings["flickr"]["consumer_secret"])
        oauth_token = str(self.settings["flickr"]["oauth_token"])
        oauth_token_secret = str(self.settings["flickr"]["oauth_token_secret"])

        auth = OAuth1(consumer_key, consumer_secret,
                      oauth_token, oauth_token_secret)

        photoid = None
        if "flic" not in url and "/" not in url:
            photoid = url.strip()
        elif "flic.kr" in url:
            base58 = url.split("/")[-1]
            alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
            base_count = len(alphabet)
            photoid = 0
            multi = 1
            base58 = base58[::-1]
            for char in base58:
                photoid += multi * alphabet.index(char)
                multi = multi * base_count
        else:
            regex = re.compile(
                r'http(s)?\:\/\/www\.flickr\.com/photos/[^/]*/(?P<photoid>\d*)(/)?', re.S)
            matchObject = regex.match(url)

            if not matchObject:
                response = requests.get(url)
                matchObject = regex.match(response.url)
                if not matchObject:
                    if response.history:
                        for resp in response.history:
                            matchObject = regex.match(resp.url)
                            if matchObject:
                                break
            if not matchObject:
                self.log.error(
                    'cound not get flickr photoid from the URL, can\'t continue' % locals())
            else:
                photoid = matchObject.group("photoid")

        if not photoid:
            return "Could not get photoId"

        try:
            response = requests.get(
                url="https://api.flickr.com/services/rest/",
                params={
                    "method": "flickr.photos.getSizes",
                    "photo_id": photoid,
                    "format": "json",
                    "nojsoncallback": "1",
                },
                auth=auth,
            )
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        data = response.json()

        images = {}
        for image in data["sizes"]["size"]:
            images[image["width"]] = image["source"]
            if image["label"].lower() == "original":
                images["original"] = image["source"]

        try:
            response = requests.get(
                url="https://api.flickr.com/services/rest/",
                params={
                    "method": "flickr.photos.getInfo",
                    "photo_id": photoid,
                    "format": "json",
                    "nojsoncallback": "1",
                },
                auth=auth,
            )
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        data = response.json()
        title = data["photo"]["title"]["_content"]
        desc = data["photo"]["description"]["_content"]
        photoId = data["photo"]["id"]

        self.log.info('completed the ``get_photo_metadata`` method')
        return images, title, desc, photoId

    def md(
            self,
            url,
            width=1024):
        """*generate a multimarkdown image link viewable anywhere (no sign-in needed for private photos*

        **Key Arguments:**
            - ``url`` -- the share URL for the flickr image  (or just the unique photoid)
            - ``width`` -- the pixel width of the fully resolved image. Default *1024*. [75, 100, 150, 240, 320, 500, 640, 800, 1024, 1600, 2048]

        **Return:**
            - ``md`` -- the image reference link in multi-markdown syntax

        **Usage:**

            To return the markdown markup for an image at a given Flickr share URL:

            .. code-block:: python 

                from picaxe import picaxe
                Flickr = picaxe(
                    log=log,
                    settings=settings
                )
                mdLink = Flickr.md(
                    url="https://www.flickr.com/photos/92344916@N06/30455211086"
                    width=1024 
                )
        """
        self.log.info('starting the ``md_image`` method')

        images, title, desc, photoId = self.get_photo_metadata(url)

        if len(title) == 0:
            tag = photoId
        else:
            tag = "%(title)s %(photoId)s" % locals()

        image = images[str(width)]

        if width == "original":
            pxWidth = 1024
        else:
            pxWidth = width

        md = """![][%(tag)s]

[%(tag)s]: %(image)s title="%(title)s" width=600px
""" % locals()

        self.log.info('completed the ``md_image`` method')
        return md

    # use the tab-trigger below for new method
    # xt-class-method
