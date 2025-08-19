import tkinter as tk
from tkinter import messagebox
import sqlite3


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dion Areglo's App")
        self.root.geometry("500x500")
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        self.db_connection = sqlite3.connect('users.db')
        self.cursor = self.db_connection.cursor()
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users
                            (
                                username
                                TEXT
                                NOT
                                NULL
                                UNIQUE,
                                password
                                TEXT
                                NOT
                                NULL
                            );
                            """)
        self.db_connection.commit()

        self.frames["Login"] = LoginWindow(self.container, self)
        self.frames["Register"] = RegisterWindow(self.container, self)
        self.frames["Dashboard"] = DashboardWindow(self.container, self)
        self.show_frame("Login")

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

class LoginWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        login_frame = tk.Frame(self, bg="#d9d9d9", padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(login_frame, text="Username:", bg="#d9d9d9").pack(pady=(10, 0))
        self.username_entry = tk.Entry(login_frame, bd=1)
        self.username_entry.pack(pady=5)
        tk.Label(login_frame, text="Password:", bg="#d9d9d9").pack()
        self.password_entry = tk.Entry(login_frame, show="*", bd=1)
        self.password_entry.pack(pady=5)

        tk.Button(login_frame, text="Login", bg="#77c85c", fg="white", activebackground="#60a84c",
                  command=self.check_login, relief="flat", padx=10).pack(pady=10)

        tk.Button(login_frame, text="Register", command=lambda: self.controller.show_frame("Register")).pack(pady=5)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        query = "SELECT * FROM users WHERE username=? AND password=?"
        self.controller.cursor.execute(query, (username, password))

        if self.controller.cursor.fetchone():
            self.controller.show_frame("Dashboard")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class RegisterWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller

        register_frame = tk.Frame(self, bg="#d9d9d9", padx=20, pady=20)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(register_frame, text="Register", font=("Arial", 16, "bold"), bg="#d9d9d9").pack(pady=(10, 0))
        tk.Label(register_frame, text="Username:", bg="#d9d9d9").pack(pady=(10, 0))
        self.username_entry = tk.Entry(register_frame, bd=1)
        self.username_entry.pack(pady=5)
        tk.Label(register_frame, text="Password:", bg="#d9d9d9").pack()
        self.password_entry = tk.Entry(register_frame, show="*", bd=1)
        self.password_entry.pack(pady=5)
        tk.Button(register_frame, text="Register", bg="#77c85c", fg="white", activebackground="#60a84c",
                  command=self.register_user, relief="flat", padx=10).pack(pady=10)

        tk.Button(register_frame, text="Back to Login", command=lambda: self.controller.show_frame("Login")).pack(
            pady=5)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        try:
            self.controller.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if self.controller.cursor.fetchone():
                messagebox.showerror("Error", "Username already exists. Please choose another.")
            else:
                self.controller.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
                self.controller.db_connection.commit()
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.controller.show_frame("Login")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.controller.db_connection.rollback()

class DashboardWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        header_frame = tk.Frame(self, bg="#3b7a9e", height=50)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="My Application Dashboard", bg="#3b7a9e", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)

        sidebar_frame = tk.Frame(main_frame, bg="#212529", width=200)
        sidebar_frame.pack(side="left", fill="y")

        tk.Label(sidebar_frame, text="Menu", bg="#212529", fg="white", font=("Arial", 12)).pack(fill="x", pady=(10, 5),
                                                                                                padx=10)
        tk.Button(sidebar_frame, text="Home", bg="#212529", fg="white", bd=0, relief="flat",
                  activebackground="#333").pack(fill="x", pady=2)
        tk.Button(sidebar_frame, text="Profile", bg="#212529", fg="white", bd=0, relief="flat",
                  activebackground="#333").pack(fill="x", pady=2)
        tk.Button(sidebar_frame, text="Settings", bg="#212529", fg="white", bd=0, relief="flat",
                  activebackground="#333").pack(fill="x", pady=2)
        tk.Button(sidebar_frame, text="Reports", bg="#212529", fg="white", bd=0, relief="flat",
                  activebackground="#333").pack(fill="x", pady=2)

        tk.Button(sidebar_frame, text="Logout", bg="#212529", fg="white", bd=0, relief="flat", activebackground="#333",
                  command=self.logout).pack(fill="x", pady=(10, 2))

        content_frame = tk.Frame(main_frame, bg="#fff")
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        tk.Label(content_frame, text="Welcome to the Dashboard", font=("Arial", 16, "bold"), bg="#fff").pack(pady=10)

        cards_frame = tk.Frame(content_frame, bg="#fff")
        cards_frame.pack(pady=20)

        card_width = 100
        card_height = 100

        inventory_card = tk.Frame(cards_frame, bg="#a0d4e7", padx=10, pady=10, relief="raised", bd=1, width=card_width,
                                  height=card_height)
        inventory_card.grid(row=0, column=0, padx=10, pady=10)
        inventory_card.grid_propagate(False)
        tk.Label(inventory_card, text="Inventory", font=("Arial", 12), bg="#a0d4e7").pack(pady=5)
        tk.Button(inventory_card, text="Open", relief="flat",
                  command=lambda: messagebox.showinfo("Feature", "Inventory feature is not yet implemented.")).pack(
            pady=5)

        users_card = tk.Frame(cards_frame, bg="#b0e0a0", padx=10, pady=10, relief="raised", bd=1, width=card_width,
                              height=card_height)
        users_card.grid(row=0, column=1, padx=10, pady=10)
        users_card.grid_propagate(False)
        tk.Label(users_card, text="Users", font=("Arial", 12), bg="#b0e0a0").pack(pady=5)
        tk.Button(users_card, text="Open", relief="flat",
                  command=lambda: messagebox.showinfo("Feature", "Users feature is not yet implemented.")).pack(pady=5)

        sales_card = tk.Frame(cards_frame, bg="#ff9999", padx=10, pady=10, relief="raised", bd=1, width=card_width,
                              height=card_height)
        sales_card.grid(row=1, column=0, padx=10, pady=10)
        sales_card.grid_propagate(False)
        tk.Label(sales_card, text="Sales", font=("Arial", 12), bg="#ff9999").pack(pady=5)
        tk.Button(sales_card, text="Open", relief="flat",
                  command=lambda: messagebox.showinfo("Feature", "Sales feature is not yet implemented.")).pack(pady=5)

        analytics_card = tk.Frame(cards_frame, bg="#c4a5d8", padx=10, pady=10, relief="raised", bd=1, width=card_width,
                                  height=card_height)
        analytics_card.grid(row=1, column=1, padx=10, pady=10)
        analytics_card.grid_propagate(False)
        tk.Label(analytics_card, text="Analytics", font=("Arial", 12), bg="#c4a5d8").pack(pady=5)
        tk.Button(analytics_card, text="Open", relief="flat",
                  command=lambda: messagebox.showinfo("Feature", "Analytics feature is not yet implemented.")).pack(
            pady=5)

    def logout(self):
        self.controller.show_frame("Login")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

