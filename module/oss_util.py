import configparser
import getpass

import oss2
from oss2.exceptions import OssError

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
            self.bucket_name = config['OSS']['OSS_BUCKET']
            self.keyid = config['OSS']['KeyId']
            self.secret = config['OSS']['KeySecret']
            self.debug_mode = config['OSS'].getboolean('DEBUG_MODE')
            self.bucket = self.auth_oss()

        def is_debug(self):
            return self.debug_mode

        def auth_oss(self):
            auth = oss2.Auth(self.keyid, self.secret)
            bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
            return bucket

    instance = None

    def __init__(self):
        if not OSSInfo.instance:
            OSSInfo.instance = OSSInfo.__OSSInfo(getpass.getuser())

    def __getattr__(self, name):
        return getattr(self.instance, name)


# test oss by id - done
# test read - done
# test write file
# test the real file read and write
# run from all_test.py to local file;
# run from main.py to local file;
# run from index to oss
def read_file_in_oss(filename):
    print("reading to oss")
    bucket = OSSInfo().instance.bucket
    if bucket.object_exists(filename):
        binary_content = bucket.get_object(filename).read()
        return binary_content.decode('utf-8')
    return ""


def save_file_in_oss(filename, str_content):
    print("uploading to oss")
    bucket = OSSInfo().instance.bucket
    if bucket.object_exists(filename):
        bucket.delete_object(filename)
    bucket.put_object(filename, str_content)


def copy_file(source_name, target_name):
    print("copying file in oss from " + source_name + " to " + target_name)
    bucket = OSSInfo().instance.bucket
    if not bucket.object_exists(source_name):
        return False
    if bucket.object_exists(target_name):
        delete_file(target_name)
    bucket.copy_object(bucket.get_bucket_info().name, source_name, target_name)
    return True


def delete_file(filename):
    bucket = OSSInfo().instance.bucket
    try:
        if bucket.object_exists(filename):
            bucket.delete_object(filename)
    except OssError:
        print("delete error")
        return False
    return True
