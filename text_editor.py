from tkinter import *
import tkinter.filedialog as tk
import tkinter.messagebox as tk2
import os
from datetime import date

text_size = 16  # default text size
text_style = "Helvetica"  # default text style


class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)  # Tk is the superclass here
        root.title("Untitled - Notepad")
        self.create_widgets()
        root.bind('<Control-z>', self.undo)  # shortcut to perform undo operation

    def create_widgets(self):
        # stausbar
        today = date.today()
        statusvar = StringVar()
        statusvar.set("Date: " + str(today))
        sbar = Label(root, textvariable=statusvar, bd=1, relief=SUNKEN, anchor="w")
        sbar.pack(side=BOTTOM, fill=X)

        # scrollbar
        scrollbar = Scrollbar(root)  # to add a scrollbar
        scrollbar.pack(side=RIGHT, fill=Y)

        # main text area
        # self.text1 = Text(width=20, height=20, yscrollcommand=scrollbar.set, font="helvetica 13")  # text color can be added by doing fg="red"
        self.text1 = Text(width=20, height=20, yscrollcommand=scrollbar.set)
        self.text1.configure(font=(text_style, text_size))
        self.text1.pack(expand=YES, fill=BOTH)  # to make the textbox fill entire window
        scrollbar.config(command=self.text1.yview)

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        editmenu = Menu(menubar, tearoff=0)
        toolsmenu = Menu(menubar, tearoff=0)
        helpmenu = Menu(menubar, tearoff=0)

        # File menu
        filemenu.add_command(label='New', command=self.newDoc)
        filemenu.add_command(label='Save', command=self.saveDoc)
        filemenu.add_command(label='Open', command=self.openDoc)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quitApp)
        menubar.add_cascade(label='File', menu=filemenu)

        # Edit menu
        editmenu.add_command(label='Cut', command=self.cut)
        editmenu.add_command(label='Copy', command=self.copy)
        editmenu.add_command(label='Paste', command=self.paste)
        editmenu.add_command(label='Clear', command=self.clear)
        menubar.add_cascade(label='Edit', menu=editmenu)

        # Tools menu
        toolsmenu.add_command(label='Undo', command=self.undo)
        toolsmenu.add_command(label='Word Count', command=self.wordCount)
        toolsmenu.add_command(label='Find & Replace', command=self.find_replace_button)
        toolsmenu.add_separator()
        toolsmenu.add_command(label='Font Style', command=self.font_style)
        toolsmenu.add_command(label='Font Size', command=self.font_size)
        toolsmenu.add_command(label='Font Color', command=self.font_color)
        toolsmenu.add_command(label='Background Color', command=self.background_color)
        menubar.add_cascade(label='Tools', menu=toolsmenu)

        # Help menu
        helpmenu.add_command(label='About', command=self.about)
        menubar.add_cascade(label='Help', menu=helpmenu)

        root.config(menu=menubar)

    def newDoc(self):
        if tk2.askyesno("Message", "All unsaved work will be lost. Continue?"):
            root.title("Untitled - Notepad")
            self.text1.delete("1.0", END)  # 1.0 means 1st row & 0th character

    def saveDoc(self):
        savefile = tk.asksaveasfile(mode='w', defaultextension=".txt")
        text2save = str(self.text1.get("1.0", END))
        savefile.write(text2save)
        savefile.close()

    def openDoc(self):
        openfile = tk.askopenfile(mode='r')
        text = openfile.read()
        self.text1.insert(END, text)
        openfile.close()

    def quitApp(self):
        root.destroy()

    def cut(self):
        self.text1.event_generate("<<Cut>>")

    def copy(self):
        # Copy the selected text into the clipboard
        # var = str(self.text1.get(SEL_FIRST, SEL_LAST))
        # self.clipboard_clear()
        # self.clipboard_append(var)
        self.text1.event_generate("<<Copy>>")

    def paste(self):
        # Insert the clipboard text into the textbox
        # result = self.selection_get(selection="CLIPBOARD")  # get text from clipboard
        # self.text1.insert("1.0", result)
        self.text1.event_generate("<<Paste>>")

    def clear(self):
        self.text1.delete("1.0", END)

    def wordCount(self):
        # Get text from textbox and split it by whitespace characters into a list. Then find length of list
        usertext = self.text1.get("1.0", END)
        wordlist = usertext.split()
        number_of_words = len(wordlist)
        tk2.showinfo('Word Count', 'Words:  ' + str(number_of_words))

    def undo(self, event):
        usertext = self.text1.get(0.0, END)
        wordlist = usertext.split()
        self.text1.delete(0.0, END)
        if wordlist == []:
            return
        wordlist.pop()  # remove the latest element written to the screen
        self.text1.insert(0.0, wordlist)

    def find_replace_button(self):
        global find_box, replace_box, label1, label2, button2, button3
        label1 = Label(text="Find")
        label1.pack(side=LEFT)
        find_box = Text(root, height=1, width=20)
        find_box.pack(side=LEFT)
        label2 = Label(text="	Replace")
        label2.pack(side=LEFT)
        replace_box = Text(root, height=1, width=20)
        replace_box.pack(side=LEFT)
        button2 = Button(root, text="Replace", command=self.find_replace)
        button2.pack(side=LEFT, padx=10)
        button3 = Button(root, text="x", command=self.destroy_find_replace)
        button3.pack(side=RIGHT)

    def destroy_find_replace(self):
        label1.destroy()
        label2.destroy()
        button2.destroy()
        button3.destroy()
        replace_box.destroy()
        find_box.destroy()

    def find_replace(self):
        keyword = str(find_box.get(0.0, END))
        keyword = keyword.rstrip("\n")  # remove the newline character at the end of keyword
        replace_word = str(replace_box.get(0.0, END))
        replace_word = replace_word.rstrip("\n")  # remove the newline character at the end of replace_word
        usertext = self.text1.get(0.0, END)
        wordlist = usertext.split()

        for i in range(len(wordlist)):
            if wordlist[i][-1:] == "." and wordlist[i].rstrip(".") == keyword:
                wordlist[i] = replace_word+"."
            elif wordlist[i] == keyword:
                wordlist[i] = replace_word

        self.text1.delete(0.0, END)
        self.text1.insert(0.0, wordlist)

    def style_dropdown(self, *args):
        txt = self.text1.get(0.0, END)
        self.text1.delete(0.0, END)
        self.text1.configure(font=(var1.get(), text_size))
        self.text1.insert(0.0, txt)
        w1.destroy()

    def font_style(self):
        global var1, w1
        var1 = StringVar(root)
        var1.set(text_style)
        match_list = ["Ariel", "Courier", "Helvetica", "Symbol", "Times New Roman"]
        var1.trace('w', self.style_dropdown)
        w1 = OptionMenu(root, var1, *match_list)
        w1.pack()

    def size_dropdown(self, *args):
        txt = self.text1.get(0.0, END)
        self.text1.delete(0.0, END)
        self.text1.configure(font=(text_style, var2.get()))
        self.text1.insert(0.0, txt)
        w2.destroy()

    def font_size(self):
        global var2, w2
        var2 = StringVar(root)
        var2.set(text_size)
        match_list = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        var2.trace('w', self.size_dropdown)
        w2 = OptionMenu(root, var2, *match_list)
        w2.pack()

    def font_color_dropdown(self, *args):
        txt = self.text1.get(0.0, END)
        self.text1.delete(0.0, END)
        self.text1.configure(font=(text_style, text_size), fg=var3.get())
        self.text1.insert(0.0, txt)
        w3.destroy()

    def font_color(self):
        global var3, w3
        var3 = StringVar(root)
        var3.set("Color")
        match_list = ["Red", "Yellow", "Blue", "Black", "Green", "Orange", "Grey", "Purple"]
        var3.trace('w', self.font_color_dropdown)
        w3 = OptionMenu(root, var3, *match_list)
        w3.pack()

    def background_color_dropdown(self, *args):
        txt = self.text1.get(0.0, END)
        self.text1.delete(0.0, END)
        self.text1.configure(font=(text_style, text_size), bg=var4.get())
        self.text1.insert(0.0, txt)
        w4.destroy()

    def background_color(self):
        global var4, w4
        var4 = StringVar(root)
        var4.set("Color")
        match_list = ["Red", "Yellow", "Blue", "Black", "Green", "Orange", "Grey", "Purple"]
        var4.trace('w', self.background_color_dropdown)
        w4 = OptionMenu(root, var4, *match_list)
        w4.pack()

    def about(self):
        tk2.showinfo("Notepad", "Hello, my name is Mr. Editor.\nI am made by Anubhav Kandiyal")


root = Tk()
root.title('My Text Editor')
root.geometry('700x600')
root.wm_iconbitmap("notepad.ico")
app = Application(root)
app.mainloop()
