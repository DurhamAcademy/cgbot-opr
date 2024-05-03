# Map all tunable vars in a single shared space.

# motor stuff
motor_left_direction_pin = 17
motor_right_direction_pin = 27
motor_left_speed_pin = 13
motor_right_speed_pin = 12
drive_speed = 100
drive_speed_turning = 30
# what pin is the safety light on?
safety_light_pin = 22
# how long after the last movement before we turn the light off?
safety_light_timeout = 20
# camera enable IO pin - Alarm1 input on camera
camera_io_alarm_pin = 6
# what pin is the physical switch that enters gps/controller mode on?
gps_mode_switch_pin = 24
# when using the mag how many degrees offset from the gps is it?
mag2gps_degree_offset = -20
# how many degrees in the heading are close enough to be accurate
turning_degree_accuracy = 10
# what is considered to low in battery voltage to continue functioning?
voltage_min_threshold = 9
# how often to read the ultrasonic sensors
ultrasonic_check_interval = 3
# how often to save gps coords, temp, and humidity to text files for frontend.
frontend_store_data_interval = 8
#
ultra_alert_distance = 20

