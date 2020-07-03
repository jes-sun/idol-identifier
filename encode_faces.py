
import imutils
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import global_vars

def encode_faces(dataset, encodings_output):
	########################################
	"""
	Takes the location of an image dataset directory and an 
	output file and encodes the associated faces+names to the file

	Parameters:
		dataset (str): the location of the image directory
		encodings_output (str): the name/location of the output file

	Returns:
		1 if successful, -1 if unsuccessful
	"""
	########################################
	# Delete old encodings if file already exists
	if os.path.exists(encodings_output):
		os.remove(encodings_output)

	# Grab the paths to the input images
	print("[INFO] quantifying faces...")
	image_paths = list(paths.list_images(dataset))

	# Initialize the list of known encodings and known names
	known_encodings = []
	known_names = []


	# Loop over image paths
	for (i, image_path) in enumerate(image_paths):

		# Extract the person name from the image path
		name = image_path.split(os.path.sep)[-2]
		print("[INFO] processing image {}/{} : {}".format(i + 1, len(image_paths), name))
		try:
		# Load input image, resize smaller, convert from BGR to RGB
			image = cv2.imread(image_path)
			w = image.shape[1]
			if w > 500:
				image = imutils.resize(image, width=500)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		except:
			print("[INFO] could not open image.")
			return -1

		# Detect locations of faces in image
		boxes = face_recognition.face_locations(rgb, model="hog")

		# Compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)
	
		# Loop over the encodings
		for encoding in encodings:
			# Add each encoding and name to the set of known faces
			known_encodings.append(encoding)
			known_names.append(name)

	# Write the encodings+names to a file
	print("[INFO] serializing encodings...")
	data = {"encodings": known_encodings, "names": known_names}
	f = open(encodings_output, "wb")
	f.write(pickle.dumps(data))
	print("[INFO] encoding complete.")
	f.close()

	return 1