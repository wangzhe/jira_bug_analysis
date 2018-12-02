import logging


# update handler file to show handler execution
# add default local file
# attach NAS for reading account info (default.local file)
# NAS file write execution
# third party code (request)
from module.sys_invariant import get_system_user


def handler(event, context):
    # do_bug_analysis()
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info('update handler file to show handler execution - Done')
    getuser = get_system_user()
    logger.info('add default local file： ' + getuser)
    return 'hello world'

# handler(None, None)
