
from tkinter import *
from PIL import Image, ImageTk
from course import CourseClass
from student import studentClass
from result import resultclass
from report import reportclass
from tkinter import messagebox
import os
from time import strftime
import random
import sqlite3
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class RMS:
    def __init__(self, root):

        self.root = root
        self.root.title("Student Result Management System")

        # ===== FULL SCREEN =====
        self.root.state('zoomed')
        self.root.config(bg="white")

        # ===== TITLE =====
        self.logo_dash = ImageTk.PhotoImage(
            file=resource_path("images/logo_p.png")
        )

        Label(
            self.root,
            text="Student Result Management System",
            image=self.logo_dash,
            compound=LEFT,
            font=("goudy old style", 22, "bold"),
            bg="#033054",
            fg="white",
            padx=10
        ).place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=0.06
        )

        # ===== MENU FRAME =====
        M_Frame = LabelFrame(
            self.root,
            text="Menus",
            font=("times new roman", 15),
            bg="white"
        )

        M_Frame.place(
            relx=0.01,
            rely=0.08,
            relwidth=0.98,
            relheight=0.12
        )

        # ===== BUTTONS =====
        btns = [
            "Course",
            "Student",
            "Result",
            "View Result",
            "Logout",
            "Exit"
        ]

        cmds = [
            self.add_course,
            self.add_student,
            self.add_result,
            self.add_report,
            self.logout,
            self.root.destroy,
        ]

        for i in range(len(btns)):

            Button(
                M_Frame,
                text=btns[i],
                font=("goudy old style", 16, "bold"),
                bg="#0b5377",
                fg="white",
                cursor="hand2",
                command=cmds[i]
            ).place(
                relx=0.02 + i * 0.16,
                rely=0.25,
                relwidth=0.14,
                relheight=0.45
            )

        # ===== LEFT CLOCK PANEL =====
        self.clock_frame = Frame(
            self.root,
            bg="#021e2f",
            bd=3,
            relief=RIDGE
        )

        self.clock_frame.place(
            relx=0.01,
            rely=0.22,
            relwidth=0.20,
            relheight=0.66
        )

        # ===== INNER FRAME =====
        inner_frame = Frame(self.clock_frame, bg="#021e2f")
        inner_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(
            inner_frame,
            text="Current Time",
            font=("Arial", 22, "bold"),
            bg="#021e2f",
            fg="cyan"
        ).pack(pady=20)

        self.lbl_time = Label(
            inner_frame,
            font=("Arial", 28, "bold"),
            bg="#021e2f",
            fg="white"
        )

        self.lbl_time.pack(pady=10)

        self.lbl_date = Label(
            inner_frame,
            font=("Arial", 18),
            bg="#021e2f",
            fg="lightgray"
        )

        self.lbl_date.pack(pady=10)

        self.lbl_quote = Label(
            inner_frame,
            font=("Arial", 15, "bold"),
            bg="#021e2f",
            fg="yellow",
            wraplength=220,
            justify="center"
        )

        self.lbl_quote.pack(pady=25)

        # ===== QUOTES =====
        self.quotes = [
            "Dream it. Do it.",
            "Success is no accident.",
            "Never stop learning.",
            "Push yourself every day.",
            "Focus on your goals."
        ]

        self.update_clock()
        self.update_quote()

        # ===== CENTER IMAGE =====
        self.bg_original = Image.open(
            resource_path("images/bg.png")
        )

        self.bg_label = Label(
            self.root,
            bd=2,
            relief=RIDGE
        )

        self.bg_label.place(
            relx=0.25,
            rely=0.22,
            relwidth=0.68,
            relheight=0.40
        )

        self.root.bind("<Configure>", self.resize_bg)

        # ===== STATS =====
        self.lbl_course = Label(
            self.root,
            text="Total Courses\n[ 0 ]",
            font=("goudy old style", 22),
            bd=10,
            relief=RIDGE,
            bg="#e45b06",
            fg="white"
        )

        self.lbl_course.place(
            relx=0.28,
            rely=0.66,
            relwidth=0.18,
            relheight=0.12
        )

        self.lbl_student = Label(
            self.root,
            text="Total Students\n[ 0 ]",
            font=("goudy old style", 22),
            bd=10,
            relief=RIDGE,
            bg="#0590af",
            fg="white"
        )

        self.lbl_student.place(
            relx=0.50,
            rely=0.66,
            relwidth=0.18,
            relheight=0.12
        )

        self.lbl_result = Label(
            self.root,
            text="Total Results\n[ 0 ]",
            font=("goudy old style", 22),
            bd=10,
            relief=RIDGE,
            bg="#1811ef",
            fg="white"
        )

        self.lbl_result.place(
            relx=0.72,
            rely=0.66,
            relwidth=0.18,
            relheight=0.12
        )

        # ===== FOOTER =====
        Label(
            self.root,
            text="SRMS - Student Result Management System\nContact : balajiit2742@gmail.com",
            font=("goudy old style", 12),
            bg="#262626",
            fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.update_details()

    # ===== RESIZE IMAGE =====
    def resize_bg(self, event=None):

        w = self.bg_label.winfo_width()
        h = self.bg_label.winfo_height()

        if w > 1 and h > 1:

            img = self.bg_original.resize((w, h), Image.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            self.bg_label.config(image=self.bg_img)

    # ===== CLOCK =====
    def update_clock(self):

        self.lbl_time.config(text=strftime('%I:%M:%S %p'))
        self.lbl_date.config(text=strftime('%d %B %Y'))

        self.lbl_time.after(1000, self.update_clock)

    # ===== QUOTES =====
    def update_quote(self):

        self.lbl_quote.config(
            text=random.choice(self.quotes)
        )

        self.lbl_quote.after(3000, self.update_quote)

    # ===== UPDATE DETAILS =====
    def update_details(self):

        con = sqlite3.connect(resource_path("rms.db"))
        cur = con.cursor()

        try:
            cur.execute("select * from course")
            cr = cur.fetchall()

            self.lbl_course.config(
                text=f"Total Courses\n[{str(len(cr))}]"
            )

            cur.execute("select * from student")
            st = cur.fetchall()

            self.lbl_student.config(
                text=f"Total Students\n[{str(len(st))}]"
            )

            cur.execute("select * from result")
            rs = cur.fetchall()

            self.lbl_result.config(
                text=f"Total Results\n[{str(len(rs))}]"
            )

            self.lbl_course.after(500, self.update_details)

        except Exception as ex:
            messagebox.showerror(
                "Error",
                f"Error due to : {str(ex)}"
            )

    # ===== BUTTON FUNCTIONS =====
    def add_course(self):

        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):

        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    def add_result(self):

        self.new_win = Toplevel(self.root)
        self.new_obj = resultclass(self.new_win)

    def add_report(self):

        self.new_win = Toplevel(self.root)
        self.new_obj = reportclass(self.new_win)

    # ===== LOGOUT =====
    def logout(self):

        op = messagebox.askyesno(
        "Confirm",
        "Do you really want to logout ?",
        parent=self.root
    )

        if op:
            self.root.destroy()

            import sys
            import subprocess
            subprocess.Popen([sys.executable, "login.py"])

    # ===== EXIT =====
    def exit_(self):

        op = messagebox.askyesno(
            "Confirm",
            "Do you really want to exit ?",
            parent=self.root
        )

        if op:
            self.root.destroy()


# ===== MAIN =====
if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()

