versionner
==========

`versionner` helps manipulating version of the project.

With one command you can update all required files and git with new version.

Current stable version
----------------------

1.3.0

Features
--------

* `versionner` guards the compliance with [Semantic Versioning](http://semver.org/)
* manual changes are error-prone, `versionner` is error proof
* it's easier to write: `ver up` instead of open editor, edit and
    save changes ;)
* `versionner` updates also project files (like README or sth)
* and create vcs (only git currently) tag if requested
* it's [very easy to install](#installation)
* and it's all in one command...

Python version
--------------

`versionner` works only with Python 3.3+. Older versions are unsupported.

Some examples
-------------

Some examples:

    # initialize new file with version 0.1.0
    % ver init
    
    # initialize new file with version 1.0.0
    % ver init 1.0.0

    # prints current version info
    % ver
    
    # increase minor by 1, set patch to 0
    % ver up
    
    # increase patch by 1
    % ver up --patch
    
    # increase patch by 2 and try to automatically commit changes
    % ver up --patch -c
    
    # create git tag
    % ver tag
    
    # increase patch by 4
    % ver up --patch 4
     
    # just guess...
    % ver set --minor 3 --patch 2 --build asd3f
        
    # set version to 1.0.0
    % ver set 1.0.0
    
    # create signed VCS tag
    % ver tag --vcs-param -s

More
----

Everything is in help :) Just execute:

    ver --help

Look at result:

    % ver --help
    usage: ver [-h] [--file VERSION_FILE] [--version] [--date-format DATE_FORMAT]
               [--vcs-engine VCS_ENGINE] [--vcs-commit-message VCS_COMMIT_MESSAGE]
               [--verbose]
               {init,up,set,tag} ...
    
    Helps manipulating version of the project
    
    positional arguments:
      {init,up,set,tag}
        init                Create new version file
        up                  Increase version
        set                 Set version to specified one
        tag                 Create VCS tag with current version
    
    optional arguments:
      -h, --help            show this help message and exit
      --file VERSION_FILE, -f VERSION_FILE
                            path to file where version is saved
      --version, -v         show program's version number and exit
      --date-format DATE_FORMAT
                            Date format used in project files
      --vcs-engine VCS_ENGINE
                            Select VCS engine (only git is supported currently)
      --vcs-commit-message VCS_COMMIT_MESSAGE, -m VCS_COMMIT_MESSAGE
                            Commit message used when committing changes
      --verbose             Be more verbose if it's possible

      
So, there are four commands: `init`, `up`, `set` and `tag`. We want to look at this:

    usage: ver init [-h] [--commit] [value]
    
    positional arguments:
      value         Initial version
    
    optional arguments:
      -h, --help    show this help message and exit
      --commit, -c  Commit changes done by `up` command (only if there is no
                    changes in repo before)

    usage: ver up [-h] [--commit] [--major | --minor | --patch] [value]
    
    positional arguments:
      value         Increase version by this value (default: 1)
    
    optional arguments:
      -h, --help    show this help message and exit
      --commit, -c  Commit changes done by `up` command (only if there is no
                    changes in repo before)
      --major, -j   increase major part of version
      --minor, -n   increase minor part of version (project default)
      --patch, -p   increase patch part of version

    % ver set --help
    usage: ver set [-h] [--major MAJOR] [--minor MINOR] [--patch PATCH]
                   [--prerelease PRERELEASE] [--build BUILD] [--commit]
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
      --commit, -c          Commit changes done by `set` command (only if there is
                            no changes in repo before)
                            
    % ver tag --help
    usage: ver tag [-h] [--vcs-tag-param VCS_TAG_PARAMS]
    
    optional arguments:
      -h, --help            show this help message and exit
      --vcs-tag-param VCS_TAG_PARAMS
                            Additional params for VCS for "tag" command

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
    ;default_init_version = 1.0.0
    
    [vcs]
    engine = git
    commit_message = '%(version)s'
    ;tag_params =
    ;  -f
    ;  --local-user=some-key-id
    
    [file:some/folder/some_file.py]
    enabled = true
    search = ^\s*__version__\s*=.*$
    replace = __version__ = '%(version)s'
    date_format = %Y-%m-%d
    match = line
    search_flags = 
    encoding = utf-8
    
    [file:2:some/folder/some_file.py]
        enabled = true
        search = ^"Program is in version \d+\.\d+\.\d+"$
        replace = "Program is in version %(version)s"
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

When replacing values, there can be used some of placeholders:

    %(date)s: current date
    %(major)s: major part of version
    %(minor)s: minor part of version
    %(patch)s: patch part of version
    %(prerelease)s: prerelease part of version
    %(build)s: build part of version
    %(version)s: full version string

If you must do more replaces in single file, just add number to section name:

    [file:2:some/path]

Installation
------------

1. Using PIP

`versionner` should work on any platform where [Python](http://python.org)
is available, it means Linux, Windows, MacOS X etc. 

Simplest way is to use Python's built-in package system:

    pip3 install versionner

2. Using sources

Download sources from [Github](https://github.com/msztolcman/versionner/archive/1.3.0.zip):

    wget -O 1.3.0.zip https://github.com/msztolcman/versionner/archive/1.3.0.zip
    
or

    curl -o 1.3.0.zip https://github.com/msztolcman/versionner/archive/1.3.0.zip

Unpack:

    unzip 1.3.0.zip

And install

    cd versionner-1.3.0
    python3 setup.py install

Voila!

Authors
-------

Marcin Sztolcman <marcin@urzenia.net>

Contact
-------

If you like or dislike this software, please do not hesitate to tell me about
this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use GitHub's
[issues](https://github.com/msztolcman/versionner/issues).

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

### v1.3.0

* Allow to automatically commit changes done by commands: up, set, init
* Rewritten VCS subsystem, allows now for many engines

### v1.2.0

* Allow to make more then one replace in single file
* Do not show an exception when version file does not exists
* PEP8 fixes (coding style)
* Makefile improvements

### v1.1.1

* minor fixes

### v1.1.0

* refactored codebase from one file to one package with few files

### v1.0.7

* fights with enforcing Python3

### v1.0.6

* fights with enforcing Python3

### v1.0.5

* fights with enforcing Python3

### v1.0.4

* fights with enforcing Python3 

### v1.0.3

* many ways to tell to use Python3.3+ for versionner
* Makefile refinements

### v1.0.2

* README fixes
* Makefile

### v1.0.1

* nothing changed, just for PYPI

### v1.0.0

* added `tag` command (creates vcs (only git currently) tag)
* versionner's app now is called 'ver', 'versionner' is deprecated
* ability to set default value for `init` command in `.versionner.rc`

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
