#!/usr/bin/env python3

import argparse
import codecs
import configparser
import os.path
import pathlib
import re
import shutil
import sys
import tempfile
import time

import semver

"""
Versionner tool.
"""

__version__ = '0.4.3'

RC_FILENAME = '.versionner.rc'
DEFAULT_VERSION_FILE = './VERSION'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_UP_PART = 'minor'


class Version:
    """
    Version of project.
    """

    VALID_FIELDS = ('major', 'minor', 'patch', 'prerelease', 'build')
    VALID_UP_FIELDS = ('major', 'minor', 'patch')

    def __init__(self, version_dict=None):
        """
        Initialise object

        :param version_dict:Version object (to clone) or dictionary from semver.parse
        """

        if isinstance(version_dict, Version):
            version_dict = {
                'major': version_dict.major,
                'minor': version_dict.minor,
                'patch': version_dict.patch,
                'prerelease': version_dict.prerelease,
                'build': version_dict.build,
            }

        self.major = version_dict['major']
        self.minor = version_dict['minor']
        self.patch = version_dict['patch']
        self.prerelease = version_dict.get('prerelease', '')
        self.build = version_dict.get('build', '')

    def up(self, type, value=None):
        """
        Increase version and return new instance

        :rtype : Version
        :param type:one of Version.VALID_UP_FIELDS
        :param value:int
        :return: :raise ValueError:
        """

        if type not in self.VALID_UP_FIELDS:
            raise ValueError("Incorrect value of \"type\"")

        if not value:
            value = 1

        version = Version(self)

        if type == 'major':
            version.major += value
            version.minor = 0
            version.patch = 0
        elif type == 'minor':
            version.minor += value
            version.patch = 0
        else:
            version.patch += value

        return version

    def set(self, type, value):
        """
        Set any field of semver to `value`

        :rtype : Version
        :param type:type of field (one of Version.VALID_FIELDS)
        :param value:
        :return: :raise ValueError:
        """

        if type not in self.VALID_FIELDS:
            raise ValueError("Incorrect value of \"type\"")

        version = Version(self)
        setattr(version, type, value)

        semver.parse(str(version))

        return version

    def __str__(self):
        """
        Return version as string compatible with semver

        :return:str
        """

        version = '.'.join([str(self.major), str(self.minor), str(self.patch)])
        if self.prerelease:
            version += '-' + str(self.prerelease)
        if self.build:
            version += '+' + str(self.build)

        return version


class VersionFile():
    """
    Main file with projects version
    """

    def __init__(self, path):
        """
        Initialisation

        :param path:pathlib.Path
        """
        self._path = path

    def read(self):
        """
        Read version from version file

        :rtype : Version
        :return:
        """
        with self._path.open(mode='r') as fh:
            version = fh.read().strip()
            version = semver.parse(version)
            return Version(version)

    def write(self, version):
        """
        Save new version into file

        :param version:Version
        """
        with self._path.open(mode='w') as fh:
            fh.write(str(version))

    def __str__(self):
        return str(self._path)


class FileConfig:
    """
    Single project file configuration
    """

    def __init__(self, filename, cfg):
        """
        Evaluate single file configuration

        :param filename:
        :param cfg:
        """
        self.filename = filename
        self.file = pathlib.Path(filename)
        self.enabled = cfg.getboolean('enabled', True)
        self.search = cfg['search']
        self.replace = cfg['replace']
        self.date_format = cfg.get('date_format', None)
        self.match = cfg.get('match', 'line')
        self.search_flags = 0
        self.encoding = cfg.get('encoding', 'utf-8')

        search_flags = cfg.get('search_flags', '')
        if search_flags:
            search_flags = re.split('\s*,\s*', search_flags)
            for search_flag in search_flags:
                self.search_flags |= getattr(re, search_flag.upper())

    def validate(self):
        """
        Validate current file configuration

        :raise ValueError:
        """
        if not self.file.exists():
            raise ValueError("File \"%s\" doesn't exists")

        if not self.search:
            raise ValueError("Search cannot be empty")

        if not self.replace:
            raise ValueError("Replace cannot be empty")

        if self.match not in ('file', 'line'):
            raise ValueError("Match must be one of: file, line")

        try:
            codecs.lookup(self.encoding)
        except LookupError:
            raise ValueError("Unknown encoding: \"%s\"" % self.encoding)


