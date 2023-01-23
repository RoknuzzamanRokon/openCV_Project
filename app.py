import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import model
import camera

class App:

    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"):

        self.window = window
        self.window_title = window_title

        self.counters = [1, 1, 1]

        self.model = model.Model()

        self.auto_predict = False

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def init_gui(self):

        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

       
        self.classname_one = simpledialog.askstring("Classname One", "Enter the name of person-1", parent=self.window)
        self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of person-2", parent=self.window)
        self.classname_three = simpledialog.askstring("Classname Three", "Enter the name of person-3", parent=self.window)

        self.btn_class_one = tk.Button(self.window, text=self.classname_one, width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text=self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)
        
        self.btn_class_three = tk.Button(self.window,text =self.classname_three,width=50,command=lambda: self.save_for_class(3))
        self.btn_class_three.pack(anchor=tk.CENTER,expand=True)

        self.btn_train = tk.Button(self.window, text="Train", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predcit", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)


        
        self.class_label = tk.Label(self.window, text="")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

        

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")
        if not  os.path.exists("3"):
            os.mkdir("3")

        cv.imwrite(f'{class_num}/frame{self.counters[class_num-2]}.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open(f'{class_num}/frame{self.counters[class_num - 2]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'{class_num}/frame{self.counters[class_num - 2]}.jpg')

        self.counters[class_num - 2] += 1

   
    def update(self):
        if self.auto_predict:
            print(self.predict())

        ret, frame = self.camera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)
        
        

        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two
        if prediction == 3:
            self.class_label.config(text=self.classname_three)
            return self.classname_three
        
     