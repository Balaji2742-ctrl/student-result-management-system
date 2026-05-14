
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys
import dashboard
import subprocess


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Login_window:
    def __init__(self, root):

        self.root = root
        self.root.title("Login Window")
        self.root.state('zoomed')
        self.root.config(bg="#021e2f")

        # ===== BACKGROUND =====
        self.left_bg = Label(self.root, bg="#08A3D2")
        self.left_bg.place(relx=0, rely=0, relwidth=0.45, relheight=1)

        self.right_bg = Label(self.root, bg="#031F3C")
        self.right_bg.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # ===== LOGIN FRAME =====
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(
            relx=0.26,
            rely=0.14,
            relwidth=0.50,
            relheight=0.68
        )

        # ===== LEFT IMAGE =====
        self.left_original = Image.open(
        resource_path("images/login.png"))
        

        self.left = ImageTk.PhotoImage(self.left_original)

        self.left_label = Label(
        self.root,
        image=self.left,
        bg="white"
        )

        self.left_label.place(
        relx=0.11,
        rely=0.15,
        relwidth=0.28,
        relheight=0.66
        )


        self.root.bind("<Configure>", self.resize_image)

        # ===== TITLE =====
        Label(
            self.login_frame,
            text="LOGIN HERE",
            font=("times new roman", 34, "bold"),
            bg="white",
            fg="#08A3D2"
        ).place(relx=0.42, rely=0.10)

        # ===== EMAIL =====
        Label(
            self.login_frame,
            text="EMAIL ADDRESS",
            font=("times new roman", 20, "bold"),
            bg="white",
            fg="gray"
        ).place(relx=0.42, rely=0.30)

        self.txt_email = Entry(
            self.login_frame,
            font=("times new roman", 16),
            bg="lightgray"
        )

        self.txt_email.place(
            relx=0.42,
            rely=0.37,
            relwidth=0.45,
            relheight=0.07
        )

        # ===== PASSWORD =====
        Label(
            self.login_frame,
            text="PASSWORD",
            font=("times new roman", 20, "bold"),
            bg="white",
            fg="gray"
        ).place(relx=0.42, rely=0.50)

        self.txt_pass_ = Entry(
            self.login_frame,
            font=("times new roman", 16),
            bg="lightgray",
            show="*"
        )

        self.txt_pass_.place(
            relx=0.42,
            rely=0.57,
            relwidth=0.45,
            relheight=0.07
        )

        # ===== SHOW / HIDE PASSWORD =====
        self.show_pass = False

        self.eye_btn = Button(
            self.login_frame,
            text="👁",
            font=("Arial", 12),
            bd=0,
            bg="lightgray",
            cursor="hand2",
            command=self.toggle_password
        )

        self.eye_btn.place(
            relx=0.84,
            rely=0.57,
            relwidth=0.05,
            relheight=0.07
        )

        # ===== REGISTER BUTTON =====
        Button(
            self.login_frame,
            cursor="hand2",
            text="Register new Account?",
            command=self.register_window,
            font=("times new roman", 14),
            bg="white",
            bd=0,
            fg="#B00857"
        ).place(relx=0.42, rely=0.68)

        # ===== FORGET BUTTON =====
        Button(
            self.login_frame,
            cursor="hand2",
            text="Forget Password",
            command=self.forget_password_window,
            font=("times new roman", 14),
            bg="white",
            bd=0,
            fg="red"
        ).place(relx=0.69, rely=0.68)

        # ===== LOGIN BUTTON =====
        Button(
            self.login_frame,
            text="Login",
            command=self.login,
            font=("times new roman", 22, "bold"),
            fg="white",
            bg="#B00857",
            cursor="hand2"
        ).place(
            relx=0.42,
            rely=0.80,
            relwidth=0.24,
            relheight=0.09
        )

    # ===== TOGGLE PASSWORD =====
    def toggle_password(self):

        if self.show_pass:
            self.txt_pass_.config(show="*")
            self.eye_btn.config(text="👁")
            self.show_pass = False

        else:
            self.txt_pass_.config(show="")
            self.eye_btn.config(text="🔒")
            self.show_pass = True

    # ===== IMAGE RESIZE =====
    def resize_image(self, event=None):

        w = self.left_label.winfo_width()
        h = self.left_label.winfo_height()

        if w > 1 and h > 1:
            img = self.left_original.resize((w, h), Image.LANCZOS)
            self.left_img = ImageTk.PhotoImage(img)
            self.left_label.config(image=self.left_img)

    # ===== RESET =====
    def reset(self):

        self.cmb_quest.current(0)

        self.txt_new_pass.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_pass_.delete(0, END)
        self.txt_email.delete(0, END)

    # ===== FORGET PASSWORD =====
    def forget_password(self):

        if self.cmb_quest.get() == "Select" or self.txt_answer.get() == "" or self.txt_new_pass.get() == "":
            messagebox.showerror(
                "Error",
                "All fields are required",
                parent=self.root2
            )

        else:
            try:
                con = sqlite3.connect(resource_path("rms.db"))
                cur = con.cursor()

                cur.execute(
                    "select * from employee where email=? and question=? and answer=?",
                    (
                        self.txt_email.get(),
                        self.cmb_quest.get(),
                        self.txt_answer.get()
                    )
                )

                row = cur.fetchone()

                if row == None:
                    messagebox.showerror(
                        "Error",
                        "Please Select Correct Question / Answer",
                        parent=self.root2
                    )

                else:
                    cur.execute(
                        "update employee set password=? where email=?",
                        (
                            self.txt_new_pass.get(),
                            self.txt_email.get()
                        )
                    )

                    con.commit()
                    con.close()

                    messagebox.showinfo(
                        "Success",
                        "Password Reset Successfully",
                        parent=self.root2
                    )

                    self.reset()
                    self.root2.destroy()

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root
                )

    # ===== FORGET PASSWORD WINDOW =====
    def forget_password_window(self):

        if self.txt_email.get() == "":
            messagebox.showerror(
                "Error",
                "Please Enter Email Address",
                parent=self.root
            )

        else:
            try:
                con = sqlite3.connect(resource_path("rms.db"))
                cur = con.cursor()

                cur.execute(
                    "select * from employee where email=?",
                    (self.txt_email.get(),)
                )

                row = cur.fetchone()

                if row == None:
                    messagebox.showerror(
                        "Error",
                        "Invalid Email Address",
                        parent=self.root
                    )

                else:
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("400x450+500+150")
                    self.root2.config(bg="white")
                    self.root2.resizable(False, False)
                    self.root2.focus_force()

                    Label(
                        self.root2,
                        text="Forget Password",
                        font=("times new roman", 22, "bold"),
                        bg="white",
                        fg="red"
                    ).pack(pady=20)

                    Label(
                        self.root2,
                        text="Security Question",
                        font=("times new roman", 15, "bold"),
                        bg="white",
                        fg="gray"
                    ).place(x=50, y=100)

                    self.cmb_quest = ttk.Combobox(
                        self.root2,
                        font=("times new roman", 13),
                        state="readonly",
                        justify="center"
                    )

                    self.cmb_quest['values'] = (
                        "Select",
                        "Your First Pet Name",
                        "Your Birth Place",
                        "Your Best Friend Name"
                    )

                    self.cmb_quest.place(x=50, y=130, width=300)
                    self.cmb_quest.current(0)

                    Label(
                        self.root2,
                        text="Answer",
                        font=("times new roman", 15, "bold"),
                        bg="white",
                        fg="gray"
                    ).place(x=50, y=190)

                    self.txt_answer = Entry(
                        self.root2,
                        font=("times new roman", 15),
                        bg="lightgray"
                    )

                    self.txt_answer.place(x=50, y=220, width=300)

                    Label(
                        self.root2,
                        text="New Password",
                        font=("times new roman", 15, "bold"),
                        bg="white",
                        fg="gray"
                    ).place(x=50, y=280)

                    self.txt_new_pass = Entry(
                        self.root2,
                        font=("times new roman", 15),
                        bg="lightgray"
                    )

                    self.txt_new_pass.place(x=50, y=310, width=300)

                    Button(
                        self.root2,
                        text="Reset Password",
                        command=self.forget_password,
                        bg="green",
                        fg="white",
                        font=("times new roman", 15, "bold")
                    ).place(x=110, y=370, width=180)

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root
                )

    # ===== REGISTER WINDOW =====
    def register_window(self):

        self.root.destroy()

        from register import Register

        root = Tk()
        obj = Register(root)
        root.mainloop()

    # ===== LOGIN =====
  
    def login(self):

        if self.txt_email.get() == "" or self.txt_pass_.get() == "":
            messagebox.showerror(
            "Error",
            "All fields are required",
            parent=self.root
        )

        else:
            try:
                con = sqlite3.connect(resource_path("rms.db"))
                cur = con.cursor()

                cur.execute(
                    "select * from employee where email=? and password=?",
                    (
                        self.txt_email.get(),
                        self.txt_pass_.get()
                    )
                )

                row = cur.fetchone()

                if row == None:
                    messagebox.showerror(
                        "Error",
                        "Invalid Email & Password",
                        parent=self.root
                    )

                else:
                    messagebox.showinfo(
                        "Success",
                        f"Welcome : {self.txt_email.get()}",
                        parent=self.root
                    )

                    self.txt_email.delete(0, END)
                    self.txt_pass_.delete(0, END)

                    self.root.destroy()

                    root = Tk()
                    app = dashboard.RMS(root)
                    root.mainloop()

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root
                )

            finally:
                try:
                    con.close()
                except NameError:
                    pass


if __name__ == "__main__":
    root = Tk()
    obj = Login_window(root)
    
    root.mainloop()

