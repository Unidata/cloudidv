#!/usr/bin/python3

import os
import tkinter as tk
import signal

import shutil
from tkinter import *

from tkinter import messagebox
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import simpledialog as sdg

import subprocess
import sys
import pexpect

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        parent.minsize(width=250,height=100)
        self.parent = parent
        # Create GUI here
        self.btn_idv = Button(self, text="Launch IDV", command = self.runIDV)

        self.btn_idv.pack(side="top",fill="both",padx=10,expand=True)

    def runIDV(self):
        idv = subprocess.call(os.path.expanduser("~/IDV/jre/bin/java -Xmx512m -XX:+DisableExplicitGC -Didv.enableStereo=false -jar ~/IDV/idv.jar"),shell=True)

if __name__ == "__main__":
        root = tk.Tk()
        MainApplication(root).pack(side="top", fill="both", expand=True)

        root.mainloop()
