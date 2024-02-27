def controller_mode():
    while True:
        left_speed, right_speed = nes.wpm_controller(nes.snes_input())
        motor_driver.set_left_speed(left_speed)
        motor_driver.set_right_speed(right_speed)

