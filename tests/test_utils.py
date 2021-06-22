from rain_alert.utils import RECEIVERS_FILE_PATH
import unittest

from .context import utils

import os


class TestGetReceivers(unittest.TestCase):
    def test_no_file(self):
        # set the path of the receivers to this folder because in tests folder 
        # we dont have the receivers file
        utils.RECEIVERS_FILE_PATH = os.path.split(utils.RECEIVERS_FILE_PATH)[-1]
        receivers = utils.get_receivers()
        self.assertEqual(receivers, None)

"""
class TestGetCredentials(unittest.TestCase):
    ...
"""

if __name__ == '__main__':
    unittest.main()
