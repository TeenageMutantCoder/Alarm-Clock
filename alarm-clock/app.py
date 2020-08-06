#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk   # Allows for window icon
from PIL import Image     # Allows for window icon
from threading import Thread
from os.path import relpath
try:
    from clock import Clock
    from alarms import Alarms
    from stopwatch import Stopwatch
    from timer import Timer
except ImportError:
    from .clock import Clock
    from .alarms import Alarms
    from .stopwatch import Stopwatch
    from .timer import Timer


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
        image_path = relpath("alarm-clock/assets/pictures/icon_2.ico")
        image = ImageTk.PhotoImage(file=image_path)
        self.iconphoto(False, image)

    def add_widgets(self):
        # Tabbed view
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.notebook.bind("<<NotebookTabChanged>>", self.manage_threads)

        # First Tab: Alarms
        self.alarms = Alarms(self.notebook)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.alarms.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(self.alarms, text="Alarms")

        # Second Tab: Clock (Hopefully will add analog and digital)
        self.clock = Clock(self.notebook)
        self.clock.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(self.clock, text="Clock")

        # Third Tab: Stopwatch
        self.stopwatch = Stopwatch(self.notebook)
        self.stopwatch.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(self.stopwatch, text="Stopwatch")

        # Fourth Tab: Timer
        self.timer = Timer(self.notebook)
        self.timer.pack(fill=tk.BOTH, expand=1)
        self.notebook.add(self.timer, text="Timer")

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

    def on_close(self):
        self.alarms.db.close()
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App(600, 185)
    app.start()
