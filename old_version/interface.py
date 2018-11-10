#!/usr/bin/python3

#import apodWallpaper

from tkinter import *

root = Tk()

'''

frameText = Label(root, text="Current New Wallpaper")
frameText.pack(side="top")
frame = Frame(root, width = 500, height = 300, bg="red")
frame.pack()
rollNewButton = Button(root, text="Roll New Wallpaper")
rollNewButton.pack(fill=X)


'''

label1 = Label(root, text="Name:")
label2 = Label(root, text="Password:")
entry1 = Entry(root)
entry2 = Entry(root)

label1.grid(row = 0)
label2.grid(row = 1)

entry1.grid(row = 0, column = 1)
entry2.grid(row = 1, column = 1)


root.mainloop()