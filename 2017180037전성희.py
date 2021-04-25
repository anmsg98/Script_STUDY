import re
import logging
from logging import info as print
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

logging.basicConfig(level=logging.DEBUG)

python_text = '''Python is an interpreted high-level general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation. Its language constructs as well as its object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.[30]
Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly, procedural), object-oriented and functional programming. Python is often described as a "batteries included" language due to its comprehensive standard library.[31]
Guido van Rossum began working on Python in the late 1980s, as a successor to the ABC programming language, and first released it in 1991 as Python 0.9.0.[32] Python 2.0 was released in 2000 and introduced new features, such as list comprehensions and a garbage collection system using reference counting and was discontinued with version 2.7.18 in 2020.[33] Python 3.0 was released in 2008 and was a major revision of the language that is not completely backward-compatible and much Python 2 code does not run unmodified on Python 3.
Python consistently ranks as one of the most popular programming languages.[34][35][36][37][38]
'''

def stop(event=None):
    window.quit()

window = Tk()
window.title('Tkinter App')
window.geometry('+100+100')
window.resizable(False, False)

label = Label(text='Regular Expression Program'.center(50, ' '))
label.pack()

# LabelFrame
frame_find = LabelFrame(window, text="Find Words", relief="solid")
frame_find.pack(side=TOP)

frame_change = LabelFrame(window, text="Change Words", relief="solid")
frame_change.pack()

frame_mode = LabelFrame(window, text="Mode", relief="solid")
frame_mode.pack()

frame_color = LabelFrame(window, text="Color", relief="solid")
frame_color.pack()

# checkbox
ignore_case = IntVar(value=0)
case_checkbutton = Checkbutton(frame_mode, text="Ignore Case", variable=ignore_case)
case_checkbutton.pack()

# radiobutton
found_color = StringVar(value='yellow')
Radiobutton(frame_color, text='Green', value='green', variable=found_color).pack()
Radiobutton(frame_color, text='Yellow', value='yellow', variable=found_color).pack()

# combobox
pattern_var = StringVar(value='Python')
combobox = Combobox(frame_find, textvariable=pattern_var, width=100, height=5, values=['python', '\d\d\d\d'])
combobox.pack(side=LEFT)

# entry
entry = Entry(frame_change, width=100)
entry.pack(side=LEFT,fill=X)

def find(event=None):
    input_text = text.get('1.0', END)
    lines = input_text.splitlines()
    pattern = pattern_var.get()
    if ignore_case.get() == 1:
        target_re = re.compile(pattern, re.IGNORECASE)
    else:
        target_re = re.compile(pattern)

    #history_listbox.insert(0, pattern)
    print(combobox['values'])
    combobox['values'] = tuple(set(combobox['values']) | {pattern})

    text.tag_configure("found", background=found_color.get(), foreground='red')
    text.tag_remove("found", 1.0, END)
    for i, line in enumerate(lines):
        for mo in target_re.finditer(line):
            text.tag_add('found', f'{i+1}.{mo.span()[0]}', f'{i+1}.{mo.span()[1]}')
            #print(mo)

def change(event=None):
    input_text = text.get('1.0', END)
    lines = input_text.splitlines()

    pattern = pattern_var.get()
    if ignore_case.get() == 1:
        target_re = re.compile(pattern, re.IGNORECASE)
    else:
        target_re = re.compile(pattern)

    pattern2 = entry.get()

    input_text = re.sub(target_re, pattern2, input_text)

    text.delete('1.0', END)
    text.insert(END, input_text)


button_find = Button(frame_find, text='Find', command=find, takefocus=False)
button_find.pack(side=RIGHT)

button_change = Button(frame_change, text='Change', command=change, takefocus=False)
button_change.pack(side=RIGHT)

text = ScrolledText(width = 50, height=20, font=("Malgun Gothic", 14))
text.insert(END, python_text)
text.pack(side=BOTTOM, fill=X)

menu_root = Menu()

def open_file():
    file_name = filedialog.askopenfilename(
        title='Select a text file',
        filetype=(('txt file (.txt)', '*.txt'),)
    )
    f = open(file_name)
    text.delete('1.0', END)
    text.insert(END, f.read())
    f.close()

def save_file_as():
    file_name = filedialog.asksaveasfile(
        mode='w',
        title='save file as ...',
        filetype=(('.txt file', '*.txt'),),
        defaultextension='txt'
    )
    file_name.write(text.get('1.0', END))
    file_name.close()


menu_file = Menu(menu_root, tearoff=0)
menu_file.add_command(label='Open', accelerator='Ctrl+O', command=open_file)
menu_file.add_command(label='Save as...', command=save_file_as)
menu_file.add_separator()
menu_file.add_command(label='quit', command=stop)
menu_root.add_cascade(label='File', menu=menu_file)

menu_search = Menu(menu_root)
menu_search.add_command(label='Search my text')
menu_root.add_cascade(label='Search', menu=menu_search)

window.config(menu=menu_root)

window.bind("<Escape>", stop)
window.mainloop()
