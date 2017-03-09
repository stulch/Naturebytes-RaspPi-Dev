#!/usr/bin/python
# Naturebytes Wildlife Cam Kit | V1.01
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Revisions by SL Cheney
# V1.01.01 Write to SD card rather than flash drive - speeds up process
#          (also frees up USB for WiFi dongle allowing remote access to photos).
# V1.01.02 Changed date format printed on the photo. Date format unchanged for file name.
#          To achieve this various field names have been changed and meanwhile some have
#          been changed to make them more meaningful.
# V1.01.03 Added options to take photos, videos or photo followed by video.
#          Change below fields photoMode and videoMode = True or False depending on requirments
# V1.01.04 Added separate dates for photo and video so they are more acurate especialy for
#          videos when in both photo and video modes.
# V1.01.05 Added options to use IR.
#          Change below field irMode = True or False depending on requirment.
#          Added logging of IR ring status and switching of it off
#          Set irMode = False
#          Added -vf to taking a photo to flip camera the right way round
# V1.01.06 (09.03.2017)
#          Added -%f to include miliseconds for photo/video file names
#          In case two photos are taken in the same second
#          Added photo_file_location & video_file_location varibles
#          Changed the default of photo_file_location from
#          /home/pi/Naturebytes/tmppics/ to /home/pi/Naturebytes/Pictures/
#          Changed the default of video_file_location from
#          /home/pi/Naturebytes/tmpvids/ to /home/pi/Naturebytes/Videos/
#          As a result new directories created and old ones deleted
#          Added addLogo varible so can easily switch between adding
#          a logo or not
#          Added logo paths and file name varibles

import RPi.GPIO as GPIO
import time
from subprocess import call
from datetime import datetime
import logging

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live 

logging.basicConfig(format='%(asctime)s %(message)s',filename='naturebytes_camera_log',level=logging.DEBUG)
logging.info('Naturebytes Wildlife Cam Kit started up successfully')

#Defining modes
photoMode = True
videoMode = False
irMode = False
verticalFlip = False
addLogo = True

logo_file_location = '/home/pi/Naturebytes/Scripts/'
logo_file_name = "naturebytes_logo_80.png"
logo_IR_file_name = "naturebytes_logo_80.png"

# Defining our default states so we can detect a change
prevState = False
currState = False
# prevBattState = False
# currBattState = False

# Assigning a variable to the pins that we have connected the PIR to
sensorPin = 11
IRring = 22

# You may want to detect the battery status (low or high) in the future so we code commented out a way of doing this to assist using pin 15
# lowbattPin = 15

# Setting the GPIO (General Purpose Input Output) pins up so we can detect if they are HIGH or LOW (on or off)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(lowbattPin, GPIO.IN)

if irMode == True:
	GPIO.setup(IRring, GPIO.OUT)
	cam_name = "Camera 2 IR"
	selected_logo = logo_file_name
else:
	cam_name = "Camera 2"
	selected_logo = logo_IR_file_name

# Starting a loop

