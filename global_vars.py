from PIL import ImageTk, Image
import cv2
from tkinter import StringVar

class Frame():
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

   
current_frame = Frame()
current_info = None    
