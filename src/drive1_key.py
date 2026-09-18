# Drive 1 - Driver Control
# Completed student code
#
# This is the first portion of the JAR Python library.  Later lessons will
# add more functions and methods to this same file.

# ---------------------------------------------------------------------------
# Library imports
# ---------------------------------------------------------------------------

from vex import *


# ---------------------------------------------------------------------------
# Robot configuration
# ---------------------------------------------------------------------------

brain = Brain()
controller = Controller(PRIMARY)

# Choose ONE drivetrain configuration below.
# The six-motor example is active.  If your robot has four drivetrain motors,
# comment out the six-motor configuration and use the four-motor example.

# ----- Four-motor drivetrain example -----
#
# LeftFront = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
# LeftBack = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
#
# RightFront = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
# RightBack = Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)
#
# DriveL = MotorGroup(LeftFront, LeftBack)
# DriveR = MotorGroup(RightFront, RightBack)


# ----- Six-motor drivetrain example -----

LeftFront = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
LeftMiddle = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
LeftBack = Motor(Ports.PORT21, GearSetting.RATIO_6_1, True)

RightFront = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
RightMiddle = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
RightBack = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)

DriveL = MotorGroup(LeftFront, LeftMiddle, LeftBack)
DriveR = MotorGroup(RightFront, RightMiddle, RightBack)


# ---------------------------------------------------------------------------
# JAR utility functions
# ---------------------------------------------------------------------------

def to_volt(percent):
    """Convert a value from -100..100 percent to volts."""
    return percent * 12.0 / 100.0


def deadband(input_value, width):
    """Return 0 when the input is inside the deadband."""
    if abs(input_value) < width:
        return 0
    return input_value


# ---------------------------------------------------------------------------
# JAR Drive class
# ---------------------------------------------------------------------------

class Drive:

    def __init__(self, DriveL, DriveR):
        self.DriveL = DriveL
        self.DriveR = DriveR

    def control_tank(self):
        """Control the left and right sides with separate joysticks."""
        leftthrottle = deadband(controller.axis3.position(), 5)
        rightthrottle = deadband(controller.axis2.position(), 5)

        self.DriveL.spin(FORWARD, to_volt(leftthrottle), VOLT)
        self.DriveR.spin(FORWARD, to_volt(rightthrottle), VOLT)

    def control_arcade(self):
        """Control throttle with Axis 3 and turning with Axis 1."""
        throttle = deadband(controller.axis3.position(), 5)
        turn = deadband(controller.axis1.position(), 5)

        self.DriveL.spin(FORWARD, to_volt(throttle + turn), VOLT)
        self.DriveR.spin(FORWARD, to_volt(throttle - turn), VOLT)


# ---------------------------------------------------------------------------
# Create the chassis
# ---------------------------------------------------------------------------

chassis = Drive(DriveL, DriveR)


# ---------------------------------------------------------------------------
# Autonomous
# ---------------------------------------------------------------------------

def autonomous():
    pass


# ---------------------------------------------------------------------------
# Driver control
# ---------------------------------------------------------------------------

def driver_control():
    while True:
        chassis.control_arcade()
        wait(20, MSEC)


# ---------------------------------------------------------------------------
# Competition
# ---------------------------------------------------------------------------

competition = Competition(driver_control, autonomous)

