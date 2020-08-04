import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox
try:
    from alarm_sound import AlarmSound
    from sql_connector import SqlConnector
except ImportError:
    from .alarm_sound import AlarmSound
    from .sql_connector import SqlConnector


class Alarm(tk.Frame):
    def __init__(self, parent, id, time, repeat, sound, message, active):
        self.db = SqlConnector()  # Allows for access to database
        self.id = id              # Allows for database identification
        self.time = time          # Time for alarm to go off
        self.repeat = repeat      # Days of the week that alarm will go off, else One
        self.sound = sound        # Path to sound that will play when alarm goes off
        self.active = active      # Boolean value whether alarm will go off at time
        self.message = message    # Message that shows when alarm goes off
        self.parent = parent
        self.alarm_sound = None
        tk.Frame.__init__(self, parent)
        self.add_widgets()
        self.configure(borderwidth=1, relief=tk.RAISED, background="black")

    def add_widgets(self):
        days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.active_var = tk.StringVar()
        self.active_var.set(1 if self.active == "True" else 0)
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
        self.delete_button = tk.Button(self.edit_frame, text="Delete", command=self.delete)
        self.test_button = tk.Button(self.edit_frame, text="Test", command=self.play_sound)

        self.label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.alarm_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.message_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.edit_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.edit_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.delete_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.test_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.active_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.alarm_repeat.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def delete(self):
        self.db.delete(self.id)
        if __name__ != "__main__":
            self.parent.parent.parent.parent.add_alarms()
        self.destroy()

    def play_sound(self):
        self.alarm_sound = AlarmSound(self, set_window=True)
 
    def edit_alarm(self):
        self.edit_window = tk.Toplevel(self)
        self.new_hr = tk.StringVar()
        self.new_min = tk.StringVar()
        self.am_pm = tk.StringVar()
        self.new_active = tk.StringVar()
        self.am_pm.set(0)

        self.edit_frame = tk.Frame(self.edit_window)
        self.spinbox_frame = tk.Frame(self.edit_frame)
        self.hours_frame = tk.LabelFrame(self.spinbox_frame,
                                         text="Set hour:")
        self.hours_select = tk.Spinbox(self.hours_frame, from_=1, to=12, 
                                       textvariable=self.new_hr, width=5, 
                                       font=Font(family='Helvetica', size=36,
                                                 weight='bold'))
        self.minutes_frame = tk.LabelFrame(self.spinbox_frame,
                                           text="Set minute:")
        self.minutes_select = tk.Spinbox(self.minutes_frame, from_=0, to=59,
                                         textvariable=self.new_min, width=5,
                                         font=Font(family='Helvetica', size=36,
                                                 weight='bold'))
        self.am_pm_frame = tk.LabelFrame(self.spinbox_frame,
                                           text="Set Am/PM:")
        self.set_am = tk.Radiobutton(self.am_pm_frame, text="AM", variable=self.am_pm,
                                     value=0)
        self.set_pm = tk.Radiobutton(self.am_pm_frame, text="PM", variable=self.am_pm,
                                     value=1)
        self.active_button = tk.Checkbutton(self.edit_frame, text="Set Active:", variable=self.new_active)
        self.save_button = tk.Button(self.edit_window, text="Save", command=self.confirm_edit)
        self.cancel_button = tk.Button(self.edit_window, text="Cancel", command=self.edit_window.destroy)
        
        self.spinbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_select.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_select.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.set_am.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.set_pm.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.am_pm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.edit_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.save_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def confirm_edit(self):
        self.confirm = messagebox.askyesno(message="Are you sure you want to complete this action?", icon="question", title="Confirm Action",
                            default="yes")
        if self.confirm == "yes":
            am_pm = "AM" if self.am_pm.get() == 0 else "PM" 
            time = str(self.new_hr.get()) + ":" + str(self.new_min.get()) + " " + am_pm
            active = self.new_active.get()
            if bool(active) is True:
                active = "True"
            elif bool(active) is False:
                active = "False"
            else:
                print("There was an error with the active variable:", active)
                return
            if __name__ != "__main__":
                self.db.edit(self.time, time, active)
            self.time = time
            self.active = active
        else:
            self.edit_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x145")
    root.minsize(400, 145)
    root.title("Alarm")

    alarm = Alarm(root, 1, "12:00 PM", "MonTueWedThuFriSatSun", None, "", True)
    alarm.pack(fill=tk.BOTH, expand=1)
    
    root.mainloop()