picaxe
======

[![Documentation Status](https://readthedocs.org/projects/picaxe/badge/)](http://picaxe.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.rawgit.com/thespacedoctor/picaxe/master/coverage.svg)](https://cdn.rawgit.com/thespacedoctor/picaxe/master/htmlcov/index.html)

*A python package and command-line tools for work with the Flickr API to
upload images, sort images, generate MD image reference links etc*.

Here's a summary of what's included in the python package:

Command-Line Usage
==================

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

Documentation
=============

Documentation for picaxe is hosted by [Read the
Docs](http://picaxe.readthedocs.org/en/stable/) (last [stable
version](http://picaxe.readthedocs.org/en/stable/) and [latest
version](http://picaxe.readthedocs.org/en/latest/)).

Installation
============

The easiest way to install picaxe is to use `pip`:

    pip install picaxe

Or you can clone the [github
repo](https://github.com/thespacedoctor/picaxe) and install from a local
version of the code:

    git clone git@github.com:thespacedoctor/picaxe.git
    cd picaxe
    python setup.py install

To upgrade to the latest version of picaxe use the command:

    pip install picaxe --upgrade

Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

    git clone git@github.com:thespacedoctor/picaxe.git
    cd picaxe
    python setup.py develop

[Pull requests](https://github.com/thespacedoctor/picaxe/pulls) are
welcomed!

### Sublime Snippets

If you use [Sublime Text](https://www.sublimetext.com/) as your code
editor, and you're planning to develop your own python code with picaxe,
you might find [my Sublime
Snippets](https://github.com/thespacedoctor/picaxe-Sublime-Snippets)
useful.

Issues
------

Please report any issues
[here](https://github.com/thespacedoctor/picaxe/issues).

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
