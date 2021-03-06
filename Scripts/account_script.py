from tkinter import * #Import all
import tkinter.messagebox as tkMessageBox
import sqlite3

class AccountManagement():
    def __init__(self, master):
        self.main = master
        self.master = master.root
        self.checker = set('abcdefghijklmnopqrstuvwxyz1234567890_')

        self.username = StringVar()
        self.password = StringVar()
        self.new_pass = StringVar()
        self.conf_pass = StringVar()
        self.authority = StringVar()
        self.lastname = StringVar()
        self.firstname = StringVar()

        self.column_names = [
            "User ID",
            "Username",
            "Password",
            "Authority",
            "Last Name",
            "First Name"
        ]
        self.db_entry_names = [
            'admin_id',
            'username',
            'password',
            'authority',
            'lastname',
            'firstname'
        ]

    def database(self, path="Data/login_details.db"):
        #Connect to database
        #Assumes database already exists
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def reset_form(self):
        self.username.set("")
        self.password.set("")
        self.new_pass.set("")
        self.conf_pass.set("")
        self.authority.set("")
        self.lastname.set("")
        self.firstname.set("")
        self.lbl_warn.config(text="")

    def show_add_user(self):
        self.form = Toplevel(self.master)
        self.form.title("Add New User")
        self.w = 400
        self.h = 300
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.add_user_form()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def add_user_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.7, bd=0,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=5)
        midlevel = Frame(
            self.form, width=self.w, height=self.h*.15, bd=0,
            bg="#77ddff", relief=SOLID
        )
        midlevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.3, bd=0,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_user = Label(
            toplevel, text='Username:', font=('arial', 14), bd=5,
            bg="#77ddff"
        )
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(
            toplevel, text="Password:", font=('arial', 14), bd=5,
            bg="#77ddff"
        )
        self.lbl_pass.grid(row=1, column=0)
        self.lbl_conf = Label(
            toplevel, text="Confirm Password:", font=('arial', 14),
            bd=5, bg="#77ddff"
        )
        self.lbl_conf.grid(row=2, column=0)
        self.lbl_auth = Label(
            toplevel, text="Authority:", font=('arial', 14), bd=5,
            bg="#77ddff"
        )
        self.lbl_auth.grid(row=3, column=0)
        self.lbl_last = Label(
            toplevel, text="Last Name:", font=('arial', 14), bd=5,
            bg="#77ddff"
        )
        self.lbl_last.grid(row=4, column=0)
        self.lbl_first = Label(
            toplevel, text="First Name:", font=('arial', 14), bd=5,
            bg="#77ddff"
        )
        self.lbl_first.grid(row=5, column=0)
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
        self.conf_pwd = Entry(
            toplevel, textvariable=self.conf_pass,
            font=('arial', 14), width=18, show="*"
        )
        self.conf_pwd.grid(row=2, column=3)
        self.auth = Entry(toplevel, textvariable=self.authority,
                         font=('arial', 14), width=18)
        self.auth.grid(row=3, column=3)
        self.last = Entry(
            toplevel, textvariable=self.lastname,
            font=('arial', 14), width=18
        )
        self.last.grid(row=4, column=3)
        self.first = Entry(
            toplevel, textvariable=self.firstname,
            font=('arial', 14), width=18
        )
        self.first.grid(row=5, column=3)

        #Buttons
        self.add_btn = Button(
            midlevel, text='Add', font=('arial', 14), width=15,
            command=self.add_user
        )
        self.add_btn.grid(row=0, column=0)
        self.reset_btn = Button(
            midlevel, text='Reset', font=('arial', 14), width=15,
            command=self.reset_form
        )
        self.reset_btn.grid(row=0, column=3)
        self.lbl_warn = Label(
            bottomlvl, text="", font=('arial', 12), bd=5,
            bg="#77ddff"
        )
        self.lbl_warn.grid(row=0)
        self.form.bind('<Return>', self.add_user)

    def add_user(self, event=None):
        if self.main.current_user[3] != 'admin':
            tkMessageBox.showerror(
                'Error: Insufficient Authority',
                "Only admins can add new users!",
                icon="warning"
            )
            return
        
        self.database()
        
        if (self.username.get() == "" or
            self.password.get() == "" or
            self.conf_pass.get() == "" or
            self.authority.get() == "" or
            self.lastname.get() == "" or
            self.firstname.get() == ""):
            self.lbl_warn.config(
                text="Please enter the required values!",
                fg="red"
            )
        elif (self.password.get() != self.conf_pass.get()):
            self.lbl_warn.config(
                text="Passwords do not match!",
                fg="red"
            )
        elif len(self.password.get()) < 6:
            self.lbl_warn.config(
                text="Password should be at least "+
                "6 characters long!",
                fg="red"
            )
        elif set(self.username.get().lower()).difference(
            self.checker) != set():
            self.lbl_warn.config(
                text="Username should be alphanumeric!",
                fg="red"
            )
        elif self.authority.get() not in ['admin', 'guest']:
            self.lbl_warn.config(
                text="Authority can only be 'admin' or 'guest'!",
                fg="red"
            )
            
        else:
            #Search for username from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ?",
                (self.username.get(),)
            )
            if self.cursor.fetchone() is not None: #Username overlap!
                self.lbl_warn.config(
                    text="Username already exists!",
                    fg="red"
                )
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
                #Destroy form after use
                self.reset_form()
                self.form.destroy()

    def show_remove_user(self):
        self.form = Toplevel(self.master)
        self.form.title("Remove User")
        self.w = 400
        self.h = 250
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.remove_user_form()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def remove_user_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.2, bd=0,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=5)
        midlevel = Frame(
            self.form, width=self.w, height=self.h*.4, bd=0,
            bg="#77ddff", relief=SOLID
        )
        midlevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.4, bd=0,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_banner = Label(
            toplevel,
            text="Enter the credentials of User to remove:",
            font=('arial', 14), bd=10, bg="#77ddff"
        )
        self.lbl_banner.grid(row=0, columnspan=3)
        self.lbl_user = Label(
            midlevel, text='Username:', font=('arial', 14),
            bd=10, bg="#77ddff"
        )
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(
            midlevel, text="Password:", font=('arial', 14),
            bd=10, bg="#77ddff"
        )
        self.lbl_pass.grid(row=1, column=0)
        #Entry boxes
        self.user = Entry(
            midlevel, textvariable=self.username,
            font=('arial', 14), width=18
        )
        self.user.grid(row=0, column=3)
        self.pwd = Entry(
            midlevel, textvariable=self.password,
            font=('arial', 14), width=18, show="*"
        )
        self.pwd.grid(row=1, column=3)

        #Buttons
        self.log_btn = Button(
            bottomlvl, text='Remove',
            font=('arial', 14), width=15,
            command=self.remove_user
        )
        self.log_btn.grid(row=0)
        self.lbl_warn = Label(
            bottomlvl, text="", font=('arial', 12), bd=10,
            bg="#77ddff"
        )
        self.lbl_warn.grid(row=1)
        self.form.bind('<Return>', self.remove_user)
    
    def remove_user(self, event=None):
        if self.main.current_user[3] != 'admin':
            tkMessageBox.showerror(
                'Error: Insufficient Authority',
                "Only admins can remove users!",
                icon="warning"
            )
            return
        
        self.database()
        
        if (self.username.get() == "" or self.password.get() == ""):
            self.lbl_warn.config(
                text="Please enter the required values!",
                fg="red"
            )
        elif set(self.username.get().lower()).difference(
            self.checker) != set():
            self.lbl_warn.config(
                text="Username should be alphanumeric!",
                fg="red"
            )
        else:
            #Search for username from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ?",
                (self.username.get(),)
            )
            if self.cursor.fetchone() is None: #Username not found!
                self.lbl_warn.config(
                    text="Username do not exist!",
                    fg="red"
                )
            else: #Check if password match
                #Search for user&pass from database
                self.cursor.execute(
                    "SELECT * FROM `Users` WHERE `username` = ? "+
                    "AND `password` = ?",
                    (self.username.get(), self.password.get())
                )
                data = self.cursor.fetchone()
                if data is None: #Username&Password do not match!
                    self.lbl_warn.config(
                        text="The password is incorrect!",
                        fg="red"
                    )
                else:
                    self.cursor.execute(
                        "DELETE FROM `Users` WHERE `username` = ? "+
                        "AND `password` = ?",
                        (self.username.get(), self.password.get())
                    )
                    self.conn.commit()
                        
                    tkMessageBox.showinfo(
                        "User successfully removed!",
                        f"System user {self.username.get()} " +
                        "has been successfully removed!"
                    )
                    #Destroy form after use
                    self.reset_form()
                    self.form.destroy()
                
        self.cursor.close()
        self.conn.close()

    def show_edit_account(self):
        self.form = Toplevel(self.master)
        self.form.title("Edit Account")
        self.w = 400
        self.h = 200
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.edit_account_form()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def edit_account_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.6, bd=0,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=5)
        midlevel = Frame(
            self.form, width=self.w, height=self.h*.2, bd=0,
            bg="#77ddff", relief=SOLID
        )
        midlevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.2, bd=0,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_last = Label(
            toplevel, text="Last Name:", font=('arial', 14),
            bd=5, bg="#77ddff"
        )
        self.lbl_last.grid(row=0, column=0)
        self.lbl_first = Label(
            toplevel, text="First Name:", font=('arial', 14),
            bd=5, bg="#77ddff"
        )
        self.lbl_first.grid(row=1, column=0)
        #Entry boxes
        self.last = Entry(
            toplevel, textvariable=self.lastname,
            font=('arial', 14), width=18
        )
        self.last.grid(row=0, column=3)
        self.first = Entry(
            toplevel, textvariable=self.firstname,
            font=('arial', 14), width=18
        )
        self.first.grid(row=1, column=3)
        self.lastname.set(self.main.current_user[4])
        self.firstname.set(self.main.current_user[5])

        #Buttons
        self.add_btn = Button(
            midlevel, text='Update',
            font=('arial', 14), width=15,
            command=self.edit_account
        )
        self.add_btn.grid(row=0, column=0)
        
        self.lbl_warn = Label(
            bottomlvl, text="", font=('arial', 12), bd=5,
            bg="#77ddff"
        )
        self.lbl_warn.grid(row=0)
        self.form.bind('<Return>', self.edit_account)
    
    def edit_account(self, event=None):
        self.database()

        if (self.firstname.get() == "" or self.lastname.get() == ""):
            self.lbl_warn.config(
                text="Please enter the required values!",
                fg="red"
            )
        else:
            #Search for current user from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `admin_id` = ?",
                (self.main.current_user[0],)
            )
            
            if self.cursor.fetchone() is None: #Username not found!
                self.lbl_warn.config(
                    text="Account do not exist!",
                    fg="red"
                )
            else: #if found, edit the entries
                self.cursor.execute(
                    "UPDATE `Users` SET `lastname` = ?, "+
                    "`firstname` = ? WHERE `admin_id` = ?",
                    (self.lastname.get(), self.firstname.get(),
                     self.main.current_user[0])
                )
                self.conn.commit()
                #Update current user
                self.cursor.execute(
                    "SELECT * FROM `Users` WHERE `admin_id` = ?",
                    (self.main.current_user[0],)
                )
                data = self.cursor.fetchone()
                self.main.current_user = data
                
                tkMessageBox.showinfo(
                    "Info",
                    f"User {self.main.current_user[1]}'s "+
                    "details updated successfully!"
                )
                #Destroy form after use
                self.reset_form()
                self.form.destroy()

    def show_change_password(self):
        self.form = Toplevel(self.master)
        self.form.title("Change Password")
        self.w = 400
        self.h = 300
        x = self.master.winfo_screenwidth()//2 - self.w//2
        y = self.master.winfo_screenheight()//2 - self.h//2
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, x, y))
        self.form.config(bg="#77ddff")
        self.form.resizable(0, 0)

        self.change_password_form()
        self.form.transient(self.master)
        self.form.grab_set()
        self.master.wait_window(self.form)

    def change_password_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.2, bd=0,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=5)
        midlevel = Frame(
            self.form, width=self.w, height=self.h*.6, bd=0,
            bg="#77ddff", relief=SOLID
        )
        midlevel.pack(side=TOP, pady=5)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.2, bd=0,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=5)
        #Labels
        self.lbl_banner = Label(
            toplevel,
            text="Enter your Password:",
            font=('arial', 14), bd=10, bg="#77ddff"
        )
        self.lbl_banner.grid(row=0, columnspan=3)
        self.lbl_user = Label(
            midlevel, text='Old Password:', font=('arial', 14),
            bd=10, bg="#77ddff"
        )
        self.lbl_user.grid(row=0, column=0)
        self.lbl_pass = Label(
            midlevel, text="New Password:", font=('arial', 14),
            bd=10, bg="#77ddff"
        )
        self.lbl_pass.grid(row=1, column=0)
        self.lbl_pass = Label(
            midlevel, text="Confirm Password:", font=('arial', 14),
            bd=10, bg="#77ddff"
        )
        self.lbl_pass.grid(row=2, column=0)
        #Entry boxes
        self.user = Entry(
            midlevel, textvariable=self.password,
            font=('arial', 14), width=18, show="*"
        )
        self.user.grid(row=0, column=3)
        self.pwd = Entry(
            midlevel, textvariable=self.new_pass,
            font=('arial', 14), width=18, show="*"
        )
        self.pwd.grid(row=1, column=3)
        self.pwd = Entry(
            midlevel, textvariable=self.conf_pass,
            font=('arial', 14), width=18, show="*"
        )
        self.pwd.grid(row=2, column=3)

        #Buttons
        self.log_btn = Button(
            bottomlvl, text='Confirm',
            font=('arial', 14), width=15,
            command=self.change_password
        )
        self.log_btn.grid(row=0)
        self.lbl_warn = Label(
            bottomlvl, text="", font=('arial', 12), bd=10,
            bg="#77ddff"
        )
        self.lbl_warn.grid(row=1)
        self.form.bind('<Return>', self.change_password)
    
    def change_password(self, event=None):
        self.database()
        
        if (self.password.get() == "" or
            self.conf_pass.get() == "" or
            self.new_pass.get() == ""):
            self.lbl_warn.config(
                text="Please enter the required values!",
                fg="red"
            )
        elif self.password.get() != self.main.current_user[2]:
            self.lbl_warn.config(
                text="Password is incorrect!",
                fg="red"
            )
        elif self.main.current_user[1] == "admin":
            self.lbl_warn.config(
                text="Cannot change admin default password!",
                fg="red"
            )
        elif self.new_pass.get() != self.conf_pass.get():
            self.lbl_warn.config(
                text="Password do not match!",
                fg="red"
            )
        elif len(self.new_pass.get()) < 6:
            self.lbl_warn.config(
                text="Password should be at least "+
                "6 characters long!",
                fg="red"
            )
        else:
            #Search for username from database
            self.cursor.execute(
                "SELECT * FROM `Users` WHERE `username` = ?",
                (self.main.current_user[1],)
            )
            if self.cursor.fetchone() is None: #Username not found!
                self.lbl_warn.config(
                    text="Account do not exist!",
                    fg="red"
                )
            else: #Check if password match
                #Search for user&pass from database
                self.cursor.execute(
                    "SELECT * FROM `Users` WHERE `username` = ? "+
                    "AND `password` = ?",
                    (self.main.current_user[1], self.password.get())
                )
                data = self.cursor.fetchone()
                if data is None: #Username&Password do not match!
                    self.lbl_warn.config(
                        text="The password is incorrect!",
                        fg="red"
                    )
                else:
                    self.cursor.execute(
                        "UPDATE `Users` SET `password` = ? "+
                        "WHERE `admin_id` = ?",
                        (self.new_pass.get(),
                         self.main.current_user[0])
                    )
                    self.conn.commit()

                    #Update current user
                    self.cursor.execute(
                        "SELECT * FROM `Users` WHERE `username` = ? "+
                        "AND `password` = ?",
                        (self.main.current_user[1], self.new_pass.get())
                    )
                    self.main.current_user = self.cursor.fetchone()
                    
                    tkMessageBox.showinfo(
                        "Password changed successfully!",
                        f"System user {self.main.current_user[1]}'s " +
                        "password has been successfully changed!"
                    )
                    #Destroy form after use
                    self.reset_form()
                    self.form.destroy()
                
        self.cursor.close()
        self.conn.close()

    def show_view_all_users(self):
        
        if self.main.current_user[3] != 'admin':
            tkMessageBox.showerror(
                'Error: Insufficient Authority',
                "Only admins can view all users!",
                icon="warning"
            )
            return
            
        self.form = Toplevel(self.master)
        self.form.title("View All Users")
        self.w = self.master.winfo_screenwidth()
        self.h = self.master.winfo_screenheight()
        self.form.geometry("%dx%d+%d+%d" %(self.w, self.h, 0, 0))
        self.form.config(bg="#77ddff")
        self.form.resizable(1, 1)
        self.form.state('zoomed')
        self.master.withdraw()
        
        def  on_exit(event):
            self.master.deiconify()
            self.master.state('zoomed')
            
        self.form.bind("<Destroy>", on_exit)
        self.view_all_users_form()

    def view_all_users_form(self):
        #Frames
        toplevel = Frame(
            self.form, width=self.w, height=self.h*.1, bd=2,
            bg="#77ddff", relief=SOLID
        )
        toplevel.pack(side=TOP, pady=2)
        midlevel = Frame(
            self.form, width=self.w, height=self.h*.8, bd=2,
            bg="#77ddff", relief=SOLID
        )
        midlevel.pack(side=TOP, pady=2)
        bottomlvl = Frame(
            self.form, width=self.w, height=self.h*.1, bd=2,
            bg="#77ddff",  relief=SOLID
        )
        bottomlvl.pack(side=TOP, pady=2)

        #Labels
        self.search_bar = Label(
            toplevel,
            text="Search:",
            font=('arial', 12), bg="#77ddff"
        )
        self.search_bar.grid(row=0, column=0)

        #Entry boxes
        self.search_kwd = StringVar()
        self.keyword = Entry(
            toplevel, textvariable=self.search_kwd,
            font=('arial', 12), width=100
        )
        self.keyword.grid(row=0, column=2)
        
        #Buttons
        self.search_btn = Button(
            toplevel, text='Confirm',
            font=('arial', 12), width=10,
            command=self.view_all_users
        )
        self.search_btn.grid(row=0, column=10)
        self.form.bind("<Return>", self.view_all_users)

        #Tree
        scrollbar_x = Scrollbar(midlevel, orient=HORIZONTAL)
        scrollbar_y = Scrollbar(midlevel, orient=VERTICAL)
        
        self.tree = ttk.Treeview(
            midlevel,
            columns=self.column_names,
            selectmode="extended",
            height=self.h*0.8,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        for c in self.column_names:
            self.tree.heading(c, text=c, anchor=N)

        for i in range(len(self.column_names)+1):
            if i > 1:
                self.tree.column(f"#{i}", stretch=NO, minwidth=50, width=200)
            else:
                self.tree.column(f"#{i}", stretch=NO, minwidth=0, width=50)
        self.tree.pack()
        
        self.view_all_users()
        
    def view_all_users(self, event=None):
        self.database()
        self.tree.delete(*self.tree.get_children())

        #Search keyword from all columns
        kwd = self.search_kwd.get()
        if kwd != "":
            search_text = "SELECT * FROM `Users` WHERE ({})".format(
                " OR ".join(
                    f"`{col}` LIKE '%{'%'.join(kwd.split())}%'" for
                    col in self.db_entry_names[1:]
                )
            )
        else:
            search_text = "SELECT * from `Users`"
            
        self.cursor.execute(search_text)
        
        for data in self.cursor.fetchall():
            self.tree.insert('', 'end', values=(data))
            
        #self.form.destroy()
        self.cursor.close()
        self.conn.close()

