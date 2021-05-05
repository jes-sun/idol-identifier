# Idol Identifier (WIP)

This program uses multithreading to process single images or videos frame-by-frame. A facial recognition library is used to compare the faces in the media to a given dataset. The faces will be identified (if able to be matched to a person in the dataset) or labeled as unknown.

Currently the functions all work, but the GUI is incomplete and needs to be fully integrated with the coded features.

## Futher Information

This was coded and tested using Anaconda with Python 3 in Windows 10.

### Dependencies
  * [OpenCV for Python](https://pypi.org/project/opencv-python/) - Image processing library
    * [imutils](https://pypi.org/project/imutils/) - Convenience funtions for OpenCV
  * [Pillow](https://pypi.org/project/Pillow/) - Another image processing library
  * [face_recognition](https://pypi.org/project/face-recognition/) - Python facial recognition library
    * [dlib](http://dlib.net/) - Deep learning library used by face_recognition
  * [NumPy](https://pypi.org/project/numpy/) - Array computing library
  * [filetype](https://pypi.org/project/filetype/) - Filetype checker

