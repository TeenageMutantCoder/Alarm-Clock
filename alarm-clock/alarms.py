import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
from time import sleep, strftime
from threading import Thread
try:
    from alarm import Alarm
    from sql_connector import SqlConnector
except ImportError:
    from .alarm import Alarm
    from .sql_connector import SqlConnector


class Alarms(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.parent = self
        self.alarms_canvas = tk.Canvas(self.canvas_frame)
        self.alarms_canvas.parent = self.canvas_frame
        self.alarms = tk.Frame(self.alarms_canvas)
        self.alarms.parent = self.alarms_canvas
        self.add_alarm_button = tk.Button(self, text="Add Alarm", command=self.add_alarm)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL,
                                      command=self.alarms_canvas.yview)

        self.add_alarm_button.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.alarms_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        
        # Creating long list of alarm frames. Values populated from database
        self.db = SqlConnector()
        self.alarm_frames = []
        self.add_alarms()
        self.thread = Thread(target=self.check_time, daemon=True)
        self.thread.start()
        self.alarms_canvas.bind("<Configure>", self.on_canvas_resize)
    
    def check_time(self):
        while True:
            if int(strftime("%S")) in [0, 1, 2]:
                time = strftime("%I:%M %p")
                for alarm in self.alarms_data:
                    if alarm[1] == time and alarm[2] == "True":
                        for alarm_obj in self.alarm_frames:
                            if alarm[0] == alarm_obj.id:
                                if alarm_obj.alarm_sound is None:
                                    alarm_obj.play_sound()
                                break
                        
            sleep(1)

    def add_alarms(self):
        self.alarms_data = self.db.collect()
        for alarm_frame in self.alarm_frames:
            alarm_frame.pack_forget()
        self.alarm_frames = []
        for row in range(len(self.alarms_data)):
            self.alarm_frames.append(Alarm(self.alarms, self.alarms_data[row][0],
                                               self.alarms_data[row][1], "SunMonTueWedThuFriSat",
                                               None, "", self.alarms_data[row][2]))
        for alarm_frame in self.alarm_frames:
            alarm_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

        self.alarms_canvas.create_window(0, 0, anchor='nw', window=self.alarms,
                                         tags="alarms")
        self.alarms_canvas.update_idletasks()
        self.alarms_canvas.configure(scrollregion=self.alarms_canvas.bbox('all'),
                                     yscrollcommand=self.scrollbar.set)
        self.on_canvas_resize()

    
    def remove_alpha(self, var, index, mode):
        if str(var) == "PY_VAR0":  # new_hr StringVar is edited
            current = self.new_hr.get()
            self.new_hr.set("".join(x for x in current if x.isdigit()))
            current = str(self.new_hr.get())
            if str(current) == "":
                self.new_hr.set(1)
            elif int(current) > 12:
                self.new_hr.set(12)
        if str(var) == "PY_VAR1":  # new_min StringVar is edited
            current = self.new_min.get()
            self.new_min.set("".join(x for x in current if x.isdigit()))
            current = str(self.new_min.get())
            if str(current) == "":
                self.new_min.set(0)
            elif int(current) > 59:
                self.new_min.set(59)

    def add_alarm(self):
        self.add_window = tk.Toplevel(self)
        self.new_hr = tk.StringVar()
        self.new_min = tk.StringVar()
        self.am_pm = tk.StringVar()
        self.new_active = tk.StringVar()
        self.new_hr.trace_add("write", self.remove_alpha)
        self.new_min.trace_add("write", self.remove_alpha)
        self.am_pm.set(0)
        self.new_active.set(1)

        self.add_frame = tk.Frame(self.add_window)
        self.spinbox_frame = tk.Frame(self.add_frame)
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
        self.active_button = tk.Checkbutton(self.add_frame, text="Set Active:", variable=self.new_active)
        self.save_button = tk.Button(self.add_window, text="Save", command=self.confirm_add_alarm)
        self.cancel_button = tk.Button(self.add_window, text="Cancel", command=self.add_window.destroy)
        
        self.spinbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_select.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_select.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.set_am.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.set_pm.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.hours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.minutes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.am_pm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.active_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.add_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.save_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def confirm_add_alarm(self):
        self.confirm = messagebox.askyesno(message="Are you sure you want to complete this action?", icon="question", title="Confirm Action",
                            default="yes")
        if self.confirm is True:
            am_pm = int(self.am_pm.get())
            if am_pm == 0:
                am_pm = "AM"
            elif am_pm == 1:
                am_pm = "PM"
            else:
                print("There was an error with the am_pm value:", am_pm)
                raise ValueError
            new_hr = str(self.new_hr.get())
            new_min = str(self.new_min.get())
            if len(new_hr) == 1:
                new_hr = "0" + new_hr
            if len(new_min) == 1:
                new_min = "0" + new_min
            time = new_hr + ":" + new_min + " " + am_pm
            active = int(self.new_active.get())
            if active == 0:
                active = "False"
            elif active == 1:
                active = "True"
            else:
                print("There was an error with the active value:", active)
                raise ValueError
            self.db.insert(time, active)
            self.alarms_canvas.delete("all")
            self.add_alarms()
            self.add_window.destroy()
        elif self.confirm is False:
            self.add_window.destroy()
        else:
            print("There was an error with the self.confirm value:", self.confirm)
            self.confirm_add_alarm()

    def on_canvas_resize(self, *args):
        self.alarms.width = self.alarms_canvas.winfo_width()
        self.alarms_canvas.itemconfig('alarms',
                                      width=self.alarms_canvas.winfo_width())
        self.alarms_canvas.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x185")
    root.minsize(420, 170)
    root.title("Alarms")

    alarms = Alarms(root)
    alarms.pack(fill=tk.BOTH, expand=1)
    def on_close():
        alarms.db.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()