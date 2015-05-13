import codecs
import configparser
import os.path
import pathlib
import re
import sys

from versionner import defaults


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

    def __repr__(self):
        return '<FileConfig(%s)>' % self.filename


class Config:
    """
    Configuration
    """

    __slots__ = 'version_file date_format files vcs_engine vcs_tag_params up_part default_init_version'.split()

    def __init__(self):
        """
        Evaluate configuration

        :return:
        """
        self.version_file = defaults.DEFAULT_VERSION_FILE
        self.date_format = defaults.DEFAULT_DATE_FORMAT
        self.default_init_version = defaults.DEFAULT_INIT_VERSION
        self.files = []
        self.vcs_engine = 'git'
        self.vcs_tag_params = []
        self.up_part = defaults.DEFAULT_UP_PART

        cfg_handler = configparser.ConfigParser(interpolation=None)

        cfg_files = [
            str(pathlib.Path(os.path.expanduser('~')) / defaults.RC_FILENAME),
            str(pathlib.Path() / defaults.RC_FILENAME)
        ]

        if not cfg_handler.read(cfg_files):
            return

        # global configuration
        if 'versionner' in cfg_handler:
            cfg = cfg_handler['versionner']
            if 'file' in cfg:
                self.version_file = cfg['file']
            if 'date_format' in cfg:
                self.date_format = cfg['date_format']
            if 'up_part' in cfg:
                self.up_part = cfg['up_part']
            if 'default_init_version' in cfg:
                self.default_init_version = cfg['default_init_version']

        if 'vcs' in cfg_handler:
            cfg = cfg_handler['vcs']
            if 'engine' in cfg:
                self.vcs_engine = cfg['engine']
            if 'tag_params' in cfg:
                self.vcs_tag_params = list(filter(None, cfg['tag_params'].split("\n")))

        # project files configuration
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

    def __repr__(self):
        ret = '<' + self.__class__.__name__ + ': '
        ret += ', '.join('%s=%r' % (name, getattr(self, name)) for name in self.__slots__)
        return ret
