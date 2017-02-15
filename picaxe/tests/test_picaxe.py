import os
import nose
import shutil
import yaml
from picaxe import picaxe, cl_utils
from picaxe.utKit import utKit
import unittest

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="picaxe"
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/picaxe/picaxe.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    shutil.copytree(pathToInputDir, pathToOutputDir)


testImage = pathToOutputDir + "/thespacedoctor_icon_dark_circle.png"

# xt-setup-unit-testing-files-and-folders


class test_picaxe(unittest.TestCase):

    # def test_picaxe_function(self):

    #     from picaxe import picaxe
    #     this = picaxe(
    #         log=log,
    #         settings=settings
    #     )
    #     oauth_token, oauth_token_secret = this.authenticate()
    #     print "oauth_token: ", oauth_token
    #     print "oauth_token_secret: ", oauth_token_secret

    def test_direct_image_function(self):

        from picaxe import picaxe
        this = picaxe(
            log=log,
            settings=settings
        )
        this.get_photo_metadata(
            url="https://www.flickr.com/photos/92344016@N06/30455210086")
        this.get_photo_metadata(
            url="https://www.flickr.com/gp/92344016@N06/093pa6")
        images, title, desc, photoId = this.get_photo_metadata(
            url="http://flic.kr/p/NpdUV5")

        print images.keys

    def test_md_image_function(self):

        from picaxe import picaxe
        photo = picaxe(
            log=log,
            settings=settings
        )
        mdLink = photo.md(
            url="https://www.flickr.com/photos/92344016@N06/30455210086")
        print mdLink
        mdLink = photo.md(
            url="https://www.flickr.com/gp/92344016@N06/093pa6")
        print mdLink
        mdLink = photo.md(url="http://flic.kr/p/NpdUV5")
        print mdLink
        # https://c7.staticflickr.com/6/5493/30455210086_6685d6eb13_k.jpg
        # <a data-flickr-embed="true"  href="https://www.flickr.com/gp/92344016@N06/pxQ3y1" title="Lion face"><img src="https://c7.staticflickr.com/6/5493/30455210086_6685d6eb13_k.jpg" width="2048" height="1356" alt="Lion face"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

    def test_upload_local_image(self):

        from picaxe import picaxe
        photo = picaxe(
            log=log,
            settings=settings
        )
        photo.upload(
            imagePath=testImage,
            private=True,
            title="delete me",
            tags="nice, photo",
            description="this is thespacedoctor icon"
        )
        photo.upload(
            imagePath=testImage,
            private=False,
            title="delete me again",
            tags="crap, photo",
            description="this is thespacedoctor icon again"
        )

    def test_list_album_titles(self):

        from picaxe import picaxe
        flickr = picaxe(
            log=log,
            settings=settings
        )
        albumList = flickr.list_album_titles()
        print albumList

    def test_picaxe_function_exception(self):

        from picaxe import picaxe
        try:
            this = picaxe(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
