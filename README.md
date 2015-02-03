versionner
==========

`versionner` helps manipulating version of the project.

With one command you can update all required files with new version.

Current stable version
----------------------

0.4.3

Features
--------

* `versionner` guards the compliance with [Semantic Versioning](http://semver.org/)
* manual changes are error-prone, `versionner` is error proof
* it's easier to write: `versionner up` instead of open editor, edit and
    save changes ;)
* `versionner` updates also project files (like README or sth)
* it's [very easy to install](#installation)

Some examples
-------------

Some examples:

    # prints current version info
    % versionner
    
    # increase minor by 1, set patch to 0
    versionner up
    
    # increase patch by 1
    versionner up --patch 
    
    # increase patch by 4
    versionner up --patch 4
     
    # just guess...
    versionner set --minor 3 --patch 2 --build asd3f
        
    # set version to 1.0.0
    versionner set 1.0.0

More
----

Everything is in help :) Just execute:

    versionner --help

Look at result:

    % versionner --help
    usage: versionner [-h] [--file VERSION_FILE] [--version]
                      [--date-format DATE_FORMAT]
                      {init,up,set} ...
    
    Manipulate version of project
    
    positional arguments:
      {init,up,set}
        init                Create new version file
        up                  Increase version
        set                 Set version to specified one
    
    optional arguments:
      -h, --help            show this help message and exit
      --file VERSION_FILE, -f VERSION_FILE
                            path to file where version is saved
      --version, -v         show program's version number and exit
      --date-format DATE_FORMAT
                            Date format used in project files
      
So, there are three commands: `init`, `up` and `set`. We want to look at this:

    % versionner init --help
    usage: versionner init [-h] [value]
    
    positional arguments:
      value       Initial version
    
    optional arguments:
      -h, --help  show this help message and exit

    % versionner up --help
    usage: versionner up [-h] [--major | --minor | --patch] [value]
    
    positional arguments:
      value        Increase version by this value (default: 1)
    
    optional arguments:
      -h, --help   show this help message and exit
      --major, -j  increase major part of version
      --minor, -n  increase minor part of version (default)
      --patch, -p  increase patch part of version

    % versionner set --help
    usage: versionner set [-h] [--major MAJOR] [--minor MINOR] [--patch PATCH]
                          [--prerelease PRERELEASE] [--build BUILD]
                          [value]
    
    positional arguments:
      value                 set version to this value
    
    optional arguments:
      -h, --help            show this help message and exit
      --major MAJOR, -j MAJOR
                            set major part of version to MAJOR
      --minor MINOR, -n MINOR
                            set minor part of version to MINOR
      --patch PATCH, -p PATCH
                            set patch part of version to PATCH
      --prerelease PRERELEASE, -r PRERELEASE
                            set prerelease part of version to PRERELEASE
      --build BUILD, -b BUILD
                            set build part of version to BUILD

Configuration
---------------------

Configuration is both: user-wide and project-wide.

User-wide is stored in `~/.versionner.rc` file, and project-wide is stored in
`<PROJECT_ROOT>/.versionner.rc`. Projects' configuration is superior to user-wide.

It allows you also to modify other files specified in configuration.

`.versionner.rc` is INI file in format:

    [versionner]
    file = ./VERSION
    date_format = %Y-%m-%d
    up_part = patch
    
    [file:some/folder/some_file.py]
    enabled = true
    search = ^\s*__version__\s*=.*$
    replace = __version__ = '%(version)s'
    date_format = %Y-%m-%d
    match = line
    search_flags = 
    encoding = utf-8

Data in '[project]' section are default data for whole project.

Data in '[file:some/folder/some_file.py]' section are for single file from
project. You can specify here that file 'some/folder/some_file.py' have
version string (key: `enabled`), has encoding `encoding` and we have to
search for it (`search`) and replace it with value of `replace`. If `match` is
'line', then `search` is matched line by line, and for 'file' whole file is
read into memory and matched against `search`.

Installation
------------

`versionner` should work on any platform where [Python](http://python.org)
is available, it means Linux, Windows, MacOS X etc. 

Simplest way is to use Python's built-in package system:

    pip install versionner

In other case, you can go also to [GitHub releases](https://github.com/mysz/versionner/releases),
download newest release, unpack and put somewhere in `PATH` (ie. `~/bin`
or `/usr/local/bin`).

If You want to install newest unstable version, then just copy file to your
PATH, for example:

    curl https://raw.github.com/mysz/versionner/master/versionner.py > /usr/local/bin/versionner

or:

    wget https://raw.github.com/mysz/versionner/master/versionner.py -O /usr/local/bin/versionner

Voila!

Authors
-------

Marcin Sztolcman <marcin@urzenia.net>

Contact
-------

If you like or dislike this software, please do not hesitate to tell me about
this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use GitHub's
[issues](https://github.com/mysz/versionner/issues).

License
-------

The MIT License (MIT)

Copyright (c) 2015 Marcin Sztolcman

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

ChangeLog
---------

### v0.4.3

* do not fail when VERSION file is missing
* automatically use python3 (shebang)
* updated program description in help

### v0.4.2

* published on pypi

### v0.4.1

* copy file permissions to new one when updating project files

### v0.4.0

* first public version
