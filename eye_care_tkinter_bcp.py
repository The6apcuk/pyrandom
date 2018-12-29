#!/usr/bin/python3.6
import tkinter as tk

import signal

from PIL import Image
from PIL import ImageTk

from tkinter import ttk

import sys


print(sys.version)


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
REST_TIME = 20
POPUP_FREQ = 0.1
RUNNING = True


class StartPage(tk.Tk):

    def __init__(self):

        # Initialize tk.Tk
        super().__init__()

        # Main Title
        self.title("PyeCare")

        # Hide on kill command
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        signal.signal(30, lambda *x: self.deiconify())

        # Image

        # dirname = os.popen("dirname $(ls -l $(which care)|awk '{print $NF}')").read().rstrip()
        self.image = ImageTk.PhotoImage(Image.open("favicon.png"))
        self.iconphoto(self, self.image)

        # Checkboxes
        # Hard
        self.checkbox_hard = ttk.Checkbutton(self, text="Hard mode")
        self.checkbox_hard.grid(row=1, column=1, columnspan=1, sticky="E")

        # Everlasting
        self.checkbox_forever = ttk.Checkbutton(self, state="normal", text="Everlasting\n    mode")
        self.checkbox_forever.state(['selected'])
        self.checkbox_forever.grid(row=2, column=1, columnspan=1, sticky="E")

        # Drop-down list
        variable = tk.StringVar(self)
        time = (0.2, 20, 25, 30, 40, 50, 60)
        choices = (str(i) + " minuts" for i in time)

        # set default value
        variable.set("{} minutes".format(time[0]))
        self.set_time("{} minutes".format(time[0]))

        # Combobox itself
        self.combobox = tk.OptionMenu(self, variable, *choices, command=lambda update: self.set_time(update))
        self.combobox.grid(row=2, column=3, columnspan=1, sticky="WE")

        # Progress bar style
        style = ttk.Style(self)

        # add label in the layout
        style.layout('text.Horizontal.TProgressbar',
                     [('Horizontal.Progressbar.trough',
                       {'children': [('Horizontal.Progressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                      ('Horizontal.Progressbar.label', {'sticky': ''})])

        # set initial text
        style.configure('text.Horizontal.TProgressbar', text='Select time and press Launch', thickness=50)

        # Progressbar
        self.progress_bar = ttk.Progressbar(self, style='text.Horizontal.TProgressbar', length = 200, )
        self.progress_bar.grid(row=0, column=0, columnspan=4, sticky="WE")

        # Button for progress bar
        self.progress_button = tk.Button(self, text="Launch",
                                         command=lambda: self.start_progress(self.progress_bar, style))
        self.progress_button.grid(row=1, column=3, columnspan=1, stick="WE")

    # Set global work time
    @staticmethod
    def set_time(update):

        # Get row time
        tmp_time = update

        # Update global time
        global WORK_TIME
        WORK_TIME = float(tmp_time[:-len("minutes")]) * 60


    def start_progress(self, pbar, style):

        # Set the maximum value of the progress bar
        pbar["maximum"] = int(WORK_TIME)

        # If Launch button was pressed
        if self.progress_button["text"] == "Launch":

            # Make the application running
            global RUNNING
            RUNNING = True

            # Change the button's text to Stop
            self.progress_button.configure(text="Stop")

            # Disable combobox
            self.combobox.configure(state='disabled')

            # Increase the progress bar
            def wrapper(pbar, style):

                # Get minutes and seconds to be updated
                min_left, sec_left = divmod((WORK_TIME - pbar["value"]), 60)

                # If progress bar needs to be updated, and the application is still running
                if pbar["value"] < WORK_TIME and RUNNING is True:

                    # Update progress-bar's real value and value in style
                    pbar["value"] += 1
                    style.configure('text.Horizontal.TProgressbar',
                                        text='Rest in {:0>2g}:{:0>2g}'.format(min_left, sec_left))

                    self.after(1000, lambda: wrapper(pbar, style))

                # If application is closing normally (not by Stop button)
                elif RUNNING is True:

                    # Enable combobox
                    self.combobox.configure(state='normal')

                    # Update progress-bar's real value and value in style
                    pbar["value"] = 0
                    style.configure('text.Horizontal.TProgressbar',
                                        text='{:0>2g}:{:0>2g}'.format(min_left, sec_left))

                    # Start the popup
                    self.popupmsg()

                    # Change the button's text
                    self.progress_button.configure(text="Launch")

                    # Wait for window application to be killed
                    tk.Toplevel.wait_window(self.popup_window)

                    # Configure the default information on the progress bar
                    style.configure('text.Horizontal.TProgressbar', text='Select time and press Launch')

                    # If the checkbox Everlasting is on
                    if self.checkbox_forever.instate(['selected']):

                        # Start the progress bar again
                        self.start_progress(pbar, style)

                # If application is closing by Stop button
                elif RUNNING is not True:

                    # Enable combobox
                    self.combobox.configure(state='normal')

                    # Update progress-bar's real value and value in style
                    pbar["value"] = 0
                    style.configure('text.Horizontal.TProgressbar',
                                    text='Stopped')

                    # Change the button's text
                    self.progress_button.configure(text="Launch")

            return wrapper(pbar, style)

        # If Stop button was pressed
        elif self.progress_button["text"] == "Stop":

            # Stop the application from running
            RUNNING = False

    def popupmsg(self):

        # Make a popup window
        self.popup_window = tk.Toplevel()

        # Expand the top level frame to full screen
        self.popup_window.rowconfigure(0, weight=1)
        self.popup_window.columnconfigure(0, weight=1)

        # Make full screen
        self.popup_window.attributes("-fullscreen", True)

        # Popup image
        label = tk.Label(self.popup_window, image=self.image, bg="light blue")
        label.grid(sticky="WENS")

        # Hotkey to kill the app
        self.popup_window.bind("<Control-q>", lambda *x: self.popup_window.destroy())

        self.popup_window.bind("<Control-u>", lambda *x: self.deiconify())


        # Make the popup unkillable
        if self.checkbox_hard.instate(['selected']):

            # To not be able to kill the window
            self.popup_window.protocol("WM_DELETE_WINDOW", lambda: ...)

            # Make permanently on top
            self.popup_window.wm_attributes("-topmost", 1)

            # Start changing the transparency
            self.less_visible(REST_TIME, self.popup_window)

        # Make popup killable
        else:
            # Start changing the transparency
            self.less_visible(REST_TIME, self.popup_window)

    # Start changing the transparency
    @staticmethod
    def less_visible(secs, window):

        # Some stupid, illogical formula, but it works
        quantity_of_updates = secs / POPUP_FREQ

        # 100% of intransparency
        cur_state = 1

        # Start changing transparency
        def wrapper(cur_state):

            # Until the application is fully transparent
            if round(cur_state, 1) != 0.0:

                # Change transparency to current value
                window.wm_attributes("-alpha", cur_state)

                # Change transparency to current value
                window.after(int(POPUP_FREQ * 1000), lambda: wrapper(cur_state - 1 / quantity_of_updates))

            # When application is fully transparent, make it killable and kill it
            elif RUNNING is True:

                # Make the application killable
                window.protocol("WM_DELETE_WINDOW", window.destroy)

                # Make the application not on top
                window.wm_attributes("-topmost", 0)

                # Kill the application
                window.destroy()

        return wrapper(cur_state)


app = StartPage()

app.mainloop()


