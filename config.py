# Map all tunable vars in a single shared space.
motor_left_direction_pin = 17
motor_right_direction_pin = 27
motor_left_speed_pin = 13
motor_right_speed_pin = 12
# what pin is the safety light on?
safety_light_pin = 22
# how long after the last movement before we turn the light off?
safety_light_timeout = 20
# what pin is the physical switch that enters gps/controller mode on?
gps_mode_switch_pin = 24
# when using the mag how many degrees offset from the gps is it?
mag2gps_degree_offset = -20
# how many degrees in the heading are close enough to be accurate
turning_degree_accuracy = 10
# witmotion device path
witmotion_imu_path = "/dev/tty.usbserial-210"
# witmotion baud rate
witmotion_imu_baud_rate = 115200


