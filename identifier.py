
import face_recognition
import argparse
import pickle
import cv2
import numpy as np
import global_vars

# Tolerance for the facial detection
# Lower = more strict, Higher = more lax
# Default 0.45
tolerance = 0.45


def load_encodings(encodings_input):
	"""
	Loads the encodings file.

	Parameters:
		encodings_input (str): location of the encodings file

	Returns:
		data if successful, -1 if unsuccessful
	"""
	try:
		print("[INFO] loading encodings...")
		data = pickle.loads(open(encodings_input, "rb").read())
	except:
		print("[INFO] could not load encodings.")
		return -1
	return data

def load_image(image_input):
	"""
	Loads the image file and converts it from BGR to RGB for
	use by dlib.

	Parameters:
		image_input (str): the location of the image file

	Returns:
		(image, rgb): the image and its RGB equivalent
		-1 if unsuccessful
	"""
	
	# Load the input image, convert from BGR to RGB
	try:
		print("[INFO] opening image...")
		image = cv2.imread(image_input)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	except:
		print("[INFO] could not open image.")
		return -1
	return (image, rgb)

def identify(data, image, rgb):
	"""
	Locates the faces in the image and finds the best match for
	each of the faces in the dataset.

	Parameters:
		data: the dataset of known faces
		image: the image/frame being processed
		rgb: the RGB version of the image for use by dlib

	Returns:
		rois[((top,right,bottom,left),name)]: an array containing
		tuples, paiting the bounding box of the detected face with
		the associated name
	"""
	detection_method = "hog"

	# Locate the faces in the image, embed them
	print("[INFO] recognizing faces...")
	boxes = face_recognition.face_locations(rgb, model=detection_method)
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Initialize the list of names for each face detected
	names = []
	
	# Loop over the facial embeddings
	for encoding in encodings:
		name = match_face(data,encoding)
		# Update the list of names
		names.append(name)
	
	rois = []
	# Loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		rois.append(((top,right,bottom,left), name))

	return rois

def match_face(data, encoding):
	"""
	Given a single encoding, finds the best match from
	each of the faces in the dataset.

	Parameters:
		data: the dataset of known faces
		encoding: the face encoding being processed

	Returns:
		name(str): the name that best matches the given face

		-1 if unsuccessful
	"""
	# Attempt to match each face in the input image to the known faces
	matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance)
	name = "?"

	# Check to see if there is a match
	if True in matches:
		# Find the indexes of all matched faces
		# Initialize dictionary to count the total number of times each face was matched
		matchedIdxs = [i for (i, b) in enumerate(matches) if b]
		counts = {}

		# Loop over the matched indexes and maintain a count for each recognized face
		for i in matchedIdxs:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1
		# Use the recognized face with most votes
		name = max(counts, key=counts.get)
	return name
