__author__ = 'Paul Pearce'

################################################################
# Logical input values to translate to motor speed and direction
#
# Use these so they logically match the numbers on the numeric keypad
STOP    =   5
LEFT    =   4
RIGHT   =   6
FORWARD =   8
BACK =   2

import math
import logging

class InputHandler(object):
    def __init__(self, min_motor_value, max_motor_value, step_value):
        """
        Constructor
        :param min_motor_value: The value to stop the motor turning.
        :param max_motor_value: The value value to spin the motor at max. speed
        :param step_value: How many increment each move input will change the motor speed up or down. It is assumed that
        the same range will be valid for reversing a motor.
        :return:

        Example ih = IH.InputHandler(0, 100, 20)

        The logical motors can handle a range of -100 to +100 (full reverse to full forward), and 5 (100/20)
        forward/back move inputs will change the motor speed from stopped to full speed in the relevant direction.

        """

        self._logger = logging.getLogger("SkidSteering.InputHandler")

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

        self._stop()

    def move(self, input):
        """
        Given the logical input movement key, determine the new left and right (logical) motor values.
        :param input: A logical movement key value

        Below are some of the actions performed when the vehicle is in various states

        Vehicle State                       Key         Action
        =============                       ===         ======
        ANY                                 STOP        Vehicle will stop

        Stationary                          FORWARD     Move forward (straight ahead) slowly
        Stationary                          BACK        Move back slowly
        Stationary                          LEFT        Spin left slowly
        Stationary                          RIGHT       Spin right slowly

        Moving forward                      FORWARD     Move forward (straight ahead) more quickly
        Moving forward                      BACK        Stop
        Moving forward                      LEFT        Turn to the left
        Moving forward                      RIGHT       Turn to the right

        Moving forward and Turning left     FORWARD     Move forward (straight ahead) at the speed of the right (faster) track
        Moving forward and Turning left     BACK        Move forward (straight ahead) at the speed of the left (slower) track
        Moving forward and Turning left     LEFT        Turn left more quickly
        Moving forward and Turning left     RIGHT       same as FORWARD


        From the above, all the other states and actions can be inferred.

        """
        initialMotorValues = "L/R" + str([self._current_motor_left_value, self._current_motor_right_value])

        self._logger.info("Initial motor values: " + initialMotorValues)

        self._logger.info("Input: [" + str(input) + "]")

        ################
        # Generic action
        if input == LEFT:
            self._turn_left()
        elif input == RIGHT:
            self._turn_right()
        elif input == FORWARD:
            self._move_forward()
        elif input == BACK:
            self._move_back()
        elif input == STOP:
            self._stop()
        else:
            raise Exception("Invalid input: " + "[" + str(input) + "]")

        currentMotorValues = "L/R" + str([self._current_motor_left_value, self._current_motor_right_value])

        self._logger.info("Current motor values: " + currentMotorValues)

        #############################################################################
        # Sanity checks - cannot have one motor moving while another motor stationery
        problem_left_motor_speed   =   self._current_motor_left_value == 0 and self._current_motor_right_value != 0
        problem_right_motor_speed  =   self._current_motor_left_value != 0 and self._current_motor_right_value == 0

        if problem_left_motor_speed or problem_right_motor_speed:
            errorMessage = "Internal consistancy check failure - Motor values are invalid - one motor is stationery:"
            errorMessage = errorMessage + " Initial motor values: " + initialMotorValues
            errorMessage = errorMessage + " Input: " + "[" + str(input) + "]"
            errorMessage = errorMessage + " Current motor values: " + currentMotorValues

            raise Exception(errorMessage)


    def left_motor_value(self):
        """

        :return: The current left motor value
        """

        self._logger.debug(self._current_motor_left_value)

        return self._current_motor_left_value

    def right_motor_value(self):
        """

        :return: The current right motor value
        """
        self._logger.debug(self._current_motor_right_value)

        return self._current_motor_right_value

    def _is_spinning(self):
        """
        Determine if the vehicle is spinning on the spot
        :return:
        """
        moving  =  self._is_moving()
        dM      =   math.fabs(self._current_motor_left_value + self._current_motor_right_value)

        value =  moving and dM == 0.0

        self._logger.debug(str(value))

        return value


    def _is_turning(self):
        """
        Determine if the vehicle should be turning based on the current motor values
        :return: true if turning; else false
        """

        moving  =       self._is_moving()
        dM      =       (self._current_motor_left_value - self._current_motor_right_value)

        value   =   moving and dM != 0.0

        self._logger.debug(str(value))

        return value

    def _is_turning_left(self):
        value = self._current_motor_left_value < self._current_motor_right_value

        self._logger.debug(str(value))

        return value

    def _is_turning_right(self):
        value = self._current_motor_right_value < self._current_motor_left_value

        self._logger.debug(str(value))

        return value

    def _is_moving_forward(self):
        """
        Determine if we are actually moving forward
        :return:
        """
        value   =    self._current_motor_left_value >= 0 and self._current_motor_right_value >= 0

        self._logger.debug(str(value))

        return value


    def _is_moving_back(self):
        value   =    self._current_motor_left_value < 0 and self._current_motor_right_value < 0

        self._logger.debug(str(value))

        return value


    def _is_stopped(self):
        """

        :return:
        """
        value   =    self._current_motor_left_value == 0 and self._current_motor_right_value == 0

        self._logger.debug(str(value))

        return value

    def _is_moving(self):
        """

        :return:
        """
        value   =    not self._is_stopped()

        self._logger.debug(str(value))

        return value

    def _stop(self):

        """
        Set motor value to stop the vehicle motors
        :return:
        """

        self._logger.info("Entering")

        self._current_motor_left_value      =   self._min_motor_value
        self._current_motor_right_value     =   self._min_motor_value


    def _turn_left(self):
        """
        Determine the motor values to turn the vehicle left
        :return:
        """

        self._logger.info("Entering")

        if self._is_spinning() or self._is_stopped():
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
            else:
                # speed up right motor
                self._current_motor_right_value = self._current_motor_right_value + self._step_value

                # slow down left motor
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value

        elif self._is_moving_forward():
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

        elif self._is_moving_back():
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


    def _turn_right(self):
        """
        Determine the motor values to turn the vehicle right
        :return:
        """

        self._logger.info("Entering")

        if self._is_spinning() or self._is_stopped():
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
            else:
                # speed up left motor
                self._current_motor_left_value = self._current_motor_left_value + self._step_value

                # slow down right motor
                self._current_motor_right_value  = self._current_motor_right_value - self._step_value

        elif self._is_moving_forward():
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

        elif self._is_moving_back():
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


    def _move_forward(self):
        """
        Determine the motor values to move the vehicle forward
        :return:
        """

        self._logger.info("Entering")

        #####################################
        # Are we near the limits of max speed
        near_limit_left   = (self._current_motor_left_value + self._step_value) > self._max_motor_value
        near_limit_right  = (self._current_motor_right_value + self._step_value) > self._max_motor_value
        near_limits      =  near_limit_left or near_limit_right

        if self._is_spinning():
            self._stop()
        elif self._is_turning():
            if self._is_moving_forward():
                if(near_limits):
                    if(near_limit_left):
                        self._current_motor_right_value = self._current_motor_left_value
                    else:
                        self._current_motor_left_value  = self._current_motor_right_value
                else:
                    if self._is_turning_left():
                        self._current_motor_left_value  = self._current_motor_right_value
                    else:
                        self._current_motor_right_value = self._current_motor_left_value
            else:
                if self._is_turning_left():
                    self._current_motor_left_value  = self._current_motor_right_value
                else:
                    self._current_motor_right_value = self._current_motor_left_value
        else:
            if(near_limits):
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value + self._step_value
                self._current_motor_right_value = self._current_motor_right_value + self._step_value

    def _move_back(self):
        """
        Determine the motor values to move the vehicle backwards
        :return:
        """

        self._logger.info("Entering")

        #####################################
        # Are we near the limits of max speed
        near_limit_left     = (self._current_motor_left_value  - self._step_value) < (self._max_motor_value * -1)
        near_limit_right    = (self._current_motor_right_value - self._step_value) < (self._max_motor_value * -1)
        near_limits         = near_limit_left or near_limit_right

        if self._is_spinning():
            self._stop()
        elif self._is_turning():
            if self._is_moving_back():
                if(near_limits):
                    if(near_limit_left):
                        self._current_motor_right_value = self._current_motor_left_value
                    else:
                        self._current_motor_left_value  = self._current_motor_right_value
                else:
                    if self._is_turning_left():
                        self._current_motor_right_value = self._current_motor_left_value
                    else:
                        self._current_motor_left_value  = self._current_motor_right_value
            else:
                if self._is_turning_left():
                    self._current_motor_right_value = self._current_motor_left_value
                else:
                    self._current_motor_left_value  = self._current_motor_right_value
        else:
            if(near_limits):
                pass
            else:
                self._current_motor_left_value  = self._current_motor_left_value - self._step_value
                self._current_motor_right_value = self._current_motor_right_value - self._step_value

