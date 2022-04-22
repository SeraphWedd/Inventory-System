from tkinter import * #Import all
import tkinter.messagebox as tkMessageBox
import tkinter.ttk as ttk
import sqlite3
import sys
from PIL import Image, ImageTk

from Scripts.login_script import LoginWindow
from Scripts.account_script import AccountManagement


class MainLoop():
    def __init__(self):
        self.root = Tk()
        self.root.title(
            "DOST-MIMAROPA REGIONAL STANDARDS AND " +
            "TESTING LABORATORY - Inventory System"
        )
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
            icon="warning"
        )
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
                    icon="warning"
                )

    def exit_system(self):
        result = tkMessageBox.askquestion(
            'Confirming exit command...',
            'Are you sure you want to quit?',
            icon="question"
        )
        
        if result == 'yes':
            self._is_logged_in = False
            self.root.destroy()
            sys.exit()

    def reset_menu(self):
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label='Login',
            command=self.login.show_login
        )
        self.filemenu.add_command(
            label='Logout',
            command=self.logout
        )
        self.filemenu.add_command(
            label='Exit',
            command=self.exit_system
        )
        self.menubar.add_cascade(
            label='File',
            menu=self.filemenu
        )

        if self._is_logged_in:
            self.accmenu = Menu(self.root, tearoff=0)
            self.accmenu.add_command(
                label="Add New User",
                command=self.account.show_add_user
            )
            self.accmenu.add_command(
                label="Remove User",
                command=self.account.show_remove_user
            )
            self.accmenu.add_command(
                label="Edit Account",
                command=self.account.show_edit_account
            )
            self.accmenu.add_command(
                label="Change Password",
                command=self.account.show_change_password
            )
            self.accmenu.add_command(
                label="View All Users",
                command=self.account.show_view_all_users
            )
            self.menubar.add_cascade(label="Account", menu=self.accmenu)
            
            self.invmenu = Menu(self.root, tearoff=0)
            self.invmenu.add_command(
                label='Add',
                command=None
            )
            self.invmenu.add_command(
                label='Remove',
                command=None
            )
            self.invmenu.add_command(
                label='Search',
                command=None
            )
            self.invmenu.add_command(
                label='View All Items',
                command=None
            )
            self.menubar.add_cascade(label='Inventory', menu=self.invmenu)

        self.helpmenu = Menu(self.root, tearoff=0)
        self.helpmenu.add_command(
            label='How To...',
            command=None
        )
        self.helpmenu.add_command(
            label='Version',
            command=None
        )
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        
        self.root.config(menu=self.menubar)
        
if __name__ == "__main__":
    window = MainLoop()
    window.root.mainloop()
