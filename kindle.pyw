#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a ...
"""

from __future__ import unicode_literals
import codecs
import os
import re
import sys
import shutil
import tkinter as T


def get_path():
    """ get Kindle path """
    if sys.platform == 'win32':
        x = os.popen("wmic VOLUME WHERE Label='kindle' GET DriveLetter").read()
        try:
            drv = re.search('[D-Z]:', x).group()
        except AttributeError:
            return 'No Kindle Device Found!\n'
        else:
            path = drv + '\\documents\\'
            if os.path.isdir(path):
                return path
            else:
                return 'No Directory Found!\n'
    else:
        return 'Unsupported System!\n'


def del_path(path):
    """ clean Kindle path """
    result = ''
    try:
        total = os.listdir(path)
        files = [
            os.path.normcase(i) for i in total
            if os.path.isfile(os.path.join(path, i))
        ]
        dirs = [
            os.path.normcase(i) for i in total
            if os.path.isdir(os.path.join(path, i))
        ]
        removes = [
            i for i in dirs
            if i not in [re.sub(r'\.\w+$', '.sdr', j) for j in files]
        ]
        for i in removes:
            if i != 'dictionaries' and i != 'updates':
                shutil.rmtree(path + i)
                result += ('Deleting %s%s\n' % (path, i))
        result += ('%s directories deleted.\n\n' % count(removes))
        return result
    except WindowsError:
        return path


def count(obj):
    n = len(obj)
    if "dictionaries" in obj:
        n -= 1
    if "updates" in obj:
        n -= 1
    return n


def show_clip(path):
    """ Show clipper """
    try:
        f = codecs.open((os.path.join(path, 'My Clippings.txt')), 'r', 'utf-8')
        t = f.readlines()
        f.close()
    except IOError:
        return 'No Clipper File Found!'
    else:
        return format_text(t)


def format_text(text):
    """ Foramt text """
    string = ''
    for i in text:
        string += i
    return string


class Kindle(object):
    """ Docstring for Kindle Frame Class """

    def __init__(self):
        """ Init """
        self.root = T.Tk()
        self.root.title('Kindle')
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+10+10' % (w * .6, h * .8))  # 'wxh+x+y'
        # self.root.resizable(0, 0)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.menubar = T.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.menu1 = T.Menu(self.menubar, tearoff=False)
        self.menu1.add_command(label='Clean', command=self.cleanup)
        self.menu1.add_command(label='Clip', command=self.clipper)
        self.menu1.add_separator()
        self.menu1.add_command(label='Quit', command=self.quit)

        self.menu2 = T.Menu(self.menubar, tearoff=False)
        self.menu2.add_command(label='Help', command=self.help)
        self.menu2.add_command(label='About', command=self.about)

        self.menubar.add_cascade(label='Todo', menu=self.menu1)
        self.menubar.add_cascade(label='Help', menu=self.menu2)

        self.frm1 = T.Frame(self.root)
        self.frm1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.frm1.rowconfigure(0, weight=1)
        self.frm1.columnconfigure(0, weight=1)

        self.frm2 = T.Frame(self.root)
        self.frm2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.txt1 = T.Text(self.frm1, font='-size 14', state='disabled')
        self.txt1.grid(row=0, column=0, sticky='nsew')

        self.scr1 = T.Scrollbar(self.frm1)
        self.scr1.grid(row=0, column=1, sticky='ns')
        self.scr1.config(command=self.txt1.yview)
        self.txt1.config(yscrollcommand=self.scr1.set)

        self.btn1 = T.Button(self.frm2, width=15, text='Clean')
        self.btn1.grid(row=0, column=0, padx=20, pady=10)
        self.btn1.config(command=self.cleanup)

        self.btn2 = T.Button(self.frm2, width=15, text='Clipper')
        self.btn2.grid(row=0, column=1, padx=20, pady=10)
        self.btn2.config(command=self.clipper)

        self.btn3 = T.Button(self.frm2, width=15, text='Quit')
        self.btn3.grid(row=0, column=2, padx=20, pady=10)
        self.btn3.config(command=self.quit)

        self.root.mainloop()

    def cleanup(self):
        """ Clean """
        self.display(del_path(get_path()))

    def clipper(self):
        """ Clipper text """
        self.display(show_clip(get_path()))

    def quit(self):
        """ Quit """
        self.root.destroy()

    def help(self):
        """ Help """
        message = 'Help:\n\nblabla'
        self.display(message)

    def about(self):
        """ About """
        self.display('Version: 0.0.0.1')

    def display(self, msg):
        """ Show message """
        self.txt1.config(state='normal')
        self.txt1.delete(0.0, 'end')
        self.txt1.insert('end', msg)
        self.txt1.config(state='disabled')


if __name__ == "__main__":
    k = Kindle()
