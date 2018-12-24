import configparser
import getpass

from module.sys_invariant import config_path


class JiraInfo:
    class __JiraInfo:
        def __init__(self, arg):
            config = configparser.ConfigParser()
            try:
                config.read(config_path + arg + '.local')
                self.host = config['JIRA']['INSTANCE_HOST']
            except KeyError as e:
                config.read(config_path + 'default.local')
                self.host = config['JIRA']['INSTANCE_HOST']
            self.user = config['JIRA']['A_USER']
            self.token = config['JIRA']['A_TOKEN']
            self.debug_mode = config['JIRA'].getboolean('DEBUG_MODE')

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
