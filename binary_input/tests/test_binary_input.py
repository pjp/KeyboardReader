__author__ = 'pjp'
import unittest as ut
import logging
import logging.config
import os

file = __file__      # absolute reference to this source
this_dir = os.path.dirname(file) # the directory this source lives in
config_file = this_dir + '/logging.ini' # Reference to the logging config. file

msg = ""

try:
    logging.config.fileConfig(config_file, disable_existing_loggers = False)
    msg  =   "Using logging config. file [" + config_file +"]"
except:
    msg =   "Cannot find logging config. file [" + config_file +"], defaulting to DEBUG level to stdout"
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("BinaryInputs.tests.TestInputs")

logger.debug(msg)

######################

class BinaryInputs(ut.TestCase):

    def test_init(self):
        pass
