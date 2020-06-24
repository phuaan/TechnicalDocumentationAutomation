from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Combobox
from ObjectiveCClassDiagramAutomator import ObjectiveC
import platform

basedir = ""

window = Tk()
window.title("Technical Documentation Template Generator - Michael Gunawan")
window.geometry('500x75')
window.resizable(width=False, height=False)
#window.configure(bg='#3E4149')
if platform.system() == "Darwin":   # if its a Mac
    lbl = Label(window, text="Code Directory")  # , bg="#3E4149", fg="White")
    lbl.grid(column=0, row=0)

    txt = Entry(window, width=10, state='readonly')
    #txt.grid_columnconfigure(0, weight=1)
    txt.grid(column=1, row=0, sticky="we")


    def selectDir():
        global basedir
        basedir = filedialog.askdirectory()
        txt.config(state='normal')
        txt.delete(0, "end")
        txt.insert(0, basedir)
        txt.config(state='readonly')


    btn = Button(text="Browse", command=selectDir)
    btn.grid(column=2, row=0, sticky="e")

    lbl2 = Label(window, text="Programming Language")  # , bg="#3E4149", fg="White")
    lbl2.grid(column=0, row=1)

    combo = Combobox(window)
    combo['values'] = "Objective-C"
    combo.current(0)  # set the selected item
    combo.config(state='readonly')
    combo.grid(column=1, row=1)


    def genDocum():
        if basedir != "":
            objc_class_diagram = ObjectiveC(basedir)
            objc_class_diagram.generate_documentation()


    btn2 = Button(text="Generate Documentation", command=genDocum)
    btn2.grid(column=0, row=2)


    def genClassDiagram():
        if basedir != "":
            objc_class_diagram = ObjectiveC(basedir)
            objc_class_diagram.generate_class_diagram()


    btn3 = Button(text="Generate Class Diagram", command=genClassDiagram)
    btn3.grid(column=1, row=2)


    def genClassDiagram():
        if basedir != "":
            objc_class_diagram = ObjectiveC(basedir)
            objc_class_diagram.generate_class_diagram_image()


    btn4 = Button(text="Fix Class Diagram", command=genClassDiagram)
    btn4.grid(column=2, row=2)



    window.mainloop()
#rootView.withdraw()
#basedir = filedialog.askdirectory()
# if basedir != "":
#     objc_class_diagram = ObjectiveC(basedir)
#     objc_class_diagram.generate_class_diagram()
#     objc_class_diagram.generate_documentation()
