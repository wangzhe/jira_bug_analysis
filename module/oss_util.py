import configparser
import getpass

import oss2

from module.sys_invariant import config_path


class OSSInfo:
    class __OSSInfo:
        def __init__(self, arg):
            config = configparser.ConfigParser()
            try:
                config.read(config_path + arg + '.local')
                self.endpoint = config['OSS']['OSS_ENDPOINT']
            except KeyError as e:
                config.read(config_path + 'default.local')
                self.endpoint = config['OSS']['OSS_ENDPOINT']
            self.bucket = config['OSS']['OSS_BUCKET']
            self.keyid = config['OSS']['KeyId']
            self.secret = config['OSS']['KeySecret']
            self.debug_mode = config['OSS'].getboolean('DEBUG_MODE')

        def is_debug(self):
            return self.debug_mode

    instance = None

    def __init__(self):
        if not OSSInfo.instance:
            OSSInfo.instance = OSSInfo.__OSSInfo(getpass.getuser())

    def __getattr__(self, name):
        return getattr(self.instance, name)


# test oss by id - done
# test read and write file
# test the real file read and write
# run from all_test.py to local file;
# run from main.py to local file;
# run from index to oss
def check_oss():
    oss_info = OSSInfo()
    auth = oss2.Auth(oss_info.keyid, oss_info.secret)
    bucket = oss2.Bucket(auth, oss_info.endpoint, oss_info.bucket)
    object_name = 'sprint_bug_summary.json'
    object_str = bucket.get_object(object_name).read()
    return object_str.decode('utf-8')