class Config:
    """
    Configuration
    """

    def __init__(self):
        """
        Evaluate configuration

        :return:
        """
        self.version_file = DEFAULT_VERSION_FILE
        self.date_format = DEFAULT_DATE_FORMAT
        self.files = []
        self.git_tag = False
        self.up_part = DEFAULT_UP_PART

        cfg_handler = configparser.ConfigParser(interpolation=None)

        cfg_files = [
            str(pathlib.Path(os.path.expanduser('~')) / RC_FILENAME),
            str(pathlib.Path() / RC_FILENAME)
        ]

        if not cfg_handler.read(cfg_files):
            return

        ## global configuration
        if 'versionner' in cfg_handler:
            cfg = cfg_handler['versionner']
            if 'file' in cfg:
                self.version_file = cfg['file']
            if 'date_format' in cfg:
                self.date_format = cfg['date_format']
            if 'git_tag' in cfg:
                self.git_tag = cfg['git_tag']
            if 'up_part' in cfg:
                self.up_part = cfg['up_part']

        ## project files configuration
        for section in cfg_handler.sections():
            if section.startswith('file:'):
                project_file = FileConfig(section[5:], cfg_handler[section])

                if not project_file.date_format:
                    project_file.date_format = self.date_format

                if project_file.enabled:
                    try:
                        project_file.validate()
                    except ValueError as ex:
                        print("Incorrect configuration for file \"%s\": %s" % (project_file.filename, ex.args[0]), file=sys.stderr)
                    else:
                        self.files.append(project_file)


def parse_args(args, **defaults):
    """
    Parse input arguments of script.

    :rtype : argparse.Namespace
    :param args:
    :return:
    """
    prog = pathlib.Path(sys.argv[0]).parts[-1].replace('.py', '')
    version = "%%(prog)s %s" % __version__
    p = argparse.ArgumentParser(prog=prog, description='Helps manipulating version of the project')
    p.add_argument('--file', '-f', dest='version_file', type=str,
        default=defaults.get('version_file'),
        help="path to file where version is saved")
    p.add_argument('--version', '-v', action="version", version=version)
    p.add_argument('--date-format', type=str,
        default=defaults.get('date_format'),
        help="Date format used in project files")
    # p.add_argument('--git', '-g', action="store_true", help="")

    sub = p.add_subparsers()

    p_init = sub.add_parser('init',
        help="Create new version file")
    p_init.add_argument('value', nargs='?', default='0.1.0', type=str,
        help="Initial version")

    p_up = sub.add_parser('up',
        help="Increase version")
    p_up.add_argument('value', nargs='?', type=int,
        help="Increase version by this value (default: 1)")

    p_up_gr = p_up.add_mutually_exclusive_group()
    up_part = defaults.get('up_part', defaults.get('up_part'))
    p_up_gr.add_argument('--major', '-j', action="store_true",
        help="increase major part of version" + (" (project default)" if up_part == 'major' else ""))
    p_up_gr.add_argument('--minor', '-n', action="store_true",
        help="increase minor part of version" + (" (project default)" if up_part == 'minor' else ""))
    p_up_gr.add_argument('--patch', '-p', action="store_true",
        help="increase patch part of version" + (" (project default)" if up_part == 'patch' else ""))

    p_set = sub.add_parser('set',
        help="Set version to specified one")
    p_set.add_argument('--major', '-j', type=int,
        help="set major part of version to MAJOR")
    p_set.add_argument('--minor', '-n', type=int,
        help="set minor part of version to MINOR")
    p_set.add_argument('--patch', '-p', type=int,
        help="set patch part of version to PATCH")
    p_set.add_argument('--prerelease', '-r', type=str,
        help="set prerelease part of version to PRERELEASE")
    p_set.add_argument('--build', '-b', type=str,
        help="set build part of version to BUILD")
    p_set.add_argument('value', nargs='?', type=str,
        help="set version to this value")

    args = p.parse_args(args)
    args.version_file = pathlib.Path(args.version_file).absolute()

    ## TODO: how can I do that better?
    if hasattr(args, 'build'):
        args.command = 'set'
        if not args.version_file.exists():
            p.error("Version file \"%s\" doesn't exists" % args.version_file)

    elif hasattr(args, 'major'):
        args.command = 'up'
        if not args.version_file.exists():
            p.error("Version file \"%s\" doesn't exists" % args.version_file)

    elif hasattr(args, 'value'):
        args.command = 'init'
        if args.version_file.exists():
            p.error("Version file \"%s\" already exists" % args.version_file)

    else:
        args.command = None

    return args


