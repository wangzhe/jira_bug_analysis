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
    smtp_host = account_config_test()
    logger.info("reading account info (default.local file) - Done")
    logger.info("NAS file write execution")

    return smtp_host


def account_config_test():
    config = configparser.ConfigParser()
    config.read(config_path + 'default.local')
    smtp_host = config['EMAIL']['SMTP_HOST']
    return smtp_host


print(handler(None, None))
