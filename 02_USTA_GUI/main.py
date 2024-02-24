import tkinter as tk

from GUI.MainWindow import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Administrar Tomasinos")
    root.geometry("700x500")
    main = MainWindow(root)
    root.mainloop()
    