import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.colorchooser
from PIL import ImageTk, Image, ImageColor, UnidentifiedImageError
import encode_faces
import cv2
import global_vars
import tracker
import filetype


# Identify menu commands
def ask_file_image():
    global output
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

        status = tracker.face_tracker_image(current_dataset.get(), path, output_file)
       
        if status == -1:
            raise UnidentifiedImageError

        output_image = global_vars.current_frame.get()
        global_vars.current_info.set("[INFO] image saved as {}".format(output_file))

        output.configure(image=output_image)
        output.image = output_image
        #output.pack(side="top", fill="both", expand="yes")
    except UnidentifiedImageError:
        tk.messagebox.showerror("Invalid image file", "The selected file is not a valid image file.", parent=root)
        return
    except AttributeError:
        pass
    return

def ask_file_video():
    try:
        if not current_dataset.get():
            tk.messagebox.showwarning("No dataset selected", "A face encodings dataset needs to be chosen before identifying faces in a video.", parent=root)
            return

        path = tk.filedialog.askopenfilename()
        if not path:
            return
        check = filetype.is_video(path)
        if check == False:
            print(check)
            raise TypeError

        name = tk.simpledialog.askstring("Image", "Name of output video (do not include file extension)", parent=root)
        if name:
            output_file = name + ".avi"
        else:
            output_file = "output_video.avi"

        tk.messagebox.showinfo("Video Processing", "Preview of video will be shown in a new window while it is processing. Once the preview is finished, the completed video will be saved to disk.")

        output.configure(image=None, text="Preview shown in new window")
        global_vars.current_info.set("[INFO] video processing...")

        status = tracker.face_tracker_video(current_dataset.get(), path, output_file)

        if status == -1:
            raise Exception

        tk.messagebox.showinfo("Procesing complete", "Facial recognition for the video has been completed. Output saved as {}.".format(output_file))

        global_vars.current_info.set("[INFO] video saved as {}".format(output_file))
    except TypeError:
        tk.messagebox.showerror("Invalid video file", "The selected file is not a valid video file.", parent=root)
        return
    return


# Dataset menu commands
def ask_file_encode():
    try:
        dataset = tk.filedialog.askdirectory(mustexist=True)
        if not dataset:
            return
        name = tk.simpledialog.askstring("Dataset", "Name of dataset", parent=root)
        if name:
            encodings_output = name + "_encodings.pickle"
        else:
            output = "encodings.pickle"


        loading = tk.messagebox.showinfo("Encoding...", "Dataset will now be encoded.", parent=root)
        
        encode_faces.encode_faces(dataset, encodings_output)
        
        if status == 1:
            complete = tk.messagebox.showinfo("Encoding", "Encoding successful. Saved as {}.".format(encodings_output), parent=root)
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
            tk.messagebox.showwarning("Invalid encodings file","The selected file is not a useable encodings file.", parent=root)
            return
        else:
            current_dataset.set(new_dataset)
            global_vars.current_info.set("[INFO] dataset selected.")
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