def update_project_files(args, cfg, version):
    """
    Update version string in project files

    :rtype : dict
    :param args:script arguments
    :param cfg:project configuration
    :param version:current version
    :return:dict :raise ValueError:
    """
    counters = {'files': 0, 'changes': 0}

    for project_file in cfg.files:
        if not project_file.file.exists():
            print("File \"%s\" not found" % project_file.filename, file=sys.stderr)
            continue

        ## prepare data
        date_format = project_file.date_format or args.date_format

        rxp = re.compile(project_file.search, project_file.search_flags)
        replace = project_file.replace % {
            "date": time.strftime(date_format),
            "major": version.major,
            "minor": version.minor,
            "patch": version.patch,
            "prerelease": version.prerelease,
            "version": str(version),
            "build": version.build,
        }

        ## update project files
        with \
                project_file.file.open(mode="r", encoding=project_file.encoding) as fh_in, \
                tempfile.NamedTemporaryFile(mode="w", encoding=project_file.encoding, delete=False) as fh_out:
            if project_file.match == 'line':
                changes = 0
                for line in fh_in:
                    (line, cnt) = rxp.subn(replace, line)
                    if cnt:
                        changes += cnt
                    fh_out.write(line)

                if changes:
                    counters['files'] += 1
                    counters['changes'] += changes

            elif project_file.match == 'file':
                data = fh_in.read()
                (data, cnt) = rxp.subn(replace, data)
                if cnt:
                    counters['files'] += 1
                    counters['changes'] += cnt
                fh_out.write(data)

            else:
                raise ValueError("Unknown match type: \"%s\"" % project_file.match)

            fh_out.close()

            shutil.copystat(project_file.filename, fh_out.name)
            pathlib.Path(fh_out.name).rename(project_file.filename)

    return counters


def main():
    """
    Main script

    :param args:
    :return:
    """

    project_cfg = Config()
    args = parse_args(sys.argv[1:], version_file=project_cfg.version_file, date_format=project_cfg.date_format,
        up_part=project_cfg.up_part)

    version_file = VersionFile(args.version_file)

    quant = None
    if args.command == 'up':
        current = version_file.read()

        if args.major:
            new = current.up('major', args.value)
        elif args.minor:
            new = current.up('minor', args.value)
        elif args.patch:
            new = current.up('patch', args.value)
        else:
            new = current.up(project_cfg.up_part, args.value)

        version_file.write(new)
        current = new

        quant = update_project_files(args, project_cfg, current)

    elif args.command == 'set':
        current = version_file.read()

        if args.value:
            parsed = semver.parse(args.value)
            new = Version(parsed)
        else:
            new = Version(current)
            for type_ in Version.VALID_FIELDS:
                value = getattr(args, type_)
                if value:
                    new = new.set(type_, value)

        version_file.write(new)
        current = new

        quant = update_project_files(args, project_cfg, current)

    elif args.command == 'init':
        parsed = semver.parse(args.value)
        current = Version(parsed)
        version_file.write(current)

    else:
        try:
            current = version_file.read()
        except FileNotFoundError:
            print('Version file not found', file=sys.stderr)
            sys.exit(1)

    print("Current version: %s" % current)
    if quant:
        print('Changed %(files)s files (%(changes)s changes)' % quant)


if __name__ == '__main__':
    main()
