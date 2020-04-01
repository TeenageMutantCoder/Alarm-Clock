import tkinter as tk
from tkinter.font import Font
from time import sleep
from threading import Thread


class Stopwatch(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.saved = []
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.time = "00:00:00"
        self.active = False
        self.kill = False
        self.clock = tk.Label(self, text=str(self.time),
                              font=Font(family='Helvetica', size=36,
                                        weight='bold'))
        self.active_button = tk.Button(self, text="Start", command=self.start)
        self.restart_button = tk.Button(self, text="Restart",
                                        command=self.restart)
        self.save_button = tk.Button(self, text="Save time", command=self.save)
        self.clear_button = tk.Button(self, text="Clear times",
                                      command=self.clear)
        self.saved_canvas = tk.Canvas(self, width=150)
        self.saved_frame = tk.LabelFrame(self.saved_canvas, text="Saved Times:")
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL,
                                      command=self.saved_canvas.yview)

        self.clock.grid(row=0, column=0, columnspan=4, sticky="NSEW")
        self.active_button.grid(row=1, column=0, sticky="NSEW")
        self.restart_button.grid(row=1, column=1, sticky="NSEW")
        self.clear_button.grid(row=1, column=3, sticky="NSEW")
        self.save_button.grid(row=1, column=2, sticky="NSEW")
        self.saved_canvas.grid(row=0, column=4, rowspan=2, sticky="NS")
        self.scrollbar.grid(row=0, column=6, rowspan=2, sticky="NS")

        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)

        self.thread = Thread(target=self.update, daemon=True)

    def update(self):
        while True:
            if self.kill:
                break
            if self.active:
                if self.seconds < 59:
                    self.seconds += 1
                elif self.seconds == 59:
                    self.seconds = 0
                    self.minutes += 1
                    if self.minutes == 60:
                        self.minutes = 0
                        self.hours += 1
                if self.minutes == 60:
                    self.minutes == 0
                    self.hours += 1
                if len(str(self.seconds)) == 1:
                    self.seconds = "0" + str(self.seconds)
                if len(str(self.minutes)) == 1:
                    self.minutes = "0" + str(self.minutes)
                if len(str(self.hours)) == 1:
                    self.hours = "0" + str(self.hours)
                self.time = f"{self.hours}:{self.minutes}:{self.seconds}"
                self.clock["text"] = self.time
                if isinstance(self.seconds, str):
                    self.seconds = int(self.seconds)
                if isinstance(self.minutes, str):
                    self.minutes = int(self.minutes)
                if isinstance(self.hours, str):
                    self.hours = int(self.hours)
                sleep(1)

    def start(self):
        self.active = True
        self.active_button.config(text="Pause", command=self.pause)

    def pause(self):
        self.active = False
        self.active_button.config(text="Start", command=self.start)

    def restart(self):
        self.active = False
        self.time = "00:00:00"
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.clear()
        self.active_button.config(text="Start", command=self.start)
        self.clock["text"] = str(self.time)

    def save(self):
        self.saved.append(self.time)
        num = len(self.saved)
        savedTime = tk.Label(self.saved_frame,
                             text=f"Time #{num} - {self.saved[-1]}")
        savedTime.grid(row=len(self.saved), column=0, sticky="EW")
        self.saved_canvas.delete("saved")
        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)

    def clear(self):
        self.saved = []
        self.saved_frame.destroy()
        self.saved_frame = tk.LabelFrame(self.saved_canvas, text="Saved Times:")
        self.saved_canvas.delete("saved")
        self.saved_canvas.create_window(0, 0, anchor='nw', tags="saved",
                                        window=self.saved_frame)
        self.saved_canvas.update_idletasks()
        self.saved_canvas.configure(scrollregion=self.saved_canvas.bbox('all'),
                                    yscrollcommand=self.scrollbar.set)
