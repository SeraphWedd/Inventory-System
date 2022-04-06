from tkinter import * #Import all
import tkinter.messagebox as tkMessageBox
import sqlite3

class LoginWindow():
    def __init__(self, master):
        self.main = master
        self.master = master.root
        self.sys_user = master.sys_username
        self.sys_pwd = master.sys_password

    def database(self, path="Data/login_details.db"):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        #Create databese if not yet existing
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS `Users` "+
            "(admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "+
            "username TEXT, password TEXT, authority TEXT, "
            "lastname TEXT, firstname TEXT)"
        )
        #Check if user credentials for first admin is available
        self.cursor.execute(
            f"SELECT * FROM `Users` WHERE `username` = '{self.sys_user}'"+
            f"AND `password` = '{self.sys_pwd}'"
        )
        if self.cursor.fetchone() is None:
            #Add initial credentials for admin
            self.cursor.execute(
                "INSERT INTO `Users` (username, password, "+
                "authority, lastname, firstname) "+
                f"VALUES('{self.sys_user}', '{self.sys_pwd}', 'admin', "+
                f"'admin', 'admin')"
            )
            self.conn.commit()
        
    def show_login(self):
        if self.main._is_logged_in:
            tkMessageBox.showerror(
                'Failed to perform operation!',
                "You are already logged in as User ID: "+
                f"{self.main.current_user[0]}, Username: "+
                f"{self.main.current_user[1]}!",
                icon="warning"
            )
            return
        
        self.form = Toplevel(self.master)
        self.form.title("Account Login")
        self.w = 400
        self.h = 200
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.username = StringVar()
        self.password = StringVar()
        self.login_form()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def login_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.4, bd=0,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.6, bd=0,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_user = Label(
            toplevel, text='Username:', font=('arial', 14), bd=10,
            bg="#77ddff"
        )
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(
            toplevel, text="Password:", font=('arial', 14), bd=10,
            bg="#77ddff"
        )
        self.lbl_pass.grid(row=1, column=0)
        #Entry boxes
        self.user = Entry(
            toplevel, textvariable=self.username,
            font=('arial', 14), width=18
        )
        self.user.grid(row=0, column=3)
        self.pwd = Entry(
            toplevel, textvariable=self.password,
            font=('arial', 14), width=18, show="*"
        )
        self.pwd.grid(row=1, column=3)

        #Buttons
        self.log_btn = Button(
            bottomlvl, text='Login', font=('arial', 14), width=15,
            command=self.login
        )
        self.log_btn.grid(row=0)
        
        self.lbl_warn = Label(
            bottomlvl, text="", font=('arial', 12), bd=10,
            bg="#77ddff"
            )
        self.lbl_warn.grid(row=1)
        self.form.bind('<Return>', self.login)

    def login(self, event=None):
        self.database()
        #Check if null values are entered
        if self.username.get() == "" or self.password.get() == "":
            self.lbl_warn.config(
                text="Please enter the required values!",
                fg="red"
            )
        else:
            #Search for user&pass from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ? "+
                "AND `password` = ?",
                (self.username.get(), self.password.get())
            )
            data = self.cursor.fetchone()
            
            if data is not None:
                self.main.current_user = data
                #Reset the variables
                self.username.set("")
                self.password.set("")
                self.lbl_warn.config(text="")
                
                self.form.destroy()
                self.main._is_logged_in = True
                self.main.reset_menu()
                tkMessageBox.showinfo(
                    "Logged in Successfully!",
                    f"Welcome back user {self.main.current_user[4]}!"
                )
            else:
                self.lbl_warn.config(
                    text="Invalid Username or Password!",
                    fg="red"
                )
                self.password.set("")
                self.main._is_logged_in = False
        self.cursor.close()
        self.conn.close()