# Settings menu
def show_settings():
    global tolerance_temp
    global interval_temp
    global color_temp
    global rects_temp

    global color_select
    global rects_select
    global settings
    settings = tk.Toplevel()
    settings.title("Settings")
    
    tolerance_frame = tk.LabelFrame(settings, text="Tolerance")
    tolerance_temp = tk.DoubleVar(value=global_vars.tolerance)
    tolerance_frame.grid(column=0, row=0, padx=15, pady=6, columnspan=2)
    tolerance_desc = tk.Label(tolerance_frame, text="Tolerance level for the facial recognition.\nA lower number is more strict when determining whether or not a face matches someone in the dataset.", justify="left", padx=15,pady=15)
    tolerance_desc.grid()
    tolerance_select = tk.Spinbox(tolerance_frame, from_=0, to=1, increment=0.05, textvariable=tolerance_temp)
    tolerance_select.grid(padx=6, pady=15)

    interval_frame = tk.LabelFrame(settings, text="Tracking Interval")
    interval_temp = tk.IntVar(value=global_vars.skip_frames)
    interval_frame.grid(column=0, row=1,padx=15, pady=6, columnspan=2)
    interval_desc = tk.Label(interval_frame, text="Interval of frames at which to conduct facial recognition during videos.\nA lower number will result in smoother and more frequent tracking, but processing will take longer.", justify="left", padx=15, pady=15)
    interval_desc.grid()
    interval_select = tk.Spinbox(interval_frame, from_=0, to=30, increment=1, textvariable=interval_temp)
    interval_select.grid(padx=6, pady=15)

    color_frame = tk.LabelFrame(settings, text="Label Colour")
    color_temp = global_vars.label_color.hex
    color_frame.grid(column=0, row=2, padx=15, pady=6)
    color_desc = tk.Label(color_frame, text="Colour of identification labels on output.", justify="left", padx=15, pady=15)
    color_desc.grid()
    color_select = tk.Button(color_frame, text="Choose new label colour", command=settings_color, bg=color_temp)
    color_select.grid(padx=6, pady=15)

    rects_frame = tk.LabelFrame(settings, text="Rectangles")
    rects_temp = tk.IntVar(value=int(global_vars.draw_rects))
    rects_frame.grid(column=1, row=2, padx=15, pady=6)
    rects_desc = tk.Label(rects_frame, text="Enable or disable the drawing of rectangles around faces.", justify="left", padx=15, pady=15)
    rects_desc.grid()
    rects_select = tk.Checkbutton(rects_frame, text="Rectangles", variable=rects_temp, bg=color_temp, relief="raised")
    rects_select.grid(padx=6, pady=15)

    button_frame = tk.Frame(settings)
    button_frame.grid(column=0, row=4, pady=15, columnspan=2)
    button_save = tk.Button(button_frame, text="Save changes", command=settings_save)
    button_save.grid(column=0, row=0, padx=5, pady=5)
    button_cancel = tk.Button(button_frame, text="Cancel", command=settings.destroy)
    button_cancel.grid(column=1,row=0, padx=5, pady=5)
    button_defaults = tk.Button(button_frame, text="Reset to defaults", command=settings_default)
    button_defaults.grid(column=0, row=1, columnspan=2)

def settings_save():
    global tolerance_temp
    global interval_temp
    global color_temp
    global rects_temp
    global settings
    global_vars.tolerance = tolerance_temp.get()
    global_vars.skip_frames = interval_temp.get()
    global_vars.label_color.set_hex(color_temp)
    global_vars.draw_rects = rects_temp == 1

    global_vars.current_info.set("[INFO] settings saved.")
    settings.destroy()
    return

def settings_default():
    global_vars.tolerance = global_vars.tolerance_default
    global_vars.skip_frames = global_vars.skip_frames_default
    global_vars.label_color = global_vars.label_color_default
    global_vars.draw_rects = True

    global_vars.current_info.set("[INFO] settings returned to default.")
    settings.destroy()
    return

def settings_color():
    global color_temp
    global color_select
    global rects_select
    color_hex = tk.colorchooser.askcolor(title="Choose new label colour", parent=settings)[1]
    color_temp = color_hex
    color_select.configure(bg=color_hex)
    rects_select.configure(bg=color_hex)
    return

# Frames
def build_gui(root):
    global current_dataset
    global output
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
    global_vars.current_info = tk.StringVar()
    show_current_info = tk.Label(info_frame, textvariable=global_vars.current_info)
    show_current_info.pack(side="right")
    info_frame.pack(side="right")
    return

# Menu bar
def build_menu(root):
    menubar = tk.Menu(root)

    dataset_menu = tk.Menu(menubar, tearoff=0)
    dataset_menu.add_command(label="Choose face dataset file", command=ask_file_dataset)
    dataset_menu.add_command(label="Encode face dataset file", command=ask_file_encode)
    dataset_menu.add_separator()
    dataset_menu.add_command(label="Help", command=show_help_dataset)
    menubar.add_cascade(label="Dataset", menu=dataset_menu)

    identify_menu = tk.Menu(menubar, tearoff=0)
    identify_menu.add_command(label="Identify from image", command=ask_file_image)
    identify_menu.add_command(label="Identify from video", command=ask_file_video)
    menubar.add_cascade(label="Identify", menu=identify_menu)

    menubar.add_command(label="Settings", command=show_settings)

    root.config(menu=menubar)

    return
    
# Window activities
root = tk.Tk()
current_dataset = tk.StringVar()
build_gui(root)
build_menu(root)
root.title("Idol Identifier")

root.mainloop()


