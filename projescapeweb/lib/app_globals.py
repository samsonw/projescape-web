"""The application's Globals object"""

import smtplib
import redis

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        self.url_root = config['projescape.root']
        self.__init_smtp(config)
        self.__init_redis(config)

    def __init_smtp(self, config):
        host = config['smtp.host']
        port = config['smtp.port']
        ssl = config['smtp.ssl']
        auth = config['smtp.auth']
        user = config['smtp.user']
        passwd = config['smtp.pass']

        if not ssl:
            self.smtp = smtplib.SMTP(host, port)
        else:
            self.smtp = smtplib.SMTP_SSL(host, port)

        if auth:
            self.smtp.login(user, passwd)

    def __init_redis(self, config):
        host = config['redis.host']
        port = int(config['redis.port'])
        passwd = config['redis.passwd'] if 'redis.passwd' in config else None

        self.redis = redis.Redis(host=host, port=port, password=passwd)

