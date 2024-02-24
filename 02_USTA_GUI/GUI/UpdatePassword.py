import tkinter as tk 
from tkinter import messagebox

class UpdatePassword():

    def __init__(self, master):
        self.toplevel = tk.Toplevel(master)
        self.toplevel.title("Actualizar Contraseña")
        self.toplevel.geometry("500x500")
        self.cod = tk.IntVar()
        self.password_old = tk.StringVar()
        self.password_new = tk.StringVar()
        self.password_new_verification = tk.StringVar()
        self.build()
        
    def build(self):
        self.frame = tk.Frame(self.toplevel)
        self.cod_lbl = tk.Label(self.frame, text="Codigo:")
        self.cod_entry = tk.Entry(self.frame, textvariable=self.cod)
        self.password_old_lbl = tk.Label(self.frame, text="Antigua Contraseña: ")
        self.password_old_entry = tk.Entry(self.frame, textvariable=self.password_old)        
        self.password_new_lbl = tk.Label(self.frame, text="Nueva Contraseña: ")
        self.password_new_entry = tk.Entry(self.frame, textvariable=self.password_new)        
        self.password_2_lbl = tk.Label(self.frame, text="Valide la Nueva Contraseña: ")
        self.password_2_entry = tk.Entry(self.frame, textvariable=self.password_new_verification)
        
        self.create_btn = tk.Button(self.frame, text="Actualizar Contraseña", command=self.toplevel.destroy)
        self.cod_lbl.grid(row=0, column=0, sticky="nw")
        self.cod_entry.grid(row=0, column=1, sticky="nw")
        self.password_old_lbl.grid(row=1, column=0, sticky="nw")
        self.password_old_entry.grid(row=1, column=1, sticky="nw")
        self.password_new_lbl.grid(row=2, column=0, sticky="nw")
        self.password_new_entry.grid(row=2, column=1, sticky="nw")   
        self.password_2_lbl.grid(row=3, column=0, sticky="nw")
        self.password_2_entry.grid(row=3, column=1, sticky="nw")
        self.create_btn.grid(row=4, column=3, sticky="nw")
        self.frame.grid(padx=10, pady=10, sticky="nswe")
        
    def show(self):
        self.toplevel.grab_set()  # Block events in other windows
        self.toplevel.wait_window()  # Wait until the dialog is closed
        return self.updatePssw()
    
    def updatePssw(self):
        if self.password_new.get() != self.password_new_verification.get():
            messagebox.showerror("Password Error", "Las contraseñas no coinciden")
            return
        return (self.cod.get(),
               self.password_old.get(),
              self.password_new.get())
        