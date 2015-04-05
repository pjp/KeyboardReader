__author__ = 'Paul Pearce'

NOOP    =   0

# Use these so they logically match the numbers on the numeric keypad
STOP    =   5
LEFT    =   4
RIGHT   =   6
FORWARD =   8
REVERSE =   2

import math
import logging


class InputHandler(object):
    def __init__(self, min_motor_value, max_motor_value, step_value):
        """
        Constructor
        :param min_motor_value: The value to stop the motor turning.
        :param max_motor_value: The value value to spin the motor at max. speed
        :param step_value: How many increment each key press will move the motor value up or down. It is assumed that
        the same range will be valid for reversing a motor.
        :return:

        Example ih = IH.InputHandler(0, 100, 20)

        The logical motors can handle a range of -100 to +100 (full reverse to full forward), and 5 (100/20)
        forward/back keypress's will move the motor from stopped to full speed in the relevant direction.

        """
        self.logger = logging.getLogger(__name__)

        # Sanity checks

        if min_motor_value > max_motor_value:
            raise Exception("min value cannot be > max value")

        if(min_motor_value == max_motor_value):
            raise Exception("Cann have min == max")

        if step_value < 1:
            raise Exception("step value must be >= 1")

        if (max_motor_value - min_motor_value) < step_value:
            raise Exception("step is too big")


        self._min_motor_value       =   min_motor_value
        self._max_motor_value       =   max_motor_value
        self._step_value            =   step_value

        self._current_motor_left_value     =   0
        self._current_motor_right_value    =   0

        self.stop()

    def getMotorValues(self, input):
        """
        Given the logical input movement key, determine the new left and right (logical) motor values.
        :param input: A logical movement key value
        :return: A list containing the new left and right motor values
        """

        self.logger.info("getMotorValues: input [" + str(input) + "]")

        self.logger.info("getMotorValues: current L/R" + str([self._current_motor_left_value, self._current_motor_right_value]))

        ################
        # Generic action
        if input == NOOP:
            pass
        elif input == LEFT:
            self.left()
        elif input == RIGHT:
            self.right()
        elif input == FORWARD:
            self.forward()
        elif input == REVERSE:
            self.reverse()
        elif input == STOP:
            self.stop()
        else:
            raise Exception("Invalid input")

        #############################################################################
        # Sanity checks - cannot have one motor moving while another motor stationery
        tLeft   =   self._current_motor_left_value == 0 and self._current_motor_right_value != 0
        tRight  =   self._current_motor_left_value != 0 and self._current_motor_right_value == 0

        if tLeft or tRight:
            raise Exception("Motor values are invalid")

        self.logger.info("getMotorValues: output  L/R" + str([self._current_motor_left_value, self._current_motor_right_value]))

        return [self._current_motor_left_value, self._current_motor_right_value]

    def isSpinning(self):
        """
        Determine if the vehicle is spinning on the spot
        :return:
        """
        moving  =  self.isMoving()
        dM      =   math.fabs(self._current_motor_left_value + self._current_motor_right_value)

        value =  moving and dM == 0.0

        self.logger.debug("isSpinning: " + str(value))

        return value


    def isTurning(self):
        """
        Determine if the vehicle should be turning based on the current motor values
        :return: true if turning; else false
        """

        moving  =       self.isMoving()
        dM      =       (self._current_motor_left_value - self._current_motor_right_value)

        value   =   moving and dM != 0.0

        self.logger.debug("isTurning: " + str(value))

        return value


    def isMovingForward(self):
        """
        Determine if we are actually moving forward
        :return:
        """
        value   =    self._current_motor_left_value >= 0 and self._current_motor_right_value >= 0

        self.logger.debug("isMovingForward: " + str(value))

        return value


    def isMovingInReverse(self):
        value   =    not self.isStopped() and not self.isMovingForward()

        self.logger.debug("isMovingInReverse: " + str(value))

        return value


    def isStopped(self):
        """

        :return:
        """
        value   =    self._current_motor_left_value == 0 and self._current_motor_right_value == 0

        self.logger.debug("isStopped: " + str(value))

        return value

    def isMoving(self):
        """

        :return:
        """
        value   =    not self.isStopped()

        self.logger.debug("isMoving: " + str(value))

        return value

    def stop(self):

        """
        Set motor value to stop the vehicle motors
        :return:
        """

        self.logger.info("stop:")

        self._current_motor_left_value      =   self._min_motor_value;
        self._current_motor_right_value     =   self._min_motor_value;


    def left(self):
        """
        Determine the motor values to turn the vehicle left
        :return:
        """

        self.logger.info("left:")

        if self.isSpinning() or self.isStopped():
            #########################################################
            # Are we near the limits of max speed in either direction
            target_left_value     = self._current_motor_left_value - self._step_value
            target_right_value    = self._current_motor_right_value + self._step_value

            ###########################
            # Slow left, speed up right
            near_limit_left     = target_left_value < (self._max_motor_value * -1)
            near_limit_right    = target_right_value >= self._max_motor_value

            if near_limit_left and near_limit_right:
                pass
            elif near_limit_left and not near_limit_right:
                # speed up right motor
                self._current_motor_right_value = target_right_value

                # slow down left motor
                self._current_motor_left_value  = target_left_value
            elif near_limit_right and not near_limit_left:
                # slow down right motor
                self._current_motor_right_value = self._current_motor_right_value - self._step_value

                # speed up left motor
                self._current_motor_left_value  = self._current_motor_left_value + self._step_value
            else:
                # speed up right motor
                self._current_motor_right_value = self._current_motor_right_value + self._step_value

                # slow down left motor
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value

        elif self.isMovingForward():
            #########################################################
            # Are we near the limits of max speed in either direction
            near_limit_left     = (self._current_motor_left_value - self._step_value) <= 0
            near_limit_right    = (self._current_motor_right_value + self._step_value) > self._max_motor_value

            if not near_limit_right :
                # speed up right motor
                self._current_motor_right_value = self._current_motor_right_value + self._step_value
            elif not near_limit_left:
                # slow down left motor
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value
            else:
                pass

        elif self.isMovingInReverse():
            #########################################################
            # Are we near the limits of max speed in either direction
            near_limit_left    = (self._current_motor_left_value + self._step_value) >= 0
            near_limit_right    = (self._current_motor_right_value - self._step_value) < (self._max_motor_value * -1)

            if not near_limit_right :
                # speed up right motor
                self._current_motor_right_value = self._current_motor_right_value - self._step_value
            elif not near_limit_left:
                # slow down left motor
                self._current_motor_left_value  = self._current_motor_left_value + self._step_value
            else:
                pass
        else:
            raise Exception("Unknown state when turning Left")


    def right(self):
        """
        Determine the motor values to turn the vehicle right
        :return:
        """

        self.logger.info("right:")

        if self.isSpinning() or self.isStopped():
            #########################################################
            # Are we near the limits of max speed in either direction
            target_left_value     = self._current_motor_left_value + self._step_value
            target_right_value    = self._current_motor_right_value - self._step_value

            ###########################
            # Slow right, speed up left
            near_limit_right   = target_right_value < (self._max_motor_value * -1)
            near_limit_left    = target_left_value >= self._max_motor_value

            if near_limit_left and near_limit_right:
                pass
            elif near_limit_right and not near_limit_left:
                # speed up left motor
                self._current_motor_left_value = target_left_value

                # slow down right motor
                self._current_motor_right_value  = target_right_value
            elif near_limit_left and not near_limit_right:
                # slow down left motor
                self._current_motor_left_value = self._current_motor_left_value - self._step_value

                # speed up right motor
                self._current_motor_right_value  = self._current_motor_right_value + self._step_value
            else:
                # speed up left motor
                self._current_motor_left_value = self._current_motor_left_value + self._step_value

                # slow down right motor
                self._current_motor_right_value  = self._current_motor_right_value - self._step_value

        elif self.isMovingForward():
            #########################################################
            # Are we near the limits of max speed in either direction
            near_limit_right     = (self._current_motor_right_value - self._step_value) <= 0
            near_limit_left    = (self._current_motor_left_value + self._step_value) > self._max_motor_value

            if not near_limit_left :
                # speed up left motor
                self._current_motor_left_value = self._current_motor_left_value + self._step_value
            elif not near_limit_right:
                # slow down right motor
                self._current_motor_right_value  = self._current_motor_right_value - self._step_value
            else:
                pass

        elif self.isMovingInReverse():
            #########################################################
            # Are we near the limits of max speed in either direction
            near_limit_right    = (self._current_motor_right_value + self._step_value) >= 0
            near_limit_left    = (self._current_motor_left_value - self._step_value) < (self._max_motor_value * -1)

            if not near_limit_left :
                # speed up left motor
                self._current_motor_left_value = self._current_motor_left_value - self._step_value
            elif not near_limit_right:
                # slow down right motor
                self._current_motor_right_value  = self._current_motor_right_value + self._step_value
            else:
                pass
        else:
            raise Exception("Unknown state when turning Right")


    def forward(self):
        """
        Determine the motor values to move the vehicle forward
        :return:
        """

        self.logger.info("forward:")

        #####################################
        # Are we near the limits of max speed
        near_limit_left   = (self._current_motor_left_value + self._step_value) > self._max_motor_value
        near_limit_right  = (self._current_motor_right_value + self._step_value) > self._max_motor_value
        near_limits      =  near_limit_left or near_limit_right

        if self.isTurning():
            if(near_limits):
                # Cannot speed up both motors without affecting the turning radius
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value + self._step_value
                self._current_motor_right_value = self._current_motor_right_value + self._step_value
        else:
            if(near_limits):
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value + self._step_value
                self._current_motor_right_value = self._current_motor_right_value + self._step_value

    def reverse(self):
        """
        Determine the motor values to move the vehicle backwards
        :return:
        """

        self.logger.info("reverse:")

        #####################################
        # Are we near the limits of max speed
        near_limit_left     = (self._current_motor_left_value  - self._step_value) < (self._max_motor_value * -1)
        near_limit_right    = (self._current_motor_right_value - self._step_value) < (self._max_motor_value * -1)
        near_limits         = near_limit_left or near_limit_right

        if self.isTurning():
            if(near_limits):
                # Cannot speed up both motors without affecting the turning radius
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value
                self._current_motor_right_value = self._current_motor_right_value - self._step_value
        else:
            if(near_limits):
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value
                self._current_motor_right_value = self._current_motor_right_value - self._step_value


