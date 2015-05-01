import pygame.mixer
from time import sleep

import cv2
import select
import sys
import config
import face
import hardware

pygame.mixer.init(48000, -16, 1, 1024)
soundA = pygame.mixer.Sound("/home/pi/my_code/welcome.wav")
soundB = pygame.mixer.Sound("/home/pi/my_code/wait.wav")
soundC = pygame.mixer.Sound("/home/pi/my_code/later.wav")

soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)
soundChannelC = pygame.mixer.Channel(3)

def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False

def main():
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	door = hardware.Door()
	# Move box to locked position.
	door.lock()
	print 'Running Lock...'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press Ctrl-C to quit.'
	while True:
		try:
			# Check if capture should be made.
			# TODO: Check if button is pressed.
			if door.is_button_up() or is_letter_input('l'):
				if not door.is_locked:
					# Lock the door if it is unlocked
					door.lock()
					print 'Door is now locked.'
				else:
					print 'Button pressed, looking for face...'
					# Check for the positive face and unlock if found.
					image = camera.read()
					# Convert image to grayscale.
					image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
					# Get coordinates of single face in captured image.
					result = face.detect_single(image)
					if result is None:
						print 'Could not detect single face!  Check the image in capture.pgm' \
							  ' to see what was captured and try again with only one face visible.'
						soundChannelC.play(soundC)
						sleep(.01)
						continue
					x, y, w, h = result
					# Crop and resize image to face.
					crop = face.resize(face.crop(image, x, y, w, h))
					# Test face against model.
					label, confidence = model.predict(crop)
					print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
						'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
						confidence)
					if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
						print 'Recognized face! Unlocking Door Now...'
						door.unlock()
						soundChannelA.play(soundA)
						sleep(.01)
					else:
						print 'Did not recognize face!'
						soundChannelB.play(soundB)
						sleep(.01)
		except KeyboardInterrupt:
			door.clean()
			sys.exit()

if __name__ == '__main__':
	main()
