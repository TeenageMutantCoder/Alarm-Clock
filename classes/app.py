#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk   # Allows for window icon
from PIL import Image     # Allows for window icon
from threading import Thread
from os.path import relpath
from classes.clock import Clock
from classes.alarm import Alarm
from classes.stopwatch import Stopwatch
from classes.timer import Timer


class App(tk.Tk):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        tk.Tk.__init__(self)
        self.configure_window()
        self.add_widgets()

    def configure_window(self):
        self.title("Alarm Clock")
        self.geometry(f"{self.width}x{self.height}+100+100")
        self.minsize(600, 185)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        image_path = relpath("assets/pictures/alarm_clock4.png")
        image = ImageTk.PhotoImage(Image.open(image_path))
        self.iconphoto(False, image)

    def add_widgets(self):
        # Tabbed view
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(sticky="NSEW")
        self.notebook.grid_columnconfigure(0, weight=1)
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.bind("<<NotebookTabChanged>>", self.manage_threads)

        # First Tab: Alarms
        self.alarms_canvas = tk.Canvas(self.notebook)
        self.alarms = tk.Frame(self.alarms_canvas)
        self.alarms_canvas.grid(row=0, column=0, sticky="NSEW")
        self.alarms_canvas.grid_columnconfigure(0, weight=1)
        self.alarms_canvas.grid_rowconfigure(0, weight=1)

        scrollbar = tk.Scrollbar(self.alarms_canvas, orient=tk.VERTICAL,
                                 command=self.alarms_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")

        # Creating long list of alarm frames to test scrolling and stuff
        self.alarm_frames = []
        for alarm in range(24):
            self.alarm_frames.append(Alarm(self.alarms, f"{alarm}:00",
                                           "SunMonTueWedThuFriSat", None, "",
                                           True))
        for alarm_frame in self.alarm_frames:
            alarm_frame.grid(row=self.alarm_frames.index(alarm_frame),
                             column=0, sticky="NSEW")
            alarm_frame.grid_columnconfigure(0, weight=1)
            alarm_frame.grid_columnconfigure(3, weight=1)
            alarm_frame.grid_rowconfigure(0, weight=1)
            alarm_frame.grid_rowconfigure(1, weight=1)

        self.alarms_canvas.create_window(0, 0, anchor='nw', window=self.alarms,
                                         tags="alarms")
        self.alarms_canvas.update_idletasks()
        self.alarms_canvas.configure(scrollregion=self.alarms_canvas.bbox('all'),
                                     yscrollcommand=scrollbar.set)
        self.alarms_canvas.bind("<Configure>", self.on_canvas_resize)
        self.notebook.add(self.alarms_canvas, text="Alarms")

        # Second Tab: Clock (Hopefully will add analog and digital)
        self.clock = Clock(self.notebook)
        self.clock.grid(sticky="NSEW")
        self.clock.grid_columnconfigure(0, weight=1)
        self.clock.grid_rowconfigure(0, weight=1)
        self.notebook.add(self.clock, text="Clock")

        # Third Tab: Stopwatch
        self.stopwatch = Stopwatch(self.notebook)
        self.stopwatch.grid(sticky="NSEW")
        self.stopwatch.grid_columnconfigure(0, weight=1)
        self.stopwatch.grid_rowconfigure(0, weight=8)
        self.stopwatch.grid_rowconfigure(1, weight=2)
        self.stopwatch.grid_rowconfigure(2, weight=1)
        self.notebook.add(self.stopwatch, text="Stopwatch")

        # Fourth Tab: Timer
        self.timer = Timer(self.notebook)
        self.timer.grid(sticky="NSEW")
        self.timer.grid_columnconfigure(0, weight=1)
        self.timer.grid_rowconfigure(0, weight=4)
        self.timer.grid_rowconfigure(1, weight=1)
        self.notebook.add(self.timer, text="Timer")

    def on_canvas_resize(self, event):
        for alarm_frame in self.alarm_frames:
            alarm_frame.width = self.alarms_canvas.winfo_width()
        self.alarms_canvas.delete("alarms")
        self.alarms_canvas.create_window(0, 0, anchor='nw', window=self.alarms,
                                         tags="alarms")
        self.alarms_canvas.itemconfig('alarms',
                                      height=self.alarms_canvas.winfo_height(),
                                      width=self.alarms_canvas.winfo_width())
        self.alarms_canvas.update_idletasks()

    def manage_threads(self, event):
        active_tab = self.notebook.tab(self.notebook.select(), "text")
        if active_tab == "Alarms":
            if self.clock.thread.is_alive():
                self.clock.kill = True
                self.clock.thread.join()
            elif self.stopwatch.thread.is_alive():
                self.stopwatch.kill = True
                self.stopwatch.thread.join()
            elif self.timer.thread.is_alive():
                self.timer.kill = True
                self.timer.thread.join()
        elif active_tab == "Clock":
            if self.stopwatch.thread.is_alive():
                self.stopwatch.kill = True
                self.stopwatch.thread.join()
            elif self.timer.thread.is_alive():
                self.timer.kill = True
                self.timer.thread.join()
            self.clock.kill = False
            self.clock.thread = Thread(target=self.clock.update,
                                       daemon=True)
            self.clock.thread.start()
        elif active_tab == "Stopwatch":
            if self.clock.thread.is_alive():
                self.clock.kill = True
                self.clock.thread.join()
            elif self.timer.thread.is_alive():
                self.timer.kill = True
                self.timer.thread.join()
            self.stopwatch.kill = False
            self.stopwatch.thread = Thread(target=self.stopwatch.update,
                                           daemon=True)
            self.stopwatch.thread.start()
        elif active_tab == "Timer":
            if self.clock.thread.is_alive():
                self.clock.kill = True
                self.clock.thread.join()
            elif self.stopwatch.thread.is_alive():
                self.stopwatch.kill = True
                self.stopwatch.thread.join()
            self.timer.kill = False
            self.timer.thread = Thread(target=self.timer.update,
                                       daemon=True)
            self.timer.thread.start()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App(600, 185)
    app.start()
