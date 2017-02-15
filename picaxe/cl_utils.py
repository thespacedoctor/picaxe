#!/usr/local/bin/python
# encoding: utf-8
"""
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
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from fundamentals import tools, times
# from ..__init__ import *


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="DEBUG",
        options_first=False,
        projectName="picaxe"
    )
    arguments, settings, log, dbConn = su.setup()

    startTime = times.get_now_sql_datetime()

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    if init:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/picaxe/picaxe.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass

    if auth:
        from picaxe import picaxe
        client = picaxe(
            log=log,
            settings=settings,
            pathToSettingsFile=pathToSettingsFile
        )
        client.authenticate()

    if md:
        from picaxe import picaxe
        Flickr = picaxe(
            log=log,
            settings=settings
        )
        if not width:
            width = "original"
        mdLink = Flickr.md(
            url=urlOrPhotoid,
            # [75, 100, 150, 240, 320, 500, 640, 800, 1024, 1600, 2048]
            width=width
        )
        print mdLink

    if albums:
        from picaxe import picaxe
        flickr = picaxe(
            log=log,
            settings=settings
        )
        albumList = flickr.list_album_titles()
        for a in albumList:
            print a

    # CALL FUNCTIONS/OBJECTS

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()
