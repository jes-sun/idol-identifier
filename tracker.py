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
import global_vars

def face_tracker_video(encodings_input, input_file, output_file):
	"""
	Processes facial recognition frame-by-frame for a video file.

	Parameters:
	encodings_input(str): the path to the encodings file
	input_file(str): the path to the input video
	output_file(str): the path to write output video

	Returns:
	1 if successful, -1 if unsuccessful
	"""
	# Open video file
	try:
		print("[INFO] opening video file...")
		input_vid = cv2.VideoCapture(input_file)
	except:
		print("[INFO] could not open video file.")
		return -1

	# Extract information from input video
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	fps = int(input_vid.get(cv2.CAP_PROP_FPS))
	w = int(input_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(input_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
	total_frames = int(input_vid.get(cv2.CAP_PROP_FRAME_COUNT))

	# Initialize writer
	writer = cv2.VideoWriter(output_file, fourcc, fps, (w,h))

	# Load encodings
	dataset = identifier.load_encodings(encodings_input)

	# Frame count
	frame_count = 0
	
	# Check if video is too large
	large = False
	if w > 1000 or h > 600:
		large = True


	rois = []

	while True:
		# Loop through frames of video
		frame = input_vid.read()
		frame = frame[1]

		# If no more frames, end of video
		if frame is None:
			break

		# Convert frame for processing
		if large:
			framep = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
		else: 
			framep = frame
		rgb = cv2.cvtColor(framep, cv2.COLOR_BGR2RGB)

		if frame_count % global_vars.skip_frames == 0:
			# Identify faces in frame
			rois = identifier.identify(dataset, framep, rgb)
		for roi in rois:
			if large:
				top = roi[0][0] * 2
				right = roi[0][1] * 2
				bottom = roi[0][2] * 2
				left = roi[0][3] * 2
			else:
				top = roi[0][0]
				right = roi[0][1]
				bottom = roi[0][2]
				left = roi[0][3]
			name = roi[1]
			if global_vars.draw_rects is True:
				cv2.rectangle(frame, (left, top), (right, bottom), global_vars.label_color.bgr, 2) 
			y = top - 15 if top - 15 > 15 else top + 15			
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, global_vars.label_color.bgr, 2)


		# Write to output
		writer.write(frame)

		# Show output
		cv2.imshow("Preview of {} ...".format(input_file), frame)
		#key = cv2.waitKey(int(1000/30)) & 0xFF
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		
		
		
		
		# Increment total frames
		frame_count += 1
		print("[INFO] Frame {} / {}".format(frame_count, total_frames))

	# Release things
	writer.release()

	input_vid.release()

	cv2.destroyAllWindows()

	return 1

def face_tracker_image(encodings_input, input_file, output_file):
	"""
	Processes facial recognition for a single image.

	Parameters:
	encodings_input(str): the path to the encodings file
	input_file(str): the path to the input image
	output_file(str): the path to write output image

	Returns:
	1 if successful, -1 if unsuccessful
	"""
	try:
		print("[INFO] opening image file...")
		frame = cv2.imread(input_file)
	except:
		print("[INFO] could not open image file.")
		return -1

	# Load encodings
	dataset = identifier.load_encodings(encodings_input)

	# Check if image is too large
	w,h = cv2.GetSize(frame)
	large = false
	if w > 1000 or h > 600:
		large = True

	# Convert frame for processing
	if large:
		framep = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
	else:
		framep = frame
	rgb = cv2.cvtColor(framep, cv2.COLOR_BGR2RGB)

	# Identify faces in frame
	rois = []
	rois = identifier.identify(dataset, framep, rgb)
	for roi in rois:
		if large:
			top = roi[0][0] * 2
			right = roi[0][1] * 2
			bottom = roi[0][2] * 2
			left = roi[0][3] * 2
		else:
			top = roi[0][0]
			right = roi[0][1]
			bottom = roi[0][2]
			left = roi[0][3]
		name = roi[1]
		if global_vars.draw_rects is True:
			cv2.rectangle(frame, (left, top), (right, bottom), global_vars.label_color.bgr, 2) 
		y = top - 15 if top - 15 > 15 else top + 15			
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, global_vars.label_color.bgr, 2)
	
	print("[INFO] faces recognized.")
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

