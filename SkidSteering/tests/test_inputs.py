__author__ = 'pjp'
# test_basic.py
import unittest as ut
import logging
import logging.config
import os, sys

import SkidSteering.InputHandler as IH

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
        self.assertFalse(ih.isMoving())
        self.assertFalse(ih.isTurning())

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
            ih.getMotorValues(999)
        except Exception:
            pass
        else:
            self.fail("Should have thrown an exception")

    def test_initial_state(self):
        ih = IH.InputHandler(0, 100, 20)

        stop = ih.getMotorValues(IH.STOP)
        self.assertTrue(stop)
        self.assertEqual(0, stop[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, stop[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertFalse(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse_boundary_check(self):
        ih = IH.InputHandler(0, 30, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_boundary_check_2(self):
        ih = IH.InputHandler(0, 29, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse_boundary_check_2(self):
        ih = IH.InputHandler(0, 29, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_boundary_check_3(self):
        ih = IH.InputHandler(0, 31, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_reverse_boundary_check_3(self):
        ih = IH.InputHandler(0, 31, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_move_forward_reverse(self):
        ih = IH.InputHandler(0, 25, 10)

        ########################
        # two forward, one back
        ih.getMotorValues(IH.FORWARD)
        ih.getMotorValues(IH.FORWARD)
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.REVERSE)

        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        ########################
        # two back
        ih.getMotorValues(IH.REVERSE)
        ih.getMotorValues(IH.REVERSE)
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.NOOP)

        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

        ########################
        # four forward
        ih.getMotorValues(IH.FORWARD)
        self.assertFalse(ih.isMoving())
        self.assertFalse(ih.isTurning())

        ih.getMotorValues(IH.FORWARD)
        ih.getMotorValues(IH.FORWARD)
        ih.getMotorValues(IH.FORWARD)
        self.assertFalse(ih.isTurning())

        values = ih.getMotorValues(IH.NOOP)

        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())
        self.assertFalse(ih.isTurning())

    def test_spin_left(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

    def test_spin_left_then_straight_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertFalse(ih.isSpinning())

    def test_spin_left_then_straight_back(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertFalse(ih.isSpinning())

    def test_turn_forward_left(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_forward_left_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_forward_left_then_straight_back(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_left(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_left_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_left_then_straight_forward(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_spin_right(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

    def test_spin_right_then_straight_forward(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertFalse(ih.isSpinning())

    def test_spin_right_then_straight_back(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertTrue(ih.isSpinning())

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertFalse(ih.isSpinning())

    def test_turn_forward_right(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_forward_right_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_forward_right_then_straight_back(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_right(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_right_then_straight(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_turn_reverse_right_then_straight_forward(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.REVERSE)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(-30, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-30, values[IH.RIGHT_MOTOR_VALUE_INDEX])

    def test_spin_left_right(self):
        ih = IH.InputHandler(0, 25, 10)

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(-10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-20, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(-10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isSpinning())

        values = ih.getMotorValues(IH.LEFT)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        self.assertFalse(ih.isSpinning())


    def test_stop(self):
        ih = IH.InputHandler(0, 35, 10)

        values = ih.getMotorValues(IH.FORWARD)
        self.assertEqual(10, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])

        values = ih.getMotorValues(IH.RIGHT)
        self.assertEqual(20, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(10, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isMoving())

        values = ih.getMotorValues(IH.STOP)
        self.assertEqual(0, values[IH.LEFT_MOTOR_VALUE_INDEX])
        self.assertEqual(0, values[IH.RIGHT_MOTOR_VALUE_INDEX])
        self.assertTrue(ih.isStopped())
