import textwrap
import tkinter as tk
from tkinter import messagebox
from constants import COLORS

class ScrollbarText(tk.Text):
    
    def __init__(self, parent, placeholder="", max_height=10, min_height=1, resize=True, command = None, *args, **kwargs):
        self.Frame = tk.Frame(parent)
        self.max_height = max_height
        self.min_height = min_height
        
        super().__init__(self.Frame, undo=True, autoseparators=True, maxundo=80, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "gray70"
        self.default_fg_color = self["fg"]
        self.build()
        self.Frame.pack(fill="both", padx=10, pady=10)
        self.command = command
        # Place holder
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.put_placeholder()
        
        # Send with Enter and alt+enter resize (\n)
        self.bind('<Return>', self.handle_return)
        
        # Resizing
        if resize:
            self.bind("<KeyRelease>", self.auto_resize)
            self.auto_resize(None)

    def handle_return(self, event):
        ## new line is handled with alt or shift
        if event.state&0x20000 | event.state&0x01:
            return
        
        self.delete("insert")
        ## execute command If no alt
        if self.command is not None:
            data = self.get_Text()
            self.delete("1.0", "end")
            self.command(data)

    def build(self):
        # Set the horizontal limit of the text box
        self.configure(wrap="word")
        ## Add a scrollbar to the textbox
        self.scrollbar = tk.Scrollbar(self.Frame) 
        self.configure(yscrollcommand=self.scrollbar.set) 
        self.pack(side=tk.LEFT)
        self.scrollbar.config(command=self.yview) 
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def auto_resize(self, event):
        if event is not None and event.keysym == "Return" and event.state==0x08:
            self.delete("insert")
            return
        # Get the current position of the scrollbar
        init_pos = self.yview()[0]
        
        # Calculate the number of lines being displayed
        end_idx = self.index("end-1c")
        ### Total lines with \n
        end_lines = int(end_idx.split(".")[0]) 
        
        ### Total lines wrapped if long text
        text = self.get_Text()
        lines = textwrap.wrap(text, width = self.cget("width"))
        # Min lines has to be 1, even there is no text
        wrapped_lines = len(lines) if len(lines) != 0 else 1
        n = wrapped_lines + end_lines - 1
        
        # Set the height of the text box
        if self.min_height < n < self.max_height:
            height = n
        elif n <= self.min_height: 
            height = self.min_height
        else: 
            height = self.max_height
            
        self.config(height = height)
        
        # Disable the scrollbar if not necessary
        self.config(yscrollcommand = self.scrollbar.set if n>self.max_height else "")
        
        # Restore the scrollbar position
        self.yview_moveto(init_pos)

    def set_Text(self, text:str):
        if not text:
            self.put_placeholder()
        else:
            self.remove_placeholder()
            self.insert("1.0", text)

    def get_Text(self):
        #-1c extract the new line character
        text = self.get("1.0", "end-1c")
        return text if text != self.placeholder else ""

    def put_placeholder(self):
        self.insert("1.0", self.placeholder)
        self["fg"] = self.placeholder_color

    def remove_placeholder(self):
        self.delete("1.0", "end")
        self["fg"] = self.default_fg_color

    def focus_in(self, event):
        if self["fg"] == self.placeholder_color:
            self.remove_placeholder()

    def focus_out(self, event):
        if not self.get_Text():
            self.put_placeholder()

class MainWindow(tk.Tk):
    
    def __init__(self, usr_name, id, command=None):
        super().__init__()
        self.title(f"Chat de {usr_name}")
        self.geometry("700x500")
        self.resizable(width=False, height=False)
        self.usr_name = usr_name
        self.id = id
        self.Frame = tk.Frame(self)
        self.send_fcn = command
        self.build()
        self.Frame.grid(sticky="nswe", padx=10, pady=10)
    
    def send(self, data):
        ## The information is implicit on the connection
        # info_dict = {
        #     "id" : self.id,
        #     "nick": self.usr_name,
        #     "data": data
        # }
        self.send_fcn(data)
    
    def send_to_server_chat(self, time:str, name:str, id:int, data:str):
        self.server_chat["state"] = "normal"
        if not data:
            ## Server is shutdown
            messagebox.showerror("Server shutdown", "Server was shutdown, we have to close the client")
            self.destroy()
            
        header = f"{time} | {name}"
        if id ==-1:
            ## Message from server
            self.server_chat.insert("end", f"{header}: {data}\n","server")
        elif self.id == id:
            ## Message from yourself
            self.server_chat.insert("end", f"{time} | You: {data}\n","right")
        else:
            self.server_chat.insert("end", f"{header}: ", COLORS[id%len(COLORS)])
            self.server_chat.insert("end", f"{data}\n", "left")
             
        self.server_chat["state"] = "disabled"
    
    def build(self):
        self.server_chat = ScrollbarText(self.Frame, resize=False)
        # Prevent editing chat
        self.server_chat["state"] = "disabled"
        self.server_chat.focus_in(None)
        ## Just format (colors and so on)
        self.server_chat.tag_configure("right", justify="right")
        self.server_chat.tag_configure("left", justify="left")
        self.server_chat.tag_configure("server", justify="left", foreground=self.server_chat.placeholder_color)
        for color in COLORS:
            self.server_chat.tag_configure(color, justify="left", foreground=color)
            
        self.message_box = ScrollbarText(self.Frame, resize=True, min_height=1, max_height=3, 
                                         command=self.send,
                                         placeholder="Type a message")
    
class AskName():
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat")
        self.root.geometry("300x100")
        self.root.resizable(width=False, height=False)
        self.name = tk.StringVar()
        name_label = tk.Label(self.root, text="Usuario: ")
        name_entry = tk.Entry(self.root, textvariable=self.name)
        btn = tk.Button(self.root, text="Ingresar", command=self.validate_name)
        name_label.grid(padx=10, pady=10, column=0, row=0)
        name_entry.grid(padx=10, pady=10, column=1, row=0, columnspan=2)
        btn.grid(padx=10, pady=10, column=3, row=1)
        self.root.bind("<Return>", lambda x: self.validate_name())
        self.root.mainloop()


    def validate_name(self):
        if self.name.get() == "":
            messagebox.showerror("Sin Nombre", "Por Favor ingrese un nombre")
        else:
            self.root.destroy()