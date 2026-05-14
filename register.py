
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys
import subprocess


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.state('zoomed')
        self.root.config(bg="white")

        # ===== BACKGROUND =====
        self.bg_img = Image.open(resource_path("images/b2.jpg"))
        self.bg_label = Label(self.root)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.root.bind("<Configure>", self.resize_bg)

        # ===== LEFT IMAGE =====
        self.left_img = Image.open(resource_path("images/side3.png"))
        self.left_label = Label(self.root, bg="white")
        self.left_label.place(relx=0.07, rely=0.12, relwidth=0.32, relheight=0.75)

        # ===== FORM FRAME =====
        self.frame1 = Frame(self.root, bg="white")
        self.frame1.place(relx=0.38, rely=0.12, relwidth=0.52, relheight=0.75)

        Label(
            self.frame1,
            text="REGISTER HERE",
            font=("times new roman", 25, "bold"),
            bg="white",
            fg="green"
        ).place(relx=0.05, rely=0.05)

        # ===== INPUT LABEL =====
        def lbl(txt, x, y):
            Label(
                self.frame1,
                text=txt,
                font=("times new roman", 15, "bold"),
                bg="white",
                fg="gray"
            ).place(relx=x, rely=y)

        # ===== ENTRY =====
        def entry(x, y):
            e = Entry(
                self.frame1,
                font=("times new roman", 15),
                bg="lightgray"
            )
            e.place(relx=x, rely=y, relwidth=0.35, relheight=0.06)
            return e

        lbl("First Name", 0.05, 0.18)
        self.txt_fname = entry(0.05, 0.24)

        lbl("Last Name", 0.55, 0.18)
        self.txt_lname = entry(0.55, 0.24)

        lbl("Contact No.", 0.05, 0.32)
        self.txt_contact = entry(0.05, 0.38)

        lbl("Email", 0.55, 0.32)
        self.txt_email = entry(0.55, 0.38)

        lbl("Security Question", 0.05, 0.46)
        self.cmb_quest = ttk.Combobox(self.frame1, state="readonly")
        self.cmb_quest['values'] = (
            "Select",
            "Your First Pet Name",
            "Your Birth Place",
            "Your Best Friend Name"
        )
        self.cmb_quest.place(relx=0.05, rely=0.52, relwidth=0.35, relheight=0.06)
        self.cmb_quest.current(0)

        lbl("Answer", 0.55, 0.46)
        self.txt_answer = entry(0.55, 0.52)

        lbl("Password", 0.05, 0.60)
        self.txt_password = entry(0.05, 0.66)

        lbl("Confirm Password", 0.55, 0.60)
        self.txt_cpassword = entry(0.55, 0.66)

        # ===== TERMS =====
        self.var_chk = IntVar()

        Checkbutton(
            self.frame1,
            text="I Agree Terms & Conditions",
            variable=self.var_chk,
            bg="white",
            font=("times new roman", 12)
        ).place(relx=0.05, rely=0.76)

        # ===== REGISTER BUTTON =====
        self.btn_img = ImageTk.PhotoImage(
            file=resource_path("images/register.png")
        )

        Button(
            self.frame1,
            image=self.btn_img,
            bd=0,
            cursor="hand2",
            command=self.register_data
        ).place(relx=0.05, rely=0.84)

        # ===== SIGN IN BUTTON =====
        Button(
            self.root,
            text="Sign In",
            command=self.login_window,
            bg="yellow",
            fg="black",
            font=("times new roman", 18, "bold"),
            bd=0,
            cursor="hand2"
        ).place(relx=0.28, rely=0.81, relwidth=0.10, relheight=0.055)

    # ===== BACKGROUND RESIZE =====
    def resize_bg(self, event=None):

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        if w > 1 and h > 1:

            bg = self.bg_img.resize((w, h), Image.LANCZOS)
            self.bg = ImageTk.PhotoImage(bg)
            self.bg_label.config(image=self.bg)

            lw = int(w * 0.32)
            lh = int(h * 0.75)

            left = self.left_img.resize((lw, lh), Image.LANCZOS)
            self.left = ImageTk.PhotoImage(left)
            self.left_label.config(image=self.left)

    # ===== LOGIN WINDOW =====
    def login_window(self):

        self.root.destroy()

        from login import Login_window

        root = Tk()
        obj = Login_window(root)
        root.mainloop()

    # ===== CLEAR =====
    def clear(self):

        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_quest.current(0)

    # ===== REGISTER DATA =====
    def register_data(self):

        if self.txt_fname.get() == "" or self.txt_contact.get() == "" or self.txt_email.get() == "":
            messagebox.showerror(
                "Error",
                "All fields required",
                parent=self.root
            )
            return

        if self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror(
                "Error",
                "Password mismatch",
                parent=self.root
            )
            return

        if self.var_chk.get() == 0:
            messagebox.showerror(
                "Error",
                "Please Accept terms & condition",
                parent=self.root
            )
            return

        try:
            con = sqlite3.connect(resource_path("rms.db"))
            cur = con.cursor()

            cur.execute(
                "select * from employee where email=?",
                (self.txt_email.get(),)
            )

            if cur.fetchone():
                messagebox.showerror(
                    "Error",
                    "User exists",
                    parent=self.root
                )

            else:
                cur.execute(
                    "insert into employee(f_name,l_name,contact,email,question,answer,password) values(?,?,?,?,?,?,?)",
                    (
                        self.txt_fname.get(),
                        self.txt_lname.get(),
                        self.txt_contact.get(),
                        self.txt_email.get(),
                        self.cmb_quest.get(),
                        self.txt_answer.get(),
                        self.txt_password.get()
                    )
                )

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Registered Successfully",
                    parent=self.root
                )

                self.clear()
                self.login_window()

            con.close()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=self.root
            )


root = Tk()
obj = Register(root)
root.mainloop()

