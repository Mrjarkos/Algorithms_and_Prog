import tkinter as tk

def trim_and_fill(lst, desired_length):
    # Trim the list if lenght is greater
    if len(lst) > desired_length:
        lst = lst[:desired_length]
    elif len(lst) < desired_length:
        # Step 2: Fill with None values if smaller
        lst.extend([None] * (desired_length - len(lst)))
    return lst


class Table(tk.Frame):
    
    header : list
    rows_displayed: int = 10
    cols_displayed: int = 10
    data = list
    
    def __init__(self, parent, header, *args, **kwargs):
        self.header = header
        self.data = []
        super().__init__(parent, *args, **kwargs)
        self.frame = tk.Frame(self)
        ## Create Labels
        self.display_headers()
        self.frame.grid()
       
    def display_headers(self):
        for i, p in enumerate(self.header):
            label = tk.Label(self.frame, text=p)
            label.grid(row=0, column=i, pady=10, sticky="nw")
    
    def set_data(self, data):
        self.data = data
    
    def insert(self, row: list):
        row = trim_and_fill(row, len(self.header))
        self.data.append(row)
        print(self.data)
    
    def update(self):
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.display_headers()
        for i, row in enumerate(self.data, start=1):
            for j, cell in enumerate(row):
                label = tk.Label(self.frame, text=cell)
                label.grid(row=i, column=j, pady=10, sticky="nw")
        self.frame.grid()
        super().update()