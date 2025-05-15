import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from src import ObjToMshConverter as converter

filetypes = ( ('obj files', '*.obj'), ('All files', '*.*') )

app = tk.Tk()
app.title("ObjToMshConverter")
app.geometry("530x100")

obj_path = tk.StringVar()
out_path = tk.StringVar()
system_message = tk.StringVar()
offset_value = tk.StringVar()
offset_value.set("5")

obj_path.set("Select Model (Obj)")
out_path.set("Select Out Path or leave empty")

def open_obj_file():
    file_path = fd.askopenfile(filetypes=filetypes, initialdir="./")
    obj_path.set(file_path.name)
    
def save_path():
    dest_path = fd.askdirectory(initialdir="./")
    out_path.set(dest_path)
    
def convert():
    obj_file_path = obj_path.get()
    out_file_path = out_path.get()
    
    if obj_file_path == "Select Model (Obj)":
        text.insert(tk.END, "Please select a model file.\n")
        return
    if out_file_path == "Select Out Path or leave empty":
        out_file_path = obj_file_path
    
    # text.insert(tk.END, f"Converting {obj_file_path} to {out_file_path}...\n")
    
    test = converter.ObjToMshConverter(offset_distance=float(offset_value.get()) / 100)
    test.make_msh(obj_file_path, out_file_path)
    
    # text.insert(tk.END, f"Conversion completed!\n")

text = tk.Text(app, height=12)
text.grid(column=0, row=0, sticky='nsew')

obj_select = ttk.Button(app, text='Select Model (Obj)', command=open_obj_file)
save_select = ttk.Button(app, text='Out Path', command=save_path)
convert_button = ttk.Button(app, text='Convert', command=convert)

obj_path_label = tk.Label(app, textvariable=obj_path, width=50)
out_path_label = tk.Label(app, textvariable=out_path, width=50)
system_message_label = tk.Label(app, textvariable=system_message, width=50)
offset_label = tk.Label(app, text="Offset:", width=5)
offset_unit_label = tk.Label(app, text="cm", width=2)
offset_entry = tk.Entry(app, textvariable=offset_value, width=3)

obj_select.place(x=3,y=3)
save_select.place(x=3,y=33)
convert_button.place(x=3,y=63)
offset_label.place(x=100,y=33)
offset_entry.place(x=100,y=63)
offset_unit_label.place(x=123,y=63)

obj_path_label.place(x=150,y=3)
out_path_label.place(x=150,y=33)
system_message_label.place(x=150,y=63)

tk.mainloop()


# test = converter.ObjToMshConverter()
# test.make_msh("cube_5x5", "./examples/", "cube_5x5", "./examples/")
