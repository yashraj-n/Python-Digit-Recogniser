from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import Image, ImageGrab
import numpy as np

model = load_model('model.h5')


def predict(img):
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img/255
    res = model.predict([img])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Digit Recognition")

        self.x = self.y = 0
        self.canvas = tk.Canvas(
            self, width=300, height=300, bg='white', cursor='cross')
        self.label = tk.Label(self, text='Draw a digit',
                              font=('Helvetica', 16))
        self.classify_btn = tk.Button(
            self, text='Recognize', command=self.classify_handwriting)
        self.clear_btn = tk.Button(self, text='Clear', command=self.clear_all)
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, sticky=W, )
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.clear_btn.grid(row=1, column=1, pady=2,)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        digit, acc = predict(ImageGrab.grab(rect))
        self.label.config(text='Recognized as ' +
                          str(digit) + ' with accuracy ' + str(acc * 100))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(
            self.x-r, self.y-r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
