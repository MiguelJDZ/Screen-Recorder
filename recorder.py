import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

class ScreenRecorder:
    def __init__(self, master):
        self.master = master
        master.title("Screen Recorder")
        master.geometry("400x200")
        
        self.style = ttk.Style()
        self.style.configure("TButton", font=("calibri", 12), padding=10)
        self.style.configure("TLabel", font=("calibri", 14), padding=10)
        self.style.configure("TFrame", background="#ffffff")
        
        self.frame1 = ttk.Frame(master)
        self.frame1.pack(pady=20)
        
        self.label = ttk.Label(self.frame1, text="Press the Start button to begin recording.")
        self.label.pack()

        self.frame2 = ttk.Frame(master)
        self.frame2.pack(pady=10)
        
        self.start_button = ttk.Button(self.frame2, text="Start", command=self.start_recording)
        self.start_button.pack(side="left")

        self.stop_button = ttk.Button(self.frame2, text="Stop", command=self.stop_recording, state="disable")
        self.stop_button.pack(side="right")

        self.reset_button = ttk.Button(self.frame2, text="Reset", command=self.reset, state="disable")
        self.reset_button.pack(side="right", padx=5)
        
        self.frame3 = ttk.Frame(master)
        self.frame3.pack(pady=10)
        
        self.progress = ttk.Progressbar(self.frame3, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack()

        self.filename = ""
        self.frames = []
        self.screen_size = (pyautogui.size())
        self.fps = 20.0
        self.recording = False
        self.out = None

    def start_recording(self):
        self.start_button["state"] = "disable"
        self.stop_button["state"] = "normal"
        self.reset_button["state"] = "disable"
        self.label["text"] = "Recording in progress..."

        self.filename = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi"), ("All Files", "*.*")])
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.filename, fourcc, self.fps, self.screen_size)
        self.recording = True
        self.frames = []
        self.progress.start()
        self.update()
        
    def stop_recording(self):
        self.recording = False
        self.progress.stop()
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disable"
        self.reset_button["state"] = "normal"
        self.label["text"] = "Recording stopped. File saved at: " + self.filename
        messagebox.showinfo("Recording stopped", "File saved at: " + self.filename)
        self.out.release()

    def reset(self):
        self.label["text"] = "Press the Start button to begin recording."
        self.progress["value"] = 0
        self.frames = []
        self.filename = ""
        self.recording = False
        self.start_button["state"] = "normal"
        self.reset_button["state"] = "disable"
        if self.out is not None:
            self.out.release()
        
    def update(self):
        if self.recording:
            img = ImageGrab.grab()
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            self.frames.append(frame)
            self.out.write(frame)
            self.master.after(int(1000/self.fps), self.update)

root = tk.Tk()
recorder = ScreenRecorder(master=root)
root.mainloop()
