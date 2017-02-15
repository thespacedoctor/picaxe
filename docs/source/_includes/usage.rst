Command-Line Usage
==================

.. code-block:: bash 
   
    
    Documentation for picaxe can be found here: http://picaxe.readthedocs.org/en/stable
    
    Usage:
        picaxe init
        picaxe auth [-s <pathToSettingsFile>]
        picaxe md <urlOrPhotoid> [<width>] [-s <pathToSettingsFile>]
        picaxe albums [-s <pathToSettingsFile>]
    
    Options:
        init                  setup the polygot settings file for the first time
        auth                  authenticate picaxe against your flickr account
        md                    generate the MD reference link for the image in the given flickr URL
        albums                list all the albums in the flickr account
    
        <pathToSettingsFile>  path to the picaxe settings file
        <urlOrPhotoid>        the flickr URL or photoid
        <width>               pixel width resolution of the linked image. Default *original*. [75|100|150|240|320|500|640|800|1024|1600|2048]
        
        -h, --help            show this help message
        -v, --version         show version
        -s, --settings        the settings file
    
