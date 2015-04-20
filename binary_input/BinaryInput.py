__author__ = 'pjp'

##############################
# Logical input to exit action
NO_OP   = 0
PARTIAL = 1
LEAD_IN = 2
REBOOT  = 9

LEAD_IN = [True, False, True, False]

class BinaryInput(object):
    def __init__(self):
        """

        :return:
        """
        self._state = NO_OP

    def input(self, value):
        """
        Given the input value, determine the current state
        :param value: True or False

        :return: the state after using the input value
        """
        return self._state


