import configparser
import logging


# update handler file to show handler execution
# add default local file
# attach NAS for reading account info (default.local file)
# NAS file write execution
# third party code (request)
from module.sys_invariant import get_system_user, config_path


def handler(event, context):
    # do_bug_analysis()
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info('update handler file to show handler execution - Done')
    logger.info('add default local file： ' + get_system_user() + " - Done")
    logger.info("reading account info (default.local file)")

    config = configparser.ConfigParser()
    config.read(config_path + 'default.local')
    smtp_host = config['EMAIL']['SMTP_HOST']
    return smtp_host


print(handler(None, None))
