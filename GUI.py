#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 04:59:32 2019

@author: qiyuwang
"""
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames

import matplotlib
matplotlib.use('agg')

import PIL
from PIL import Image, ImageDraw, ImageTk

import os
import subprocess

class Paint(object):

    DEFAULT_PEN_SIZE = 1.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title("Doodle to Masterpieces")
        
        self.text = Text(self.root, height = 1, width = 80)
        self.text.grid(row=0, column=2)
        self.text.insert(END, "Draw the doodle below and transfer it to Renoir's style")
        
        self.menubar = Menu(self.root)
        # create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save File", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
          
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        
        # add buttons
        self.example_button = Button(self.root, text='example', command=self.show_example)
        self.example_button.grid(row=0, column=4)
        
        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=1, column=0)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=2, column=0)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=3, column=0)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=4, column=0)
        
        self.clean_button = Button(self.root, text='clean', command=self.clean)
        self.clean_button.grid(row=5, column=0)
        
        self.style = StringVar(self.root)
        self.style.set("Van Gogh")
        self.select_menu = OptionMenu(self.root, self.style, "Van Gogh", "Renoir", "Monet")
        self.select_menu.grid(row=6, column=0)        
        
        self.transfer_button = Button(self.root, text='transfer', command=self.transfer)
        self.transfer_button.grid(row=7, column=0)                

        self.c = Canvas(self.root, bg='white', width=800, height=600)
        self.c.grid(row=2, column = 1, rowspan = 5, columnspan=5)
        
        #  --- PIL
        self.image1 = PIL.Image.new('RGB', (512, 384), 'white')
        self.draw = ImageDraw.Draw(self.image1)

        self.setup()
        self.root.config(menu=self.menubar)
       
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.image = None
        
    def show_example(self):
        example_win = Toplevel()
        example_win.title("Example")
        img = ImageTk.PhotoImage(Image.open('target_masks/example.png'))     
        panel = Label(example_win, image = img)
        panel.image = img
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), 
                           fill=paint_color, width=self.line_width)
        self.old_x = event.x
        self.old_y = event.y

    def transfer(self):
        filename = f'target_mask.png'   
        self.image1.save('Result/'+filename)
        
        os.system("git --version")
        os.system("python3 test.py")
        
        VanGogh_command = "CUDA_VISIBLE_DEVICES=2,3 python apply.py --colors Models/VanGogh.hdf5_colors.npy --target_mask Result/target_mask.png --model Models/VanGogh.t7"
        Renoir_command = "CUDA_VISIBLE_DEVICES=2,3 python apply.py --colors Models/Renoir.hdf5_colors.npy --target_mask Result/target_mask.png --model Models/Renoir.t7"
        Monet_command = "CUDA_VISIBLE_DEVICES=2,3 python apply.py --colors Models/Monet.hdf5_colors.npy --target_mask Result/target_mask.png --model Models/Monet.t7"
        if self.style == 'Van Gogh':
            return_code = subprocess.run(VanGogh_command, shell=True)
        if self.style == 'Renoir':
            return_code = subprocess.run(Renoir_command, shell=True)
        if self.style == 'Monet':
            return_code = subprocess.run(Monet_command, shell=True)
        
        im = Image.open('Result/result.png')
        self.c.image = ImageTk.PhotoImage(im)
        self.c.create_image(0, 0, image=self.c.image, anchor='nw')
        
        
    def reset(self, event):
        self.old_x, self.old_y = None, None
        
    def clean(self):
        self.c.delete("all")
    
    def file_open(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select PNG File", filetypes=[("PEG","*.png")])
        if not filename:
            return # user cancelled; stop this method
        
        im = Image.open(filename)
        self.c.image = ImageTk.PhotoImage(im)
        self.c.create_image(0, 0, image=self.c.image, anchor='nw')

        
    def save(self):
        filename = f'test_sem.png'   
        self.image1.save(filename)
            
    def donothing():
       print ('')

if __name__ == '__main__':
    Paint()
    
    
