from PIL import ImageTk, Image, ImageColor
import cv2
from tkinter import StringVar, IntVar, DoubleVar

class Frame():
    # Class to convert output images into suitable format
    # for display by tk.Label in the GUI
    def __init__(self):
        self.image = None

    def get(self):
        return self.image

    def set(self, new):
        image = cv2.cvtColor(new, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((1000,600))
        image = ImageTk.PhotoImage(image)
        self.image = image
        return

# Image to be shown in gui.output (tk.Label)
current_frame = Frame()

# Info text for bottom right corner
current_info = None

# Tolerance for the facial detection
# Lower = more strict, Higher = more lax
# Default 0.45
tolerance = 0.45
tolerance_default = 0.45

# Number of frames to skip in between facial detections
# Higher = faster performance, less accurate
# Lower = slower performance, more accurate
# Default 15
skip_frames = 15
skip_frames_default = 15


class LabelColor():
    def __init__(self):
        self.bgr = (157,20,255)
        self.hex = "#ff149d"
    
    def set_hex(self, hex):
        self.hex = hex
        # Convert to RGB, then convert again to BGR
        rgb = ImageColor.getcolor(hex, "RGB")
        self.bgr = (rgb[2], rgb[1], rgb[0])

        return

# BGR value of the labels drawn to frame
# Default 157,20,255 (it's pink)
label_color = LabelColor()
label_color_default = LabelColor()

# Include rectangles drawn around face ROIs on output
# Default True
draw_rects = True