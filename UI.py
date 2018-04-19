# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tkinter import *
import Arabycia

def text_analysis(text, search):
	print(text)
	ara = Arabycia.Arabycia(text)
	raw_data, data = ara.print_result()
	TextArea2.insert('1.0', raw_data)
	TextArea3.insert('1.0', data)
	if search != '':
		sres = ara.search(search)
		TextArea5.insert('1.0', sres)



root = Tk()
root.geometry("800x600")
root.resizable(0,0)
root.title("Arabycia")

lbl = Label(root, text="ادخل النص")
lbl.grid(row=0, column=3, padx=30, pady=15)
TextArea = Text(relief=SUNKEN, height=5)
TextArea.grid(row=0, column=2, padx=15, pady=15, ipadx=5, ipady=5)

lbl = Label(root, text="بحث")
lbl.grid(row=1, column=3, padx=15, pady=15)
TextArea4 = Text(relief=SUNKEN, height=1)
TextArea4.grid(row=1, column=2, padx=15, pady=15, ipadx=5, ipady=5)

lbl = Label(root, text="نتائج البحث")
lbl.grid(row=2, column=3, padx=15, pady=15)
TextArea5 = Text(relief=SUNKEN, height=1, bg="#EAEAEA")
TextArea5.grid(row=2, column=2, padx=15, pady=15, ipadx=5, ipady=5)

lbl = Label(root, text="النص مشكل")
lbl.grid(row=3, column=3, padx=15, pady=15)
TextArea2 = Text(relief=SUNKEN, height=3, bg="#EAEAEA")
TextArea2.grid(row=3, column=2, padx=15, pady=15, ipadx=5, ipady=5)

lbl = Label(root, text="التحليل")
lbl.grid(row=4, column=3, padx=15, pady=15)
TextArea3 = Text(relief=SUNKEN, height=10, bg="#EAEAEA")
TextArea3.grid(row=4, column=2, padx=15, pady=15, ipadx=5, ipady=5)

btn = Button(root, text="تحليل النص", command=lambda: text_analysis(TextArea.get("1.0", "end-1c"), TextArea4.get("1.0", "end-1c")))
btn.grid(row=5, column=2, ipadx=20, ipady=5)
root.mainloop()
