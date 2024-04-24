#!/bin/sh

# Run updates each time
arduino-cli core update-index
arduino-cli board list
arduino-cli core install arduino:avr
arduino-cli core list

arduino-cli compile --fqbn  arduino:avr:uno blink_example
arduino-cli upload -p /dev/cu.usbmodem101 --fqbn  arduino:avr:uno blink_example