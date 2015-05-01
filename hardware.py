
import time
import numpy as np
import cv2
import RPi.GPIO as GPIO

import picam
import config
import face

class Door(object):
	"""Class to represent the state and encapsulate access to the hardware of 
	the treasure box."""
	def __init__(self):
		# Initialize lock servo and button.
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(config.LOCK_SERVO_PIN, GPIO.OUT)
		GPIO.setup(config.BUTTON_PIN, GPIO.IN)
		self.servo = GPIO.PWM(config.LOCK_SERVO_PIN, 50)
		
		
		# Set initial box state.
		self.servo.start(2.5)
		self.button_state = GPIO.input(config.BUTTON_PIN)
		self.is_locked = None

	def lock(self):
		"""Lock the box."""
		self.servo.ChangeDutyCycle(2.5)
		self.is_locked = True

	def unlock(self):
		"""Unlock the box."""
		self.servo.ChangeDutyCycle(12.5)
		self.is_locked = False

	def clean(self):
		self.servo.stop()
		GPIO.cleanup()

	def is_button_up(self):
	 	"""Return True when the box button has transitioned from down to up (i.e.
	 	the button was pressed)."""
	 	old_state = self.button_state
	 	self.button_state = GPIO.input(config.BUTTON_PIN)
	 	# Check if transition from down to up
	 	if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
	 		# Wait 20 milliseconds and measure again to debounce switch.
	 		time.sleep(20.0/1000.0)
	 		self.button_state = GPIO.input(config.BUTTON_PIN)
	 		if self.button_state == config.BUTTON_UP:
	 			return True
	 	return False
