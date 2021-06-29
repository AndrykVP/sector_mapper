import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from lib import mapper
from pathlib import Path


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.dir = Path.home()
        self.pack(padx=8, pady=16)
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Enter Sector ID:")
        self.label.grid(column=0, row=0)

        self.input = tk.Entry(self, width=10)
        self.input.grid(column=1, row=0)
        self.input.focus()

        self.select_folder = tk.Button(self)
        self.select_folder["text"] = "Change Folder..."
        self.select_folder["command"] = self.file_path
        self.select_folder.grid(column=0, row=3, pady=(12, 0))

        self.run = tk.Button(self)
        self.run['text'] = "Generate Map"
        self.run['command'] = self.build_spreadsheet
        self.run.grid(column=1, row=3, pady=(12, 0))

        self.dir_label = tk.Label(self)
        self.dir_label['text'] = 'Output Folder:'
        self.dir_label.grid(column=0, row=1)

        self.dir_path = tk.Label(self)
        self.dir_path['text'] = self.dir
        self.dir_path.grid(column=1, row=1)


    def file_path(self):
        self.dir = filedialog.askdirectory(title='Select Output Folder', initialdir=str(Path.home()))
        self.dir_path['text'] = self.dir

    def build_spreadsheet(self):
        uid = self.input.get()
        folder = self.dir
        if not folder:
            messagebox.showerror(title='Directory Needed',
                                 message='A directory for the output file needs to be selected')
            return

        if not uid:
            messagebox.showerror(title='Sector ID Needed',
                                 message='The ID of a Sector is required to search the database')
            return

        sector = mapper.api_call('sectors', f'25:{uid}')
        if not sector:
            messagebox.showerror(title='Sector Not Found',
                                 message=f'There are no Sectors with ID {uid}')
            return

        # Raise an error if there's already a spreadsheet with the same filename as the Sector's
        if Path(f'{folder}/{sector["name"]}.xlsx').is_file():
            messagebox.showerror(title='Sector Already Mapped',
                                 message=f'Sector {sector["name"]} has already been mapped')
            return

        systems = mapper.get_systems(sector['systems'])
        shape = mapper.make_polygon(sector['coordinates']['point'])
        mapper.make_spreadsheet(sector['name'], shape, systems, folder)

        messagebox.showinfo(title='Sector Map Created',
                            message=f'The Spreadsheet for Sector {sector["name"]} has been created')


root = tk.Tk()
root.title("Sector Mapper")
app = Application(master=root)
app.mainloop()
