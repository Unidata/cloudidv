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

class KeySimpleDialog(sdg.Dialog):

    def body(self, master):

        minst = ['1. Sign in to Dropbox via web browser.','2. Copy dropbox key with highlight, right-click, copy','3. Minimize browser window.','4. Click the "Grab Key from clipboard button".', '5. Press "ok"']

        self.result = "default result"
        self.keytxt = StringVar()
        self.insttxt = StringVar()

        self.instlbl = Label(master, textvariable = self.insttxt, justify=LEFT).grid(row=0)
        self.insttxt.set("\n".join(minst))

        self.keylbl = Label(master, textvariable = self.keytxt).grid(row=1)
        self.keyentry = Entry(master,textvariable=self.keytxt)
        self.keytxt.set("[Key will go here]")
        self.grabbtn = Button(master, text="Grab Key from clipboard", command = self.grabKey).grid(row=2)

    def grabKey(self):
        print("Key: " + self.clipboard_get())
        self.keytxt.set(self.clipboard_get())
        self.result = self.clipboard_get()


    def apply(self):
        print("Apply caught.")
        print("Result: " + self.result)

    def validate(self):
        return 1

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        parent.minsize(width=250,height=100)
        self.parent = parent
        # Create GUI here
        self.btn_auth = Button(self, text="Authenticate", command = self.configDB)
        self.btn_import = Button(self, text="Import", command = self.importFiles)
        self.btn_export = Button(self, text="Export", command = self.exportFiles)
        self.btn_reset = Button(self, text="Reset IDV Preferences", command = self.resetPrefs)
        self.btn_idv = Button(self, text="Launch IDV", command = self.runIDV)
        self.btn_quit = Button(self,text="Quit", command=quit)

        self.btn_auth.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_import.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_export.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_reset.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_idv.pack(side="top",fill="both",padx=10,expand=True)
        self.btn_quit.pack(side="bottom",fill="both",padx=10,expand=True)

        parent.bind('<Control-c>', self.quit_proc)

    def resetPrefs(self):
        folder = os.path.expanduser("~/.unidata/idv")
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        messagebox.showinfo("Reset","IDV Preferences reset to default")


    def runIDV(self):
        idv = subprocess.call(os.path.expanduser("~/IDV/runIDV"),shell=True)

    def configDB(self):
        child = pexpect.spawnu('rclone config')
        child.logfile = sys.stdout

        child.expect(['n/s/q> ', 'e/n/d/s/q> '])
        child.sendline('n')

        child.expect('name> ')
        child.sendline('dropbox')

        child.expect('Storage> ')
        child.sendline('dropbox')

        child.expect('app_key> ')
        child.sendline('')

        child.expect('app_secret> ')
        child.sendline('')

        ## Optional, only if there exists a config file already.
        try:
            child.expect('y/n> ',timeout=1)
            child.sendline('y')
        except pexpect.TIMEOUT:
            pass

        child.expect('https://.*response_type=code')

        mbrowser = subprocess.Popen(["/usr/bin/firefox", "--private-window", child.after], preexec_fn=os.setsid)

        d = KeySimpleDialog(root)
        mykey = d.result
        print("mykey: " + mykey)
        child.expect('Enter the code: ')

        ## Kill the browser.
        os.killpg(os.getpgid(mbrowser.pid), signal.SIGTERM)

        child.sendline(mykey)

        child.expect('y/e/d> ')
        child.sendline('y')

        child.expect('e/n/d/s/q> ')
        child.sendline('q')

        child.close()
        messagebox.showinfo("Authentication","Authentication Successful.")


    def quit_proc(self):
        print("Quit event caught")
        quit()

    def importFiles(self):
        if not os.path.exists(os.path.expanduser('~/.unidata')):
            print("Creating target directory ~/.unidata")
            os.makedirs(os.path.expanduser('~/.unidata'))

        mimport = subprocess.call("/usr/bin/rclone --stats 0m5s --exclude jython2.7/** copy dropbox:unidata_sync/idv ~/.unidata",shell=True)
        messagebox.showinfo("Import","Files imported from dropbox:unidata_sync/IDV")

    def exportFiles(self):
        if os.path.exists(os.path.expanduser("~/.unidata")):
            mexport = subprocess.call("/usr/bin/rclone --stats 0m5s --exclude jython2.7/** copy ~/.unidata dropbox:unidata_sync/idv",shell=True)
            messagebox.showinfo("Export","Files exported to dropbox:unidata_sync/IDV")
        else:
            messagebox.showinfo("Export","No files found in ~/.unidata to export.")

if __name__ == "__main__":
        root = tk.Tk()
        MainApplication(root).pack(side="top", fill="both", expand=True)

        root.mainloop()
