from tkinter import * #Import all
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3
from PIL import Image, ImageTk


class MainLoop():
    def __init__(self):
        self.root = Tk()
        self.root.title("DOST-MIMAROPA REGIONAL STANDARDS AND "
                        "TESTING LABORATORY - Inventory System")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_system)
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+%d+%d" %(self.width, self.height, 0, 0))
        self.root.state('zoomed')
        self.root.resizable(1, 1)

        self.icon = PhotoImage(file='Resources/logo.png')
        self.root.iconphoto(True, self.icon)
        self.bg_image = Image.open("Resources/bg_image.png").convert("RGBA")
        self.bg_image.putalpha(200)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_image_label = Label(
            self.root, width=self.width, height=self.height,
            image=self.bg_image, anchor='center', bg="#77ddff"
            )
        self.bg_image_label.pack()

        self._is_logged_in = False
        self.current_user = None
        self.sys_username = 'admin'
        self.sys_password = '123456'

        self.login = LoginWindow(self)
        self.account = AccountManagement(self)

        self.reset_menu()

    def logout(self):
        result = tkMessageBox.askquestion(
            'Logging out of the System...',
            'Are you sure you want to logout?',
            icon="warning")
        if result == 'yes':
            if self._is_logged_in:
                self._is_logged_in = False
                self.current_user = None
                self.reset_menu()
                tkMessageBox.showinfo(
                    "Logged out Successfully!",
                    "You have logged out successfully from the system."
                    )
            else:
                tkMessageBox.showerror(
                    'Failed to Logout!',
                    "You are not logged in!",
                    icon="warning")

    def exit_system(self):
        result = tkMessageBox.askquestion(
            'Confirming exit command...',
            'Are you sure you want to quit?',
            icon="question")
        
        if result == 'yes':
            self.root.destroy()
            exit()

    def reset_menu(self):
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Login', command=self.login.show)
        self.filemenu.add_command(label='Logout', command=self.logout)
        self.filemenu.add_command(label='Exit', command=self.exit_system)
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        if self._is_logged_in:
            self.accmenu = Menu(self.root, tearoff=0)
            self.accmenu.add_command(label="Add New User",
                                     command=self.account.show_add_new)
            self.accmenu.add_command(label="Remove User", command=None)
            self.accmenu.add_command(label="Change Password", command=None)
            self.accmenu.add_command(label="View All Users", command=None)
            self.menubar.add_cascade(label="Account", menu=self.accmenu)
            
            self.invmenu = Menu(self.root, tearoff=0)
            self.invmenu.add_command(label='Add', command=None)
            self.invmenu.add_command(label='Remove', command=None)
            self.invmenu.add_command(label='Search', command=None)
            self.menubar.add_cascade(label='Inventory', menu=self.invmenu)

        self.helpmenu = Menu(self.root, tearoff=0)
        self.helpmenu.add_command(label='How To...', command=None)
        self.helpmenu.add_command(label='Version', command=None)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        
        self.root.config(menu=self.menubar)


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
        

    def show(self):
        if self.main._is_logged_in:
            tkMessageBox.showerror(
                    'Failed to perform operation!',
                    "You are already logged in as User ID: "+
                    f"{self.main.current_user[0]}, Username: "
                    f"{self.main.current_user[1]}!",
                    icon="warning")
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
        toplevel = Frame(self.form, width=self.w,
                         height=self.h*.4, bd=0,
                         bg="#77ddff", relief=SOLID)
        toplevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(self.form, width=self.w,
                          height=self.h*.6, bd=0,
                         bg="#77ddff",  relief=SOLID)
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_user = Label(toplevel, text='Username:',
                              font=('arial', 14), bd=10,
                              bg="#77ddff")
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(toplevel, text="Password:",
                              font=('arial', 14), bd=10,
                              bg="#77ddff")
        self.lbl_pass.grid(row=1, column=0)
        #Entry boxes
        self.user = Entry(toplevel, textvariable=self.username,
                          font=('arial', 14), width=18)
        self.user.grid(row=0, column=3)
        self.pwd = Entry(toplevel, textvariable=self.password,
                         font=('arial', 14), width=18, show="*")
        self.pwd.grid(row=1, column=3)

        #Buttons
        self.log_btn = Button(bottomlvl, text='Login',
                              font=('arial', 14), width=15,
                              command=self.login)
        self.log_btn.grid(row=0)
        self.lbl_warn = Label(bottomlvl, text="",
                              font=('arial', 12), bd=10,
                              bg="#77ddff")
        self.lbl_warn.grid(row=1)
        self.form.bind('<Return>', self.login)

    def login(self, event=None):
        self.database()
        #Check if null values are entered
        if self.username.get() == "" or self.password.get() == "":
            self.lbl_warn.config(text="Please enter the required values!",
                                 fg="red")
        else:
            #Search for user&pass from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ? "+
                "AND `password` = ?",
                (self.username.get(), self.password.get())
                )
            if self.cursor.fetchone() is not None:
                self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ? "+
                "AND `password` = ?",
                (self.username.get(), self.password.get())
                )
                data = self.cursor.fetchone()
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
                    f"Welcome back user: {self.main.current_user[1]}."
                    )
            else:
                self.lbl_warn.config(text="Invalid Username or Password!",
                                     fg="red")
                self.username.set("")
                self.password.set("")
                self.main._is_logged_in = False
        self.cursor.close()
        self.conn.close()
                

