from tkinter.filedialog import askopenfile
import time
from tkinter.ttk import *
from tkinter import *
import webbrowser
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil
import subprocess


target = './TestData/TestWhole'


class MyApp:

    def __init__(self):
        self.window = Tk()
        self.window.title("DFDNet")
        self.window.geometry("750x500")
        self.window.minsize(750, 500)
        self.window.iconbitmap("logo.ico")
        self.window.config(background='#1A2723')
        self.pixelVirtual = PhotoImage(width=1, height=1)
        self.buttonImageInput = PhotoImage(file='./assets/button.png')
        self.buttonImageStart = PhotoImage(file='./assets/start.png')
        self.buttonSave = PhotoImage(file='./assets/save.png')
        self.bgButton = PhotoImage(file='./assets/bg_button.png')
        self.bgResult = PhotoImage(file='./assets/bg_result.png')
        self.Result = PhotoImage(file='./assets/test9.png')
        self.old = PhotoImage(file='./assets/test9.png')
        self.file_path = None
        self.save_path = None
        self.save_target = None
        # initialization des composants
        self.frameTitre = Frame(self.window, bg='#1A2723', )
        self.frameBouton = Frame(
            self.window, bg='#273934')
        self.frameResult = Frame(
            self.window, bg='#273934', bd=1, relief=SUNKEN)

        # Canvas
        self.ButtonCanva = Canvas(
            self.window, width=740, highlightthickness=0, bg="#1A2723", height=79)

        self.ButtonCanva.create_image(0, 0, image=self.bgButton, anchor="nw")

        self.ResultCanva = Canvas(
            self.window, width=740, highlightthickness=0, bg="#1A2723", height=293)

        self.ResultCanva.create_image(0, 0, image=self.bgResult, anchor="nw")

        self.loadCanva = Canvas(
            self.window, width=740, highlightthickness=0, bg="#1A2723", height=20)

        # creation des composants
        self.create_widgets()

        # empaquetage
        self.frameTitre.pack()
        self.ButtonCanva.pack()
        self.frameBouton.pack()

        self.ResultCanva.pack()

    def create_widgets(self):
        self.create_title()
        self.create_button()

    def create_title(self):
        label_title = Label(self.frameTitre, text="DFDNet", font=("Poppins Bold", 40), bg='#1A2723',
                            fg='white')
        label_title.pack()

    def create_button(self):

        in_button = Button(self.window, font=(
            "Poppins SemiBold", 22),  fg='#273934', bg="#273934", bd=0, image=self.buttonImageInput,  command=lambda: self.open_file())
        in_button.pack(side=LEFT, padx=20)

        in_button_canvas = self.ButtonCanva.create_window(
            10, 20, anchor="nw", window=in_button)

        st_button = Button(self.window, font=(
            "Poppins SemiBold", 22),  fg='#273934', bg="#273934", bd=0, image=self.buttonImageStart,  command=lambda: self.uploadFiles())
        st_button.pack(side=RIGHT, padx=20)

        st_button_canvas = self.ButtonCanva.create_window(
            650, 20, anchor="nw", window=st_button)

    def open_file(self):
        self.file_path = askopenfile(
            mode='r', filetypes=[('Image Files', '*png')])
        print("this is file path : ", os.path.basename(self.file_path.name))
        if self.file_path is not None:
            shutil.copy(self.file_path.name, target)

            st_button_canvas = self.ButtonCanva.create_text(
                230, 30, anchor="nw", text=os.path.basename(self.file_path.name), font=("Poppins Bold", 12), fill='#8AD6BF')

    def save_file(self):
        self.save_path = filedialog.askdirectory()
        print("this is save path : ", self.save_path)
        print("this is Image path : ", self.save_target)
        if (self.save_path is not None and self.save_target is not None):
            shutil.copy(self.save_target, self.save_path)

    def uploadFiles(self):
        if self.file_path is not None:
            p = subprocess.Popen(['python', 'test_FaceDict.py'])
        s = Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar",
                    foreground='#8AD6BF', background='#273934', bd=0)
        pb1 = Progressbar(
            self.frameBouton,
            orient=HORIZONTAL,
            length=738,
            mode='indeterminate', style="red.Horizontal.TProgressbar"
        )
        pb1.grid(row=4, columnspan=3)
        while p.poll() is None:
            self.frameBouton.update_idletasks()
            pb1['value'] += 1
            time.sleep(0.01)
        pb1.destroy()
        fichier = './Results/TestWholeResults/Step4_FinalResults/' + \
            os.path.basename(self.file_path.name)
        print(fichier)
        img = Image.open(self.file_path.name)
        img = img.resize((250, 250), Image.ANTIALIAS)
        self.old = ImageTk.PhotoImage(image=img)
        label_image_old = Label(self.window, image=self.old,
                                height=250, width=250)

        label_canva = self.ResultCanva.create_window(
            44, 20, anchor="nw", window=label_image_old)
        img2 = Image.open(fichier)
        img2 = img2.resize((250, 250), Image.ANTIALIAS)
        self.Result = ImageTk.PhotoImage(image=img2)
        label_image = Label(self.window, image=self.Result,
                            height=250, width=250)

        label_canva = self.ResultCanva.create_window(
            444, 20, anchor="nw", window=label_image)
        self.save_target = fichier
        save_button = Button(self.window, font=(
            "Poppins SemiBold", 22),  fg='#273934', bg="#273934", bd=0, image=self.buttonSave,  command=lambda: self.save_file())
        save_button.pack(side=LEFT, padx=20)

        in_button_canvas = self.ResultCanva.create_window(
            310, 230, anchor="nw", window=save_button)


# afficher
app = MyApp()
app.window.resizable(False, False)
app.window.mainloop()
