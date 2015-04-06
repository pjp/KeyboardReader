__author__ = 'pjp'
# test_basic.py
import unittest as ut
import logging
import logging.config
import os

import skid_steering.InputHandler as IH

######################
# Initalize the logger
######################
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

logger = logging.getLogger("SkidSteering.tests.TestInputs")

logger.debug(msg)

######################

class TestInputs(ut.TestCase):


    def test_init(self):
        ih = IH.InputHandler(0, 100, 20)

        self.assertTrue(ih)
        self.assertFalse(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_bad_constructor_values(self):
        try:
            IH.InputHandler(0, 0, 0)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

        try:
            IH.InputHandler(0, 1, 0)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

        try:
            IH.InputHandler(1, 0, 0)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

        try:
            IH.InputHandler(0, 1, -1)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

        try:
            IH.InputHandler(0, 1, 2)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")


    def test_bad_input(self):
        ih = IH.InputHandler(0, 100, 20)

        try:
            ih.move(999)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

    def test_initial_state(self):
        ih = IH.InputHandler(0, 100, 20)

        ih.move(IH.STOP)
        self.assertTrue(ih._is_stopped())
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())
        self.assertFalse(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_back(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_back_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward_boundary_check_2(self):
        ih = IH.InputHandler(0, 29, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_back_boundary_check_2(self):
        ih = IH.InputHandler(0, 29, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward_boundary_check_3(self):
        ih = IH.InputHandler(0, 31, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_back_boundary_check_3(self):
        ih = IH.InputHandler(0, 31, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_move_forward_back(self):
        ih = IH.InputHandler(0, 25, 10)

        ########################
        # two forward, one back
        ih.move(IH.FORWARD)
        ih.move(IH.FORWARD)
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.BACK)

        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ########################
        # two back
        ih.move(IH.BACK)
        ih.move(IH.BACK)
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ########################
        # four forward
        ih.move(IH.FORWARD)
        self.assertFalse(ih._is_moving())
        self.assertFalse(ih._is_turning())

        ih.move(IH.FORWARD)
        ih.move(IH.FORWARD)
        ih.move(IH.FORWARD)
        self.assertFalse(ih._is_turning())

        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())
        self.assertTrue(ih._is_moving())
        self.assertFalse(ih._is_turning())

    def test_spin_left(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

    def test_spin_left_then_straight_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

        ih.move(IH.FORWARD)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        self.assertFalse(ih._is_spinning())

    def test_spin_left_then_straight_back(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

        ih.move(IH.BACK)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        self.assertFalse(ih._is_spinning())

    def test_turn_forward_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_turn_forward_left_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_turn_forward_left_then_straight_back(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.BACK)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_turn_back_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_turn_back_left_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_turn_back_left_then_straight_forward(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.FORWARD)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_spin_right(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.RIGHT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

    def test_spin_right_then_straight_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.RIGHT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

        ih.move(IH.FORWARD)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        self.assertFalse(ih._is_spinning())

    def test_spin_right_then_straight_back(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.RIGHT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        self.assertTrue(ih._is_spinning())

        ih.move(IH.BACK)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        self.assertFalse(ih._is_spinning())

    def test_turn_forward_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

    def test_turn_forward_right_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_turn_forward_right_then_straight_back(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.BACK)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_turn_back_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

    def test_turn_back_right_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_turn_back_right_then_straight_forward(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.FORWARD)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_spin_left_right(self):
        ih = IH.InputHandler(0, 25, 10)

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
        self.assertTrue(ih._is_spinning())

        ih.move(IH.LEFT)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())

        self.assertFalse(ih._is_spinning())


    def test_stop(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())
        self.assertTrue(ih._is_moving())

        ih.move(IH.STOP)
        self.assertEqual(0, ih.left_motor_value())
        self.assertEqual(0, ih.right_motor_value())
        self.assertTrue(ih._is_stopped())

    #############################################################
    #
    #############################################################
    def test_max_forward_then_turn_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        ih.move(IH.FORWARD)

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_max_forward_then_turn_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        ih.move(IH.FORWARD)

        ih.move(IH.FORWARD)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

    def test_min_forward_then_turn_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(30, ih.right_motor_value())

    def test_min_forward_then_turn_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.FORWARD)
        self.assertEqual(10, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(20, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(30, ih.left_motor_value())
        self.assertEqual(10, ih.right_motor_value())

    #############################################################
    #
    #############################################################
    def test_max_back_then_turn_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        ih.move(IH.BACK)

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_max_back_then_turn_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        ih.move(IH.BACK)

        ih.move(IH.BACK)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

    def test_min_back_then_turn_left(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-20, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

        ih.move(IH.LEFT)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-30, ih.right_motor_value())

    def test_min_back_then_turn_right(self):
        ih = IH.InputHandler(0, 35, 10)

        ih.move(IH.BACK)
        self.assertEqual(-10, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-20, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())

        ih.move(IH.RIGHT)
        self.assertEqual(-30, ih.left_motor_value())
        self.assertEqual(-10, ih.right_motor_value())
