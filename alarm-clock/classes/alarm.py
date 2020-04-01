import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
from .alarm_sound import AlarmSound


class Alarm(tk.Frame):
    def __init__(self, parent, time, repeat, sound, message, active):
        self.time = time        # Time for alarm to go off
        self.repeat = repeat    # Days of the week that alarm will go off, else One
        self.sound = sound      # Path to sound that will play when alarm goes off
        self.active = active    # Boolean value whether alarm will go off at time
        self.message = message  # Message that shows when alarm goes off
        tk.Frame.__init__(self, parent)
        self.add_widgets()
        self.configure(borderwidth=1, relief=tk.RAISED, background="black")

    def add_widgets(self):
        days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.active_var = tk.StringVar(value=self.active)
        self.repeat_var = tk.StringVar(value=days)
        self.message_var = tk.StringVar(value=self.message)

        self.label_frame = tk.Frame(self)
        self.alarm_label = tk.Label(self.label_frame, text=self.time,
                                    relief=tk.RAISED,
                                    font=Font(family='Helvetica', size=36,
                                              weight='bold'))
        self.message_frame = tk.LabelFrame(self.label_frame,
                                           text="Alarm Message:")
        self.message_box = tk.Text(self.message_frame, wrap="word",
                                   height=3, width=15, relief=tk.RAISED)
        self.active_frame = tk.Frame(self)
        self.alarm_repeat = tk.Listbox(self.active_frame, height=0,
                                       listvariable=self.repeat_var,
                                       selectmode="extended", relief=tk.RAISED)
        self.active_button = tk.Checkbutton(self.active_frame, text="Active?",
                                            variable=self.active_var,
                                            relief=tk.RAISED)

        self.edit_frame = tk.Frame(self)
        self.edit_button = tk.Button(self.edit_frame, text="Edit", command=self.edit_alarm)
        self.delete_button = tk.Button(self.edit_frame, text="Delete", command=self.destroy)
        self.test_button = tk.Button(self.edit_frame, text="Test", command=self.play_sound)

        self.label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.alarm_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.message_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=2)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.edit_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.delete_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.test_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.active_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.alarm_repeat.pack(side=tk.TOP, expand=1)

    def play_sound(self):
        self.alarm_sound = AlarmSound(self, set_window=True)
 
    def edit_alarm(self):
        self.edit_window = tk.Toplevel(self)
        self.save_button = tk.Button(self.edit_window, text="Save", command=self.confirm_edit)
        self.cancel_button = tk.Button(self.edit_window, text="Cancel", command=self.edit_window.destroy)
        self.save_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def confirm_edit(self):
        self.confirm = messagebox.askyesno(message="Are you sure you want to complete this action?", icon="question", title="Confirm Action",
                            default="yes")
        if self.confirm == "yes":
            self.alarm_label["text"] = ""
        else:
            self.edit_window.destroy()
