#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path
from datetime import datetime
from loguru import logger as log
from warnings import filterwarnings
from orbit_component_base.src.orbit_shared import world
from platform import system


class OrbitConfig:

    BASE_authentication = 'secure'

    @property
    def path (self):            return Path(self._conf.get('BASE', 'path')).expanduser()

    @property
    def code (self):            return Path(self._conf.get('BASE', 'code')).expanduser()

    @property
    def namespace (self):       return self._conf.get('BASE', 'namespace')

    @property
    def authentication (self):  return self._conf.get('BASE', 'authentication')

    @property
    def name (self):            return self._conf.get('SSL', 'name')

    @property
    def ssl (self):             return self.mkpath('SSL', 'ssl')

    @property
    def secure (self):          return self._conf.getboolean('SSL', 'secure')
    
    @property
    def host (self):            return self._conf.get('NETWORK', 'host')

    @property
    def port (self):            return self._conf.getint('NETWORK', 'port')

    @property
    def local_port (self):      return self._conf.getint('NETWORK', 'local_port')

    @property
    def sio_debug (self):       return self._conf.getboolean('NETWORK', 'sio_debug')

    @property
    def engineio_debug (self):  return self._conf.getboolean('NETWORK', 'engineio_debug')

    @property
    def vite_port (self):       return self._conf.getint('DEV', 'vite_port')

    @property
    def make_keys (self):       return self.mkcode('TOOLS', 'make_keys')

    @property
    def database (self):        return self.mkpath('DATA', 'database')

    @property
    def tmp (self):             return self.mkpath('DATA', 'tmp')

    @property
    def templates (self):       return self.mkcode('DATA', 'templates')
    
    @property
    def web (self):             return self.mkcode('DATA', 'web')

    @property
    def logs (self):             return self.mkpath('DATA', 'logs')

    @property
    def writemap (self):        return self._conf.get('DATA', 'writemap')

    def __init__ (self, application):
        self._appl = application
        self._path = Path('~/.local/' + application).expanduser()
        self._file = (self._path / 'config.ini').expanduser()
        self._conf = None
        self._changed = False

    def setup_logging (self):
        try:
            level = log.level('RPC')
        except ValueError:
            log.level('RPC', no=10, color="<magenta>", icon='🗒️')
        if world.args and not world.args.dev:
            log.remove()
            Path(self.logs).mkdir(exist_ok=True)
            log.add((self.logs / 'orbit_access.log').as_posix(), level='RPC', colorize=True, rotation="10 MB", retention="3 days",
                filter=lambda record: record['name'] == 'src.orbit_decorators', enqueue=True)
            log.add((self.logs / 'orbit_system.log').as_posix(), colorize=True, rotation="10 MB", retention="3 days",
                filter=lambda record: record['name'] != 'src.orbit_decorators', enqueue=True)

    def _option (self, section, name, value):
        if not self._conf.has_option(section, name):
            self._conf.set(section, name, value)
            self._changed = True

    def mkpath (self, section, option):
        return self.mk(section, option, self.path)
    
    def mkcode (self, section, option):
        return self.mk(section, option, self.code)

    def mk (self, section, option, path):
        value = self._conf.get(section, option)
        if not value:
            return None
        if value[0] in './~':
            p = Path(self._conf.get(section, option)).expanduser()
        else:
            p = path / self._conf.get(section, option)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def open (self):
        self._path.mkdir(parents=True, exist_ok=True)
        self._conf = ConfigParser()
        self._conf.read(self._file.as_posix())
        for section in ['BASE', 'NETWORK', 'TOOLS', 'DATA', 'SSL', 'DEV']:
            if section not in self._conf.sections():
                self._conf.add_section(section)
                self._changed = True
        code_path = f'/Applications/{self._appl}.app/Contents/Resources/' if system() == 'Darwin' else f'/opt/{self._appl}'
        self._option('BASE', 'path', f'~/.local/{self._appl}')
        self._option('BASE', 'code', code_path)
        self._option('BASE', 'namespace', '/orb')
        self._option('BASE', 'authentication', self.BASE_authentication)
        self._option('SSL', 'name', 'localhost')
        self._option('SSL', 'ssl', 'ssl')
        self._option('SSL', 'secure', 'true')
        self._option('NETWORK', 'host', '127.0.0.1')
        self._option('NETWORK', 'port', '8445')
        self._option('NETWORK', 'local_port', '8445')
        self._option('DEV', 'vite_port', '3000')
        self._option('NETWORK', 'sio_debug', 'false')
        self._option('NETWORK', 'engineio_debug', 'false')
        self._option('TOOLS', 'make_keys', 'scripts/make_keys.sh')
        self._option('DATA', 'database', 'orbit_database')
        self._option('DATA', 'tmp', 'tmp')
        self._option('DATA', 'templates', 'templates')
        self._option('DATA', 'web', 'web')
        self._option('DATA', 'logs', 'logs')
        self._option('DATA', 'writemap', 'true')        
        if self._changed:
            with open(self._file.as_posix(), 'w') as configfile:
                self._conf.set('DEFAULT', 'updated', datetime.now().isoformat())
                self._conf.write(configfile)
        self.setup_logging()                
        return self


if __name__ == '__main__':
    conf = OrbitConfig('Demo').open()
    print("Path           =", conf.path)
    print("Code           =", conf.code)
    print("Name           =", conf.name)
    print("SSL            =", conf.ssl)
    print("Host           =", conf.host)
    print("Port           =", conf.port)
    print("Local Port     =", conf.local_port)
    print("sio_debug      =", conf.sio_debug)
    print("engineio_debug =", conf.engineio_debug)
    print("make_keys      =", conf.make_keys)
    print("database       =", conf.database)
    print("templates      =", conf.templates)
    print("web            =", conf.web)
