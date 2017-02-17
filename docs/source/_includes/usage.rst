Command-Line Usage
==================

.. code-block:: bash 
   
    
    Documentation for picaxe can be found here: http://picaxe.readthedocs.org/en/stable
    
    Usage:
        picaxe init
        picaxe auth [-s <pathToSettingsFile>]
        picaxe md <urlOrPhotoid> [<width>] [-s <pathToSettingsFile>]
        picaxe albums [-s <pathToSettingsFile>]
        picaxe [-giop] upload <imagePath> [--title=<title> --tags=<tags> --desc=<desc> --album=<album>]
    
    Options:
        init                  setup the polygot settings file for the first time
        auth                  authenticate picaxe against your flickr account
        md                    generate the MD reference link for the image in the given flickr URL
        albums                list all the albums in the flickr account
        upload                upload a local image to flickr
    
        <pathToSettingsFile>  path to the picaxe settings file
        <urlOrPhotoid>        the flickr URL or photoid
        <width>               pixel width resolution of the linked image. Default *original*. [75|100|150|240|320|500|640|800|1024|1600|2048]
        <imagePath>           path to the local image to upload to flickr
    
        --title=<title>       the image title
        --tags=<tags>         quoted, comma-sepatated tags
        --desc=<desc>         image description
        
        -p, --public          make the image public (private by default)
        -o, --open            open the image in the flickr web-app once uploaded
        -i, --image           "photo" is an image
        -g, --screenGrab      "photo" is a screengrab
        -h, --help            show this help message
        -v, --version         show version
        -s, --settings        the settings file
    
