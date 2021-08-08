from tkinter import *
import tkinter.colorchooser
from PIL import ImageGrab


class PixelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art")

        # dimensions
        self.cell_length = 15
        self.grid_length = 30
        self.grid_height = 15

        # variables
        self.color_chooser = tkinter.colorchooser.Chooser(self.root)
        self.chosen_color = None
        self.is_pencil_selected = False
        self.is_eraser_selected = False

        # background of drawing grid
        self.drawing_grid = Canvas(self.root)
        self.drawing_grid.grid(column=0, row=0, sticky=(N, E, S, W))

        # one cell
        self.cells = []
        for i in range(0, self.grid_height):
            for j in range(0, self.grid_length):
                cell = Frame(self.drawing_grid, width=self.cell_length, height=self.cell_length, background="white",
                             highlightbackground="black", highlightcolor="black", highlightthickness=0.5)
                # when left mouse button pressed
                cell.grid(column=j, row=i)
                cell.bind('<Button-1>', self.tap_cell)
                self.cells.append(cell)

        # control panel
        control_panel = Frame(self.root, height=50)
        control_panel.grid(column=0, row=1, sticky=(N, E, S, W))

        # new button
        new_button = Button(control_panel, text="New",
                            command=self.press_new_button)
        new_button.grid(column=0, row=0, columnspan=5,
                        sticky=(N, E, S, W), padx=5, pady=5)

        # save button
        save_button = Button(control_panel, text="Save",
                             command=self.press_save_button)
        save_button.grid(column=round(self.grid_length*0.1),
                         row=0, columnspan=5, sticky=(N, E, S, W), padx=5, pady=5)

        # pencil button
        self.pencil_image = PhotoImage(file="pencil.png").subsample(3, 4)
        pencil_button = Button(control_panel, text="Pencil", image=self.pencil_image,
                               command=self.press_pencil_button)
        pencil_button.grid(column=round(self.grid_length*0.5-7),
                           row=0, columnspan=5, sticky=(N, E, S, W), padx=5, pady=5)

        # erase button
        self.erase_image = PhotoImage(file="eraser.png").subsample(3, 4)
        erase_button = Button(control_panel, text="Erase", image=self.erase_image,
                              command=self.press_erase_button)
        erase_button.grid(column=round(self.grid_length*0.5+2),
                          row=0, columnspan=5, sticky=(N, E, S, W), padx=5, pady=5)

        # select color box
        self.selected_color_box = Frame(
            control_panel, borderwidth=2, relief="raised", bg="white")
        self.selected_color_box.grid(column=round(
            self.grid_length*0.9-5), row=0, sticky=(N, E, S, W), columnspan=5, padx=5, pady=5)

        # pick color button
        pick_color_button = Button(
            control_panel, text="Pick color", command=self.press_pick_color_button)
        pick_color_button.grid(column=round(
            self.grid_length-5), row=0, columnspan=5, sticky=(N, E, S, W), padx=5, pady=5)

        cols, rows = control_panel.grid_size()
        for col in range(cols):
            control_panel.columnconfigure(col, minsize=self.cell_length)
        control_panel.rowconfigure(0, minsize=self.cell_length)

    def tap_cell(self, event):
        index = self.cells.index(event.widget)  # which cells selected?
        selected_cell = self.cells[index]
        if self.is_eraser_selected:
            selected_cell["bg"] = "white"
        if self.is_pencil_selected and self.chosen_color != None:
            selected_cell["bg"] = self.chosen_color

    def press_new_button(self):
        for cell in self.cells:
            cell["bg"] = "white"
        self.selected_color_box = "white"
        self.chosen_color = None
        self.is_pencil_selected = False
        self.is_eraser_selected = False

    def press_save_button(self):
        x = root.winfo_ + self.drawing_grid.winfo_x() + 35
        y = root.winfo_y() + self.drawing_grid.winfo_y() + 50
        width = x + self.cell_length*self.grid_length
        height = y + self.cell_length*self.grid_height
        ImageGrab.grab(bbox=(x, y, width, height)).save(
            "image.png")
        print(self.root.winfo_geometry)

    def press_pencil_button(self):
        self.is_pencil_selected = True
        self.is_eraser_selected = False

    def press_erase_button(self):
        self.is_eraser_selected = True
        self.is_pencil_selected = False

    def press_pick_color_button(self):
        color_info = self.color_chooser.show()
        # colour_info will either be ((r,g,b),hex) or (none, none)
        chosen = color_info[1]
        if chosen != None:
            self.chosen_color = chosen  # extract hex string
            self.selected_color_box["bg"] = self.chosen_color


root = Tk()
root.attributes('-fullscreen', True)
PixelApp(root)
root.mainloop()