class AccountManagement():
    def __init__(self, master):
        self.main = master
        self.master = master.root
        self.checker = set('abcdefghijklmnopqrstuvwxyz1234567890_')

    def database(self, path="Data/login_details.db"):
        #Connect to database
        #Assumes database already exists
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def show_add_new(self):
        self.form = Toplevel(self.master)
        self.form.title("Add New User")
        self.w = 400
        self.h = 300
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.username = StringVar()
        self.password = StringVar()
        self.conf_pass = StringVar()
        self.authority = StringVar()
        self.lastname = StringVar()
        self.firstname = StringVar()
        
        self.add_new()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def add_new(self):
        #Frames
        toplevel = Frame(self.form, width=self.w,
                         height=self.h*.7, bd=0,
                         bg="#77ddff", relief=SOLID)
        toplevel.pack(side=TOP, pady=5)
        midlevel = Frame(self.form, width=self.w,
                         height=self.h*.15, bd=0,
                         bg="#77ddff", relief=SOLID)
        midlevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(self.form, width=self.w,
                          height=self.h*.3, bd=0,
                         bg="#77ddff",  relief=SOLID)
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_user = Label(toplevel, text='Username:',
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(toplevel, text="Password:",
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_pass.grid(row=1, column=0)
        self.lbl_conf = Label(toplevel, text="Confirm Password:",
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_conf.grid(row=2, column=0)
        self.lbl_auth = Label(toplevel, text="Authority:",
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_auth.grid(row=3, column=0)
        self.lbl_last = Label(toplevel, text="Last Name:",
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_last.grid(row=4, column=0)
        self.lbl_first = Label(toplevel, text="First Name:",
                              font=('arial', 14), bd=5,
                              bg="#77ddff")
        self.lbl_first.grid(row=5, column=0)
        #Entry boxes
        self.user = Entry(toplevel, textvariable=self.username,
                          font=('arial', 14), width=18)
        self.user.grid(row=0, column=3)
        self.pwd = Entry(toplevel, textvariable=self.password,
                         font=('arial', 14), width=18, show="*")
        self.pwd.grid(row=1, column=3)
        self.conf_pwd = Entry(toplevel, textvariable=self.conf_pass,
                         font=('arial', 14), width=18, show="*")
        self.conf_pwd.grid(row=2, column=3)
        self.auth = Entry(toplevel, textvariable=self.authority,
                         font=('arial', 14), width=18)
        self.auth.grid(row=3, column=3)
        self.last = Entry(toplevel, textvariable=self.lastname,
                         font=('arial', 14), width=18)
        self.last.grid(row=4, column=3)
        self.first = Entry(toplevel, textvariable=self.firstname,
                         font=('arial', 14), width=18)
        self.first.grid(row=5, column=3)

        #Buttons
        self.add_btn = Button(midlevel, text='Add',
                              font=('arial', 14), width=15,
                              command=self.add_user)
        self.add_btn.grid(row=0, column=0)
        self.reset_btn = Button(midlevel, text='Reset',
                              font=('arial', 14), width=15,
                              command=self.reset_form)
        self.reset_btn.grid(row=0, column=3)
        self.lbl_warn = Label(bottomlvl, text="",
                              font=('arial', 12), bd=5,
                              bg="#77ddff")
        self.lbl_warn.grid(row=0)
        self.form.bind('<Return>', self.add_user)

    def reset_form(self):
        self.username.set("")
        self.password.set("")
        self.conf_pass.set("")
        self.authority.set("")
        self.lastname.set("")
        self.firstname.set("")
        self.lbl_warn.config(text="")

    def add_user(self):
        self.database()
        
        if (self.username.get() == "" or
            self.password.get() == "" or
            self.conf_pass.get() == "" or
            self.authority.get() == "" or
            self.lastname.get() == "" or
            self.firstname.get() == ""):
            self.lbl_warn.config(text="Please enter the required values!",
                                 fg="red")
        elif (self.password.get() != self.conf_pass.get()):
            self.lbl_warn.config(text="Passwords do not match!",
                                 fg="red")
        elif len(self.password.get()) < 6:
            self.lbl_warn.config(text="Password should be at least "+
                                 "6 characters long!",
                                 fg="red")
        elif set(self.username.get().lower()).difference(
            self.checker) != set():
            self.lbl_warn.config(
                text="Username should be alphanumeric!",
                fg="red")
        else:
            #Search for username from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ?",
                (self.username.get(),)
                )
            if self.cursor.fetchone() is not None: #Username overlap!
                self.lbl_warn.config(text="Username already exists!",
                                     fg="red")
            else: #Save user as new
                self.cursor.execute(
                "INSERT INTO `Users` (username, password, "+
                "authority, lastname, firstname) "+
                f"VALUES('{self.username.get()}', "+
                f"'{self.password.get()}', '{self.authority.get()}', "+
                f"'{self.lastname.get()}', '{self.firstname.get()}')"
                )
                self.conn.commit()
                tkMessageBox.showinfo(
                    "New User successfully added!",
                    "Welcome to the DOST-MIMAROPA RSTL - Inventory "+
                    f"System user: {self.username.get()}!"
                    )
                #Reset the variables
                self.form.destroy()
                
        self.cursor.close()
        self.conn.close()
        
        
if __name__ == "__main__":
    window = MainLoop()
    window.root.mainloop()
