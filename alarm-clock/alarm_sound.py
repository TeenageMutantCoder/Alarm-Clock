import tkinter as tk
from tkinter.font import Font
import pygame.mixer
import wave
from os.path import relpath
from threading import Thread


class AlarmSound():
    def __init__(self, parent, file="default", set_window=False):
        self.parent = parent
        self.file = file  # File path or "default" alarm Sound
        self.set_window = set_window
        self.thread = Thread(target=self.on_active, daemon=True)
        if file == "default":
            self.file = relpath("alarm-clock/assets/sounds/beep_beep.wav")
        wav = wave.open(self.file)
        frequency = wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        self.sound = pygame.mixer.Sound(self.file)
        self.thread.start()

    def on_active(self):
        if self.set_window is True:
            self.window = tk.Toplevel(self.parent)
            self.window.title("Beep Beep!")
            self.label = tk.Label(self.window, text="Beep Beep!",
                                  font=Font(family='Helvetica', size=36,
                                            weight='bold'))
            self.stop_button = tk.Button(self.window, text="Stop",
                                         command=self.stop_sound,
                                         font=Font(family='Helvetica',
                                                   size=20))
            self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=3)
            self.stop_button.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            self.sound.play(loops=-1)
        else:
            self.sound.play(loops=-1)

    def stop_sound(self):
        self.sound.stop()
        if self.set_window is True:
            self.window.destroy()
        self.parent.alarm_sound = None


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x100")
    root.minsize(400, 100)
    root.title("Alarm Sound Test")
    alarm_sound = AlarmSound(root, set_window=True)
    root.mainloop()