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
        self.infoText = "The amount of memory available is modified using\n the IDVMEM parameter when launching\n the Docker container."
        self.labelText = "IDV Memory available: %sm" % (os.getenv('IDVMEM', "512"))

        self.lbl_info = Label(self, text=self.infoText)
        self.lbl_mem = Label(self, text=self.labelText)
        self.btn_idv = Button(self, text="Launch IDV", command = self.runIDV)
        #self.btn_watch = Button(self, text="Launch Watch Widget", command=self.runWatch)

        self.lbl_info.pack(side="top",fill="both",padx=10,expand=True)
        self.lbl_mem.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_idv.pack(side="top",fill="both",padx=10,expand=True)
        #self.btn_watch.pack(side="top",fill="both",padx=10,expand=True)
        self.runIDV()

    def runIDV(self):
        idv = subprocess.call(os.path.expanduser("~/IDV/jre/bin/java -Xmx%sm -XX:+DisableExplicitGC -Didv.enableStereo=false -jar ~/IDV/idv.jar" % (os.getenv('IDVMEM', "512"))), shell=True)

    def runWatch(self):
        mwatch = subprocess.call(os.path.expanduser("/usr/bin/swisswatch &"),shell=True)

if __name__ == "__main__":
        root = tk.Tk()
        MainApplication(root).pack(side="top", fill="both", expand=True)

        root.mainloop()
