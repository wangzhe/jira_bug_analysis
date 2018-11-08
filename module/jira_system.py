import configparser
import getpass

from module.sys_invariant import config_path


class JiraInfo:
    class __JiraInfo:
        def __init__(self, arg):
            config = configparser.ConfigParser()
            config.read(config_path + arg + '.local')
            self.host = config['ACCOUNT']['INSTANCE_HOST']
            self.user = config['ACCOUNT']['A_USER']
            self.token = config['ACCOUNT']['A_TOKEN']
            self.debug_mode = config['ACCOUNT'].getboolean('DEBUG_MODE')

        #
        # def __str__(self):
        #     return repr(self) + self.val

        def is_debug(self):
            return self.debug_mode

    instance = None

    def __init__(self):
        if not JiraInfo.instance:
            JiraInfo.instance = JiraInfo.__JiraInfo(getpass.getuser())
        else:
            JiraInfo.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
