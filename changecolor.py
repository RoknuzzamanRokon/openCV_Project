import cv2
import numpy as np
from skimage import data
from skimage.color import rgb2hsv
import tkinter as tk
from PIL import Image, ImageTk

def show_frame():
    # Get a frame from the camera
    _, frame = cap.read()

    # Convert the frame to a format that can be displayed in Tkinter
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)

    # Update the label with the new frame
    label.config(image=img)
    label.image = img

    # Schedule the next frame to be displayed
    label.after(10, show_frame)

def change_hair_color():
    # Get a frame from the camera
    _, frame = cap.read()

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of hair color in HSV color space
    lower_hair = np.array([0, 20, 70])
    upper_hair = np.array([50, 255, 255])

    # Threshold the frame to get only the hair color
    mask = cv2.inRange(hsv_frame, lower_hair, upper_hair)

    # Change the color of the hair
    hsv_frame[np.where(mask==255)] = [0,255,255]
    frame = cv2.cvtColor(hsv_frame, cv2.COLOR_HSV2BGR)
