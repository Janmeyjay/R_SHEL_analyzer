import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
import pickle
import glob
import threading

# Global variables
image_window = None
processing_flag = False
file_path = ""
image_list = []
data_dict = {}
current_window_name = None

#Helper functions

# Function to rotate the image by the given angle
def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

#Function to show the image in a separate window
def show_image(image, window_name):
    global image_window
    if image_window is not None:
        cv2.destroyWindow(image_window)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow(window_name, image)
    image_window = window_name

    # Set the maximum size for the window
    max_width, max_height = 1200, 800
    cv2.resizeWindow(window_name, min(image.shape[1], max_width), min(image.shape[0], max_height))

# Function to browse and select a folder containing images and data files
def browse_folder():
    global file_path, image_list, data_dict
    file_path = filedialog.askdirectory()
    trimmed_path_start = file_path[:3]  # Trim the file path to first 3 characters
    trimmed_path = file_path[-20:]      # Trim the file path to last 20 characters
    folder_path_label.config(text=f"{trimmed_path_start}...{trimmed_path}")
    image_list = sorted(glob.glob(f"{file_path}/img0_0_*.png"), key=lambda x: int(x.strip(f'{file_path}')[8:-4]))
    data_dict = glob.glob(f"{file_path}/data.sav")
    data_dict = pickle.load(open(data_dict[0], 'rb'))

# Function to calculate the center of mass and intensity of the image
def scipy_center(img):
    centers = ndi.measurements.center_of_mass(img)
    intensity = ndi.mean(img)
    return centers, intensity

# Function to get the center of the region of interest
def get_center(x_cent, y_cent, roi, y_shift, x_shift):
    # Function to get the center of the region of interest
    img_no = int(img_no_var.get())
    if img_no < 0 or img_no >= len(image_list):
        messagebox.showerror("Invalid Input", "Invalid image number")
        return

    selected_image_path = image_list[img_no]
    image = cv2.imread(selected_image_path)
    # show_image(image, 'Image')
    cv2.imshow("Image",image)
    x_cent = int(x_cent_entry.get())
    y_cent = int(y_cent_entry.get())
    print(y_cent - roi + y_shift, y_cent + roi + y_shift)
    crop_img = image[(y_cent - roi + y_shift):(y_cent + roi + y_shift), (x_cent - roi + x_shift):(x_cent + roi + x_shift)]
    cv2.imshow("Crop", crop_img)
    inp = messagebox.askquestion("Confirm", "Do you want to proceed with the selected center pixel?")
    if inp == "yes":
        cv2.destroyAllWindows()
        return x_cent, y_cent, selected_image_path
    else:
        messagebox.showerror("Error","Please enter the correct center pixels")
        return None

# Function to process the images and save the processed data
def process_images():
    global processing_flag
    try:
        processing_flag = True
        global image_list

        roi = int(roi_var.get())
        y_shift = int(y_shift_var.get())
        x_shift = int(x_shift_var.get())

        center_data= get_center(int(x_cent_entry.get()), int(y_cent_entry.get()), roi, y_shift,x_shift)
        if center_data is None:
            processing_flag = False
            return

        x_cent, y_cent, selected_image_path = center_data

        # Initialize lists to store the processed data
        center_list = {'x': [], 'y': [], 'intensity': []}

        fig, axs = plt.subplots(1, 3, figsize=(12, 4))

        # Image processing loop
        for i, img_path in enumerate(image_list):
            if not processing_flag:
                break 
            image = cv2.imread(img_path)
            image = rotate_image(image, int(angle_var.get()))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh1 = cv2.threshold(image, 1, 255, cv2.THRESH_TOZERO)

            if img_path == selected_image_path:
                crop_img = image[(y_cent - roi + y_shift):(y_cent + roi + y_shift), (x_cent - roi + x_shift):(x_cent + roi + x_shift)]
            else:
                crop_img = image[(y_cent - roi + y_shift):(y_cent + roi + y_shift), (x_cent - roi + x_shift):(x_cent + roi + x_shift)]

            cent, intensity = scipy_center(crop_img)
            center_list['x'].append(float(cent[0]))
            center_list['y'].append(float(cent[1]))
            center_list['intensity'].append(float(intensity))

            axs[0].clear()
            axs[1].clear()
            axs[2].clear()
            axs[0].plot(data_dict['analyser positions'][:i], center_list['x'][:i], color='orange')
            axs[1].plot(data_dict['analyser positions'][:i], center_list['y'][:i], color='green')
            axs[2].plot(data_dict['analyser positions'][:i], center_list['intensity'][:i], color='blue')
            axs[0].set_title('x_shift')  # Set title for x_shift subplot
            axs[1].set_title('y_shift')  # Set title for y_shift subplot
            axs[2].set_title('intensity')  # Set title for intensity subplot

            plt.pause(0.05)

            with open(f"{file_path}/{file_name_var.get()}.dat", 'a', encoding='utf-8') as f:
                f.write(f"{np.round(data_dict['analyser positions'][i], 3)}\t {np.round(center_list['x'][i], 2)} \t {np.round(center_list['y'][i], 2)} \t {np.round(center_list['intensity'][i], 2)} \n")
        messagebox.showinfo("Process Completed", "Image processing completed successfully!")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
    
    finally:
        processing_flag = False  # Set the flag to False after the loop is done or an error occurs

# Function to create the "About" tab content
def create_about_tab(frame):
    about_tab = ttk.Frame(frame)
    tab_control.add(about_tab, text="About")

    about_label = tk.Label(about_tab, text="This is a image processing application for Retro SHEL.\n\n"
                                           "Select a folder containing images, then enter the central image number,\n "
                                           "x and y center, region of interest, shift, and angle of rotation.\n\n"
                                           "Click the 'Process Images' button to start the image processing.\n\n"
                                           "The processed data will be saved in a file with the given name.\n\n"
                                           "Note: Ensure the entered values are correct before\n" 
                                           "proceeding with the image processing.\n\n\n\n"
                                           "Creator: Janmey Jay panda\n"
                                           "Version: 1.0\nLisence: MIT License\n"
                                           "Copyright (c) 2023 Janmeyjay\n", bg="#f0f0f0", font=("Helvetica", 10),justify="left")
    about_label.pack(padx=20, pady=20)

# Function to create the main GUI widgets and layout
def create_main_gui(frame):
    global folder_path_label, roi_var, y_shift_var, x_shift_var, x_cent_entry,y_cent_entry, angle_var, file_name_var,img_no_var

    # Create and configure GUI widgets
    browse_button = tk.Button(frame, text="Browse Folder", command=browse_folder, bg="#008CBA", fg="white", font=("Helvetica", 10))
    folder_path_label = tk.Label(frame, text="", bg="#f0f0f0", font=("Helvetica", 10))

    file_name_label = tk.Label(frame, text="Enter data file name:", bg="#f0f0f0", font=("Helvetica", 12))
    file_name_var = tk.StringVar(value="Yshift_50_0")
    file_name_entry = tk.Entry(frame, textvariable=file_name_var, justify='center')

    img_no_label = tk.Label(frame, text="Enter central image number:", bg="#f0f0f0", font=("Helvetica", 12))
    img_no_var = tk.StringVar(value="100")
    img_no_entry = tk.Entry(frame, textvariable=img_no_var, justify='center')

    x_cent_label = tk.Label(frame, text="Enter x center:", bg="#f0f0f0", font=("Helvetica", 12))
    x_cent_entry = tk.Entry(frame, justify='center')

    y_cent_label = tk.Label(frame, text="Enter y center:", bg="#f0f0f0", font=("Helvetica", 12))
    y_cent_entry = tk.Entry(frame, justify='center')

    roi_label = tk.Label(frame, text="Enter region of Interest:", bg="#f0f0f0", font=("Helvetica", 12))
    roi_var = tk.StringVar(value="50")
    roi_entry = tk.Entry(frame, textvariable=roi_var, justify='center')

    y_shift_label = tk.Label(frame, text="Enter y_shift in region of Interest:", bg="#f0f0f0", font=("Helvetica", 12))
    y_shift_var = tk.StringVar(value="0")
    y_shift_entry = tk.Entry(frame, textvariable=y_shift_var, justify='center')

    x_shift_label = tk.Label(frame, text="Enter x_shift in region of Interest:", bg="#f0f0f0", font=("Helvetica", 12))
    x_shift_var = tk.StringVar(value="0")
    x_shift_entry = tk.Entry(frame, textvariable=x_shift_var, justify='center')

    angle_label = tk.Label(frame, text="Enter angle of rotation:", bg="#f0f0f0", font=("Helvetica", 12))
    angle_var = tk.StringVar(value="0")
    angle_entry = tk.Entry(frame, textvariable=angle_var, justify='center')

    process_button = tk.Button(frame, text="Process Images", command=process_images, bg="#008CBA", fg="white", font=("Helvetica", 12))
    stop_button = tk.Button(frame, text="Stop Image Processing", command=stop_program, bg="#FF0000", fg="white", font=("Helvetica", 12))

    # Layout the widgets using grid
    browse_button.grid(row=0, column=0, padx=10, pady=10,sticky="W")
    folder_path_label.grid(row=0, column=1, padx=5, pady=5)
    img_no_label.grid(row=1, column=0, padx=5, pady=5,sticky="W")
    img_no_entry.grid(row=1, column=1, padx=5, pady=5)
    x_cent_label.grid(row=2, column=0, padx=5, pady=5,sticky="W")
    x_cent_entry.grid(row=2, column=1, padx=5, pady=5)
    y_cent_label.grid(row=3, column=0, padx=5, pady=5,sticky="W")
    y_cent_entry.grid(row=3, column=1, padx=5, pady=5)
    roi_label.grid(row=4, column=0, padx=5, pady=5,sticky="W")
    roi_entry.grid(row=4, column=1, padx=5, pady=5)
    y_shift_label.grid(row=5, column=0, padx=5, pady=5,sticky="W")
    y_shift_entry.grid(row=5, column=1, padx=5, pady=5)
    x_shift_label.grid(row=6, column=0, padx=5, pady=5,sticky="W")
    x_shift_entry.grid(row=6, column=1, padx=5, pady=5)
    angle_label.grid(row=7, column=0, padx=5, pady=5,sticky="W")
    angle_entry.grid(row=7, column=1, padx=5, pady=5)
    file_name_label.grid(row=8, column=0, padx=5, pady=5,sticky="W")
    file_name_entry.grid(row=8, column=1, padx=5, pady=5)
    process_button.grid(row=9, column=0, padx=5, pady=5,columnspan=1)
    stop_button.grid(row=9, column=1, padx=5, pady=5, columnspan=1, sticky="W")

