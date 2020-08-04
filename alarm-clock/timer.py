import tkinter as tk
from tkinter.font import Font
from time import sleep
from threading import Thread
try:
    from alarm_sound import AlarmSound
except ImportError:
    from .alarm_sound import AlarmSound


class Timer(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.active = False
        self.kill = False
        self.start_hours = tk.StringVar(value=0)
        self.start_minutes = tk.StringVar(value=0)
        self.start_seconds = tk.StringVar(value=0)
        self.start_hours.trace("w", self.remove_alpha)
        self.start_minutes.trace("w", self.remove_alpha)
        self.start_seconds.trace("w", self.remove_alpha)
        self.hours_left = 0
        self.minutes_left = 0
        self.seconds_left = 0
        self.time_remaining = "00:00:00"
        self.alarm_sound = None
        self.clock = None

        self.spinbox_frame = tk.Frame(self)
        self.hours_frame = tk.LabelFrame(self.spinbox_frame,
                                         text="Set starting hours:")
        self.hours_select = tk.Spinbox(self.hours_frame, from_=0, to=99,
                                       width=5, textvariable=self.start_hours,
                                       font=Font(family='Helvetica', size=36,
                                                 weight='bold'))
        self.minutes_frame = tk.LabelFrame(self.spinbox_frame,
                                           text="Set starting minutes:")
        self.minutes_select = tk.Spinbox(self.minutes_frame, from_=0, to=59,
                                         textvariable=self.start_minutes,
                                         font=Font(family='Helvetica', size=36,
                                                   weight='bold'),
                                         width=5)
        self.seconds_frame = tk.LabelFrame(self.spinbox_frame,
                                           text="Set starting seconds:")
        self.seconds_select = tk.Spinbox(self.seconds_frame, from_=0, to=59,
                                         textvariable=self.start_seconds,
                                         font=Font(family='Helvetica', size=36,
                                                   weight='bold'),
                                         width=5)

        self.button_frame = tk.Frame(self)
        self.active_button = tk.Button(self.button_frame, text="Start",
                                       command=self.start)
        self.stop_button = tk.Button(self.button_frame, text="Stop",
                                     command=self.stop)

        self.spinbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.seconds_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.hours_select.pack(fill=tk.BOTH, expand=1)
        self.minutes_select.pack(fill=tk.BOTH, expand=1)
        self.seconds_select.pack(fill=tk.BOTH, expand=1)

        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.stop_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.thread = Thread(target=self.update, daemon=True)

    def remove_alpha(self, var, index, mode):
        if str(var) == "PY_VAR0":
            current = str(self.start_hours.get())
            self.start_hours.set("".join(x for x in current if x.isdigit()))
            if str(current) == "":
                self.start_hours.set(0)
        if str(var) == "PY_VAR1":
            current = str(self.start_minutes.get())
            self.start_minutes.set("".join(x for x in current if x.isdigit()))
            current = self.start_minutes.get()
            if str(current) == "":
                self.start_minutes.set(0)
            elif int(current) > 59:
                self.start_minutes.set(59)
        if str(var) == "PY_VAR2":
            current = self.start_seconds.get()
            self.start_seconds.set("".join(x for x in current if x.isdigit()))
            current = str(self.start_seconds.get())
            if str(current) == "":
                self.start_seconds.set(0)
            elif int(current) > 59:
                self.start_seconds.set(59)

    def update(self):
        while True:
            if self.kill:
                break
            if self.active:
                if self.hours_left + self.minutes_left + self.seconds_left != 0:
                    self.update_clock()
                    sleep(1)
                    if self.seconds_left > 0:
                        self.seconds_left -= 1
                    elif self.seconds_left <= 0:
                        if self.minutes_left > 0:
                            self.seconds_left = 59
                            self.minutes_left -= 1
                        elif self.minutes_left <= 0:
                            if self.hours_left > 0:
                                self.minutes_left = 59
                                self.hours_left -= 1
                else:
                    self.active = False
                    self.time_remaining = "00:00:00"
                    self.clock["text"] = self.time_remaining
                    self.active_button.pack_forget()
                    self.alarm_sound = AlarmSound(self)

    def update_clock(self):
        if len(str(self.seconds_left)) == 1:
            self.seconds_left = "0" + str(self.seconds_left)
        if len(str(self.minutes_left)) == 1:
            self.minutes_left = "0" + str(self.minutes_left)
        if len(str(self.hours_left)) == 1:
            self.hours_left = "0" + str(self.hours_left)

        hours = self.hours_left
        minutes = self.minutes_left
        seconds = self.seconds_left
        self.time_remaining = f"{hours}:{minutes}:{seconds}"
        self.clock["text"] = self.time_remaining

        if isinstance(self.seconds_left, str):
            self.seconds_left = int(self.seconds_left)
        if isinstance(self.minutes_left, str):
            self.minutes_left = int(self.minutes_left)
        if isinstance(self.hours_left, str):
            self.hours_left = int(self.hours_left)

    def start(self):
        self.hours_left = int(self.start_hours.get())
        self.minutes_left = int(self.start_minutes.get())
        self.seconds_left = int(self.start_seconds.get())
        self.spinbox_frame.pack_forget()
        self.button_frame.pack_forget()
        self.active_button.pack_forget()
        self.stop_button.pack_forget()
        self.clock = tk.Label(self, text=self.time_remaining,
                              font=Font(family='Helvetica', size=36,
                                        weight='bold'))
        self.active = True
        self.active_button.config(text="Pause", command=self.pause)
        self.clock.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.stop_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def resume(self):
        self.active = True
        self.active_button.config(text="Pause", command=self.pause)

    def pause(self):
        self.active = False
        self.active_button.config(text="Resume", command=self.resume)

    def stop(self):
        if self.active is False:
            self.start_hours.set(0)
            self.start_minutes.set(0)
            self.start_seconds.set(0)
        self.active = False
        if self.alarm_sound is not None:
            self.alarm_sound.stop_sound()
            self.alarm_sound = None
        if self.clock is not None:
            self.clock.pack_forget()
        self.button_frame.pack_forget()
        self.active_button.pack_forget()
        self.stop_button.pack_forget()
        self.active_button.config(text="Start", command=self.start)

        self.spinbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.hours_select.pack(fill=tk.BOTH, expand=1)
        self.minutes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_select.pack(fill=tk.BOTH, expand=1)
        self.seconds_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.seconds_select.pack(fill=tk.BOTH, expand=1)

        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.stop_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x150")
    root.minsize(500, 150)
    root.title("Timer")
    timer = Timer(root)
    timer.pack(fill=tk.BOTH, expand=1)
    timer.thread.start()
    root.mainloop()