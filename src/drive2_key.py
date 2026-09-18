from vex import *

# -------------------------------------------------------------
# Robot Configuration
# -------------------------------------------------------------

brain = Brain()
controller = Controller(PRIMARY)

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



# -------------------------------------------------------------
# Drive Class
# -------------------------------------------------------------

class Drive:

    def __init__(self, drive_left, drive_right):
        self.drive_left = drive_left
        self.drive_right = drive_right


    # ---------------------------------------------------------
    # drive(left_volts, right_volts)
    #
    # Sends voltage directly to the left and right sides of
    # the drivetrain.
    #
    # PARAMETERS:
    #   left_volts  - Voltage sent to the left drivetrain
    #   right_volts - Voltage sent to the right drivetrain
    # ---------------------------------------------------------

    def drive(self, left_volts, right_volts):
        self.drive_left.spin(FORWARD, left_volts, VOLT)
        self.drive_right.spin(FORWARD, right_volts, VOLT)


    # ---------------------------------------------------------
    # control_tank()
    #
    # Controls the drivetrain using tank drive.
    # Axis 3 controls the left side.
    # Axis 2 controls the right side.
    # ---------------------------------------------------------

    def control_tank(self):
        left = controller.axis3.position()
        right = controller.axis2.position()

        # Deadband
        if abs(left) < 5:
            left = 0

        if abs(right) < 5:
            right = 0

        # Convert joystick percent to voltage
        left_volts = left * 0.12
        right_volts = right * 0.12

        self.drive(left_volts, right_volts)


    # ---------------------------------------------------------
    # control_arcade()
    #
    # Controls the drivetrain using arcade drive.
    # Axis 3 controls forward/backward movement.
    # Axis 1 controls turning.
    # ---------------------------------------------------------

    def control_arcade(self):
        throttle = controller.axis3.position()
        turn = controller.axis1.position()

        # Deadband
        if abs(throttle) < 5:
            throttle = 0

        if abs(turn) < 5:
            turn = 0

        # Arcade drive mixing
        left = throttle + turn
        right = throttle - turn

        # Convert joystick percent to voltage
        left_volts = left * 0.12
        right_volts = right * 0.12

        self.drive(left_volts, right_volts)


    # ---------------------------------------------------------
    # timed_move(left_volts, right_volts, move_time)
    #
    # Drives the robot using the requested left and right
    # voltages for a specified amount of time.
    #
    # PARAMETERS:
    #   left_volts  - Voltage sent to the left drivetrain
    #   right_volts - Voltage sent to the right drivetrain
    #   move_time   - Length of the move in seconds
    # ---------------------------------------------------------

    def timed_move(self, left_volts, right_volts, move_time):
        start_time = brain.timer.time(SECONDS)

        while brain.timer.time(SECONDS) - start_time < move_time:
            self.drive(left_volts, right_volts)
            wait(5, MSEC)

        self.drive(0, 0)


# -------------------------------------------------------------
# Create the Drive object
# -------------------------------------------------------------

drive = Drive(drive_left, drive_right)


# -------------------------------------------------------------
# Autonomous
# -------------------------------------------------------------

def autonomous():

    # Drive forward at 8 volts for 1 second
    drive.timed_move(8, 8, 1)

    # Turn in place for 0.5 seconds
    drive.timed_move(6, -6, 0.5)

    # Drive forward at 5 volts for 1.5 seconds
    drive.timed_move(5, 5, 1.5)


# -------------------------------------------------------------
# Driver Control
# -------------------------------------------------------------

def driver_control():

    while True:
        drive.control_arcade()
        wait(20, MSEC)


# -------------------------------------------------------------
# Competition
# -------------------------------------------------------------

competition = Competition(driver_control, autonomous)