while True:
	time.sleep(0.1)
	prevState = currState
	# prevBattState = currBattState
    
	# Map the state of the camera to our input pins (jumper cables connected to your PIR)
	
	currState = GPIO.input(sensorPin)
	# currBattState = GPIO.input(lowbattPin)
	
	# Checking that our state has changed
	
	if currState != prevState:
		# About to check if our new state is HIGH or LOW
		
		newState = "HIGH" if currState else "LOW"
		# newBattState = "HIGH" if currBattState else "LOW"        
		print "GPIO pin %s is %s" % (sensorPin, newState)
		# print "Battery level detected via pin %s is %s" % (lowbattPin, newBattState)
		
		if currState:  # Our state has changed, so that must be a trigger from the PIR       
			
			# batt_state = newBattState
			# Checking the current status of the battery
			
			# Recording that a PIR trigger was detected and logging the battery level at this time
			logging.info('PIR trigger detected')
			# logging.info('Battery level is %(get_batt_level)s', { 'get_batt_level': batt_state })
			
			if photoMode == True:
				if irMode == True:
					GPIO.output(IRring, GPIO.HIGH)
					logging.info('IR ring switched ON for photo')
				
				# Getting dates and times for JPG file and photo overlay
				# Getting dates and times for photo"
				logging.info('About to get dates and times for photo')
				i = datetime.now() # Get the time now
				get_file_date = i.strftime('%Y-%m-%d') # Get and format the date for the file name
				get_file_time = i.strftime('%H-%M-%S-%f') # Get and format the time for the file name
				get_photo_date = i.strftime('%A %d %B %Y') # Get and format the date for the photo/video
				get_photo_time = i.strftime('%I:%M.%S %p') # Get and format the time for the photo/video
				
				photo_file_location = '/home/pi/Naturebytes/Pictures/'
				photo_file_name = get_file_date + '_' +  get_file_time + '.jpg'
			
				# Using the raspistill library to take a photo and show that a photo has been taken in a small preview box on the desktop
				# cmd = 'raspistill -t 300 -w 1920 -h 1440 --nopreview -o /media/usb0/' + photo
				if verticalFlip == False:
					# cmd = 'raspistill -t 300 -w 1920 -h 1440 --nopreview -o /home/pi/Naturebytes/tmppics/' + photo_file_name
					cmd = 'raspistill -t 300 -w 1920 -h 1440 --nopreview -o ' + photo_file_location + photo_file_name
				else:
					# cmd = 'raspistill -t 300 -w 1920 -h 1440 -vf --nopreview -o /home/pi/Naturebytes/tmppics/' + photo_file_name
					cmd = 'raspistill -t 300 -w 1920 -h 1440 -vf --nopreview -o' + photo_file_location + photo_file_name
				print 'cmd ' +cmd
				# Log that we are about to take a photo"
				logging.info('About to take a photo')
				call ([cmd], shell=True)
				
				# Log that a photo was taken successfully and state the file name so we know which one"
				logging.info('Photo taken successfully %(show_photo_file_name_name)s', { 'show_photo_file_name_name': photo_file_name })
				# photo_location =  '/media/usb0/' + photo
				photo_path_file_name =  photo_file_location + photo_file_name
				
				# Log that we are about to attempt to write the overlay text"
				logging.info('About to write the overlay text')            
				
				overlay = "/usr/bin/convert "+ photo_path_file_name + " "
				
				# Use ImageMagick to write text and meta data onto the photo.
				# overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date: " + get_photo_date + " | Time: " + get_photo_time + "' -gravity southeast -annotate +6+6 'Camera 1' " + photo_path_file_name
				overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date: " + get_photo_date + " | Time: " + get_photo_time + "' -gravity southeast -annotate +6+6 ' " + " " + cam_name + "' " + photo_path_file_name
				# Log that we the text was added successfully"
				logging.info('Added the overlay text successfully')
				call ([overlay], shell=True)
				
				if addLogo == True:
					logo_path_file_name = logo_file_location + selected_logo # Not used at present
					#' I can't get the below to use selected logo as opposed to naturebytes_logo_80.png
					# Add a small Naturebytes logo to the top left of the photo. Note - you could change this to your own logo if you wanted.
					logging.info('Adding the Naturebytes logo')
					# overlay = '/usr/bin/convert '+ photo_path_file_name + ' /home/pi/Naturebytes/Scripts/naturebytes_logo_80.png -geometry +1+1 -composite ' + photo_path_file_name
					overlay = '/usr/bin/convert '+ photo_path_file_name + ' logo_file_location + naturebytes_logo_80.png -geometry +1+1 -composite ' + photo_path_file_name
					call ([overlay], shell=True)
				
					# Log that the logo was added succesfully"
					logging.info('Logo added successfully')

				if irMode == True:
					GPIO.output(IRring, GPIO.LOW)
					logging.info('IR ring switched off for photo')
				
				# If you wished to move the photo to the flash drive you could code it below
				# it would still be quicker than what was above as previously there was more
				# than one write to the flash drive
				# I would need to find the python equivalent of the below
				# cp /home/pi/Naturebytes/tmppics/photo_file_name /media/usb0/$photo_file_name
				
			if videoMode == True:

				if irMode == True:
					GPIO.output(IRring, GPIO.HIGH)
					logging.info('IR ring switched ON for video')					

				# Getting dates and times for h264 file and video overlay
				# Details for overlay are for possible future development
				# Getting dates and times for video"
				logging.info('About to get dates and times for video')
				i2 = datetime.now() # Get the time now
				get_file_date = i2.strftime('%Y-%m-%d') # Get and format the date for the file name
				get_file_time = i2.strftime('%H-%M-%S-%f') # Get and format the time for the file name
				get_photo_date = i2.strftime('%A %d %B %Y') # Get and format the date for the video
				get_photo_time = i2.strftime('%I:%M.%S %p') # Get and format the time for the video
			
				video_file_location = '/home/pi/Naturebytes/Videos/'
				video_file_name = get_file_date + '_' +  get_file_time + '.h264'
				
				if verticalFlip == False:
					# cmd = 'raspivid -t 10000 -o /home/pi/Naturebytes/tmpvids/' + video_file_name
					cmd = 'raspivid -t 10000 -o ' + video_file_location + video_file_name
				else:
					# cmd = 'raspivid -vf -t 10000 -o /home/pi/Naturebytes/tmpvids/' + video_file_name
					cmd = 'raspivid -vf -t 10000 -o ' + video_file_location + video_file_name
				print 'cmd ' +cmd
				# Log that we have are about to start filming a video"
				logging.info('About to start filming a video')
				call ([cmd], shell=True)
				
				# Log that filmed successfully and state the file name so we know which one"
				logging.info('Filmed successfully %(show_video_file_name_name)s', { 'show_video_file_name_name': video_file_name })

				if irMode == True:
					GPIO.output(IRring, GPIO.LOW)
					logging.info('IR ring switched off for video')
		else:
			
			# print "Waiting for a new PIR trigger to continue"
			logging.info('Waiting for a new PIR trigger to continue')

# END