# Start the image processing in a separate thread
def start_processing_thread():
    processing_thread = threading.Thread(target=process_images)
    processing_thread.start()

# Function to stop the image processing when the "Stop Image Processing" button is clicked
def stop_program():
    global processing_flag
    if messagebox.askokcancel("Quit", "Do you want to quit the image processing?"):
        processing_flag = False  # Set the flag to False to stop the image processing

# Function to set up and run the main GUI
def main():
    global root, tab_control

    root = tk.Tk()
    root.title("R_SHEL Analyzer")
    root.geometry("460x400")  # Set initial window size
    root.configure(bg="#f0f0f0")  # Set background color

    # Set the path to your ICO file
    icon_path = "C:/Users/Janmey Jay/Desktop/trial_gui/R_SHEL.ico"
    root.iconbitmap(icon_path)  # Set the icon for the GUI window

    tab_control = ttk.Notebook(root)

    # Create and configure the main GUI frames
    main_frame = ttk.Frame(tab_control)
    tab_control.add(main_frame, text="Main GUI")

    # Add main GUI widgets to the main_frame
    create_main_gui(main_frame)

    # Create the "About" tab content
    create_about_tab(tab_control)

    tab_control.pack(expand=1, fill='both')

    root.mainloop()

if __name__ == "__main__":
    main()