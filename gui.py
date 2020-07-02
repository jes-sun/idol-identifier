import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
from PIL import ImageTk, Image, UnidentifiedImageError
import encode_faces
import cv2
import global_vars
import tracker
import concurrent.futures


# Identify menu commands

def ask_file_image():
    try:
        if not current_dataset.get():
            tk.messagebox.showwarning("No dataset selected", "A face encodings dataset needs to be chosen before identifying faces in an image.", parent=root)
            return

        path = tk.filedialog.askopenfilename()
        img = ImageTk.PhotoImage(Image.open(path))
        name = tk.simpledialog.askstring("Image", "Name of output image (do not include file extension)", parent=root)
        if name:
            output_file = name + ".jpg"
        else:
            output_file = "output_image.jpg"

        tracker.face_tracker_image(current_dataset.get(), path, output_file, output_frame)

        output_image = global_vars.current_frame.get()

        output.configure(image=output_image)
        output.image = output_image
        output.pack(side="top", fill="both", expand="yes")
    except UnidentifiedImageError:
        tk.messagebox.showerror("Invalid image file", "The selected file is not a valid image file.", parent=root)
        return
    except AttributeError:
        pass
    return

# Dataset menu commands
def ask_file_encode():
    try:
        dataset = tk.filedialog.askdirectory(mustexist=True)
        if not dataset:
            return
        name = tk.simpledialog.askstring("Dataset", "Name of dataset", parent=root)
        if name:
            output = name + "_encodings.pickle"
        else:
            output = "encodings.pickle"


        loading = tk.messagebox.showinfo("Encoding...", "Dataset will now be encoded.", parent=root)
        status = encode_faces.encode_faces(dataset, output)
  
        if status == 1:
            complete = tk.messagebox.showinfo("Encoding", "Encoding successful. Saved as {}.".format(output), parent=root)
        else:
            complete = tk.messagebox.showerror("Encoding", "Encoding unsuccessful.", parent=root)
    except AttributeError:
        pass
    return

def ask_file_dataset():
    try:
        global current_dataset
        new_dataset = tk.filedialog.askopenfilename()
        if not new_dataset:
            return
        elif not new_dataset.endswith(".pickle"):
            tk.messagebox.showwarning("Invalid encodings file","This file is not a useable encodings file.", parent=root)
            return
        else:
            current_dataset.set(new_dataset)
    except AttributeError:
        pass
    return

def show_help_dataset():
    tk.messagebox.showinfo("Dataset Help",
    """
    To encode a dataset, place image files of a person inside a folder named after them. The chosen directory will contain a folder for each person you wish to identify.\n
    The dataset file will be saved in the root directory as "[name]_encodings.pickle".\n
    Once an encodings file has been created and saved to disk, you may select it for use to identify faces in an image or video file.
    """,
    parent=root)
    return
    
# Window activities
root = tk.Tk()

# Frames
main_frame = tk.Frame(root)
main_frame.pack()

output_frame = tk.LabelFrame(main_frame, width=1000, height=600)
output_frame.pack()

output = tk.Label(output_frame, padx=500, pady=300)
output.pack()

dataset_frame = tk.LabelFrame(main_frame)
dataset_frame.pack(side="left")
current_dataset = tk.StringVar()
dataset_text = tk.Label(dataset_frame, text="Current dataset: ")
dataset_text.pack(side="left")
show_current_dataset = tk.Label(dataset_frame, textvariable=current_dataset)
show_current_dataset.pack(side="left")

info_frame = tk.LabelFrame(main_frame)
current_info = tk.StringVar()
show_current_info = tk.Label(info_frame, textvariable=current_info)
show_current_info.pack(side="right")
info_frame.pack(side="right")

# Menu bar
def build_menu(root):
    menubar = tk.Menu(root)

    identify_menu = tk.Menu(menubar, tearoff=0)
    identify_menu.add_command(label="Identify from image", command=ask_file_image)
    identify_menu.add_command(label="Identify from video")
    menubar.add_cascade(label="Identify", menu=identify_menu)

    dataset_menu = tk.Menu(menubar, tearoff=0)
    dataset_menu.add_command(label="Choose face dataset file", command=ask_file_dataset)
    dataset_menu.add_command(label="Encode face dataset file", command=ask_file_encode)
    dataset_menu.add_separator()
    dataset_menu.add_command(label="Help", command=show_help_dataset)
    menubar.add_cascade(label="Dataset", menu=dataset_menu)

    root.config(menu=menubar)

    return

build_menu(root)
root.title("Idol Identifier")


root.after(1, current_info.get)
root.mainloop()


