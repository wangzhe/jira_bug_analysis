import logging

from bug_analysis import do_bug_analysis
from module.sys_invariant import get_system_user


# update handler file to show handler execution
# add default local file
# attach NAS for reading account info (default.local file)
# NAS file write execution
# third party code (request)


def handler(event, context):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info('update handler file to show handler execution - Done')
    logger.info('add default local file： ' + get_system_user() + " - Done")
    do_bug_analysis()
    return "Hello World"
