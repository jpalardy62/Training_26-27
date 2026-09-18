# Drive 1 - Driver Control
# Completed student code
#
# This is the first portion of the JAR Python library. Later lessons will
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
# The six-motor example is active. If your robot has four drivetrain motors,
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

left_front = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
left_middle = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
left_back = Motor(Ports.PORT21, GearSetting.RATIO_6_1, True)

# Right drivetrain motors
right_front = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
right_middle = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
right_back = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)

# Drivetrain motor groups
drive_left = MotorGroup(left_front, left_middle, left_back)
drive_right = MotorGroup(right_front, right_middle, right_back)



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

    def drive(self, left_volts, right_volts):
        """Send voltage commands to the left and right drivetrain."""
        self.DriveL.spin(FORWARD, left_volts, VOLT)
        self.DriveR.spin(FORWARD, right_volts, VOLT)

    def control_tank(self):
        """Control the left and right sides with separate joysticks."""
        left_throttle = deadband(controller.axis3.position(), 5)
        right_throttle = deadband(controller.axis2.position(), 5)

        left_volts = to_volt(left_throttle)
        right_volts = to_volt(right_throttle)

        self.drive(left_volts, right_volts)

    def control_arcade(self):
        """Control throttle with Axis 3 and turning with Axis 1."""
        throttle = deadband(controller.axis3.position(), 5)
        turn = deadband(controller.axis1.position(), 5)

        left_volts = to_volt(throttle + turn)
        right_volts = to_volt(throttle - turn)

        self.drive(left_volts, right_volts)


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
