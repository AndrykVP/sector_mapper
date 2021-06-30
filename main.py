import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from lib import mapper
from pathlib import Path


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sector Mapper")
        self.master.eval('tk::PlaceWindow . center')
        self.master.resizable(False, False)
        self.buttons = {}
        self.button_labels = {}
        self.button_circles = {}
        self.pack(padx=8, pady=16)
        self.create_variables()
        self.create_widgets()
        self.create_buttons()

    def create_variables(self):
        self.dir = tk.StringVar()
        self.dir.set(Path.home())

        self.colors = {
            'empty': tk.StringVar(),
            'occupied': tk.StringVar(),
            'outter': tk.StringVar()
        }

        self.colors['empty'].set('#0201ff')
        self.colors['occupied'].set('#48ff00')
        self.colors['outter'].set('#666666')

    def create_widgets(self):
        self.id_label = tk.Label(self, text="Enter Sector ID:")
        self.id_label.grid(column=1, row=0, sticky='E')

        self.id_input = tk.Entry(self, width=10)
        self.id_input.grid(column=2, row=0, sticky='W')
        self.id_input.bind('<Return>', self.build_spreadsheet)

        self.dir_label = tk.Label(self, text="Output Folder:")
        self.dir_label.grid(column=1, row=1, sticky='E')

        self.dir_path = tk.Label(self, text=self.dir.get())
        self.dir_path.grid(column=2, row=1, sticky='W')

        self.select_folder = tk.Button(self, text="Change Folder...", command=self.file_path)
        self.select_folder.grid(column=1, row=5, pady=(12, 0), sticky='E')

        self.run = tk.Button(self, text="Generate Map", command=self.build_spreadsheet)
        self.run.grid(column=2, row=5, pady=(12, 0), sticky='W')

    def create_buttons(self):
        self.button_labels['empty'] = tk.Label(self, text=f"Empty Squares:")
        self.button_labels['empty'].grid(column=1, row=2, sticky='E')
        self.buttons['empty'] = tk.Button(self,
                                          text="Choose Color",
                                          command=lambda: self.choose_color("empty", 2))
        self.buttons["empty"].grid(column=2, row=2, sticky='W')
        self.create_color_circle("empty", 2)

        self.button_labels['occupied'] = tk.Label(self, text=f"Systems:")
        self.button_labels['occupied'].grid(column=1, row=3, sticky='E')
        self.buttons['occupied'] = tk.Button(self,
                                             text="Choose Color",
                                             command=lambda: self.choose_color("occupied", 3))
        self.buttons["occupied"].grid(column=2, row=3, sticky='W')
        self.create_color_circle("occupied", 3)

        self.button_labels['outter'] = tk.Label(self, text=f"Out of bounds:")
        self.button_labels['outter'].grid(column=1, row=4, sticky='E')
        self.buttons['outter'] = tk.Button(self,
                                           text="Choose Color",
                                           command=lambda: self.choose_color("outter", 4))
        self.buttons["outter"].grid(column=2, row=4, sticky='W')
        self.create_color_circle("outter", 4)

    def file_path(self):
        path = filedialog.askdirectory(title='Select Output Folder', initialdir=self.dir.get())
        if path:
            self.dir.set(path)
            if len(path) > 20:
                self.dir_path.config(text='...' + path[-16:])
            else:
                self.dir_path.config(text=path)

    def choose_color(self, color, row):
        hex_color = colorchooser.askcolor(title=f'Color for {color.capitalize()} squares')
        if not hex_color[1]:
            return
        self.colors[color].set(hex_color[1])
        self.create_color_circle(color, row)

    def create_color_circle(self, color, row):
        self.button_circles[color] = tk.Canvas(self, height=20, width=20)
        self.button_circles[color].create_oval(10, 10, 20, 20, fill=self.colors[color].get())
        self.button_circles[color].grid(column=0, row=row)

    def build_spreadsheet(self, e=None):
        uid = self.id_input.get()
        folder = self.dir.get()
        colors = (self.colors['empty'].get(), self.colors['occupied'].get(), self.colors['outter'].get())
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
        mapper.make_spreadsheet(sector['name'], shape, systems, folder, colors)

        messagebox.showinfo(title='Sector Map Created',
                            message=f'The Spreadsheet for Sector {sector["name"]} has been created')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
