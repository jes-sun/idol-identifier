from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import identifier
import encode_faces
import gui
import global_vars

input_vid = "testitems\\flinch.mp4"
output_vid = "output.avi"

input_img = "testitems\\blackpink.jpg"
output_img = "output.jpg"

encodings_input = "encodings.pickle"

# Number of frames to skip in between facial detections
# Higher = faster performance, less accurate
# Lower = slower performance, more accurate
# Default 15
skip_frames = 15

# BGR value of the labels drawn to frame
label_color = (157,20,255)


def face_tracker_video(encodings_input, input_file, output_file):
	"""
	Processes facial recognition frame-by-frame for a video file.

	Parameters:
	input_file(str): the path to the input video
	output_file(str): the path to write output video

	Returns:
	1 if successful, -1 if unsuccessful
	"""
	# Open video file
	try:
		gui.current_info.set("[INFO] opening video file...")
		input_vid = cv2.VideoCapture(input_file)
	except:
		gui.current_info.set("[INFO] could not open video file.")
		return -1

	# Extract information from input video
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	fps = int(input_vid.get(cv2.CAP_PROP_FPS))
	w = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
	total_frames = int(input_vid.get(cv2.CAP_PROP_FRAME_COUNT))

	# Initialize writer
	writer = cv2.VideoWriter(output_file, fourcc, fps, (w,h))
	
	W = None
	H = None

	# Load encodings
	dataset = identifier.load_encodings(encodings_input)

	# Frame count
	frame_count = 0

	W = None
	H = None

	rois = []

	while True:
		# Loop through frames of video
		frame = input_vid.read()
		frame = frame[1]

		# If no more frames, end of video
		if frame is None:
			break

		# Convert frame for processing
		framep = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
		rgb = cv2.cvtColor(framep, cv2.COLOR_BGR2RGB)

		if W is None or H is None:
			(H,W) = framep.shape[:2]

		if frame_count % skip_frames == 0:
			# Identify faces in frame
			rois = identifier.identify(dataset, framep, rgb)
		for roi in rois:
			top = roi[0][0] * 2
			right = roi[0][1] * 2
			bottom = roi[0][2] * 2
			left = roi[0][3] * 2

			name = roi[1]
			cv2.rectangle(frame, (left, top), (right, bottom), label_color, 2) 
			y = top - 15 if top - 15 > 15 else top + 15			
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_color, 2)


		# Write to output
		writer.write(frame)

		# Show output
		cv2.imshow("Preview of {} ...".format(input_file), frame)
		#key = cv2.waitKey(int(1000/20)) & 0xFF
		key = cv2.waitKey(int(1000/30)) & 0xFF
		if key == ord("q"):
			break
		
		
		
		
		# Increment total frames
		frame_count += 1
		gui.current_info.set("[INFO] Frame {} / {}".format(frame_count, total_frames))

	# Release things
	writer.release()

	input_vid.release()

	cv2.destroyAllWindows()

	return 1

def face_tracker_image(encodings_input, input_file, output_file, output_frame):
	"""
	Processes facial recognition for a single image.

	Parameters:
	input_file(str): the path to the input image
	output_file(str): the path to write output image

	Returns:
	1 if successful, -1 if unsuccessful
	"""
	try:
		gui.current_info.set("[INFO] opening image file...")
		frame = cv2.imread(input_file)
	except:
		gui.current_info.set("[INFO] could not open image file.")
		return -1

	# Load encodings
	dataset = identifier.load_encodings(encodings_input)

	# Convert frame for processing
	framep = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
	rgb = cv2.cvtColor(framep, cv2.COLOR_BGR2RGB)

	# Identify faces in frame
	rois = []
	rois = identifier.identify(dataset, framep, rgb)
	for roi in rois:
		top = roi[0][0] * 2
		right = roi[0][1] * 2
		bottom = roi[0][2] * 2
		left = roi[0][3] * 2

		name = roi[1]
		cv2.rectangle(frame, (left, top), (right, bottom), label_color, 2) 
		y = top - 15 if top - 15 > 15 else top + 15			
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, label_color, 2)
	
	gui.current_info.set("[INFO] faces recognized.")
	cv2.imwrite(output_file, frame)
	global_vars.current_frame.set(frame)
	"""
	cv2.imshow("Preview of {} ...".format(input_file), frame)
	key = cv2.waitKey(0) & 0xFF
	if key == ord("q"):
		pass
	"""
	# Release things

	cv2.destroyAllWindows()

	return 1

#face_tracker_video(input_vid,output_vid)

#face_tracker_image(input_img,output_img)


