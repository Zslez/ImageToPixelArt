from tkinter import Tk
from tkinter import Menu
from tkinter import Label
from tkinter import DoubleVar

from tkinter import ttk
from tkinter import font
from tkinter import filedialog

from PIL import Image, ImageTk

import os

# test cmd: cls && py -m cProfile -s tottime main.py

file_ext = [
    '.avci', '.avcs', '.avif', '.avifs', '.bmp', '.cr2',
    '.eps', '.gif', '.heic', '.heics', '.heif', '.heifs',
    '.jpeg', '.jpg', '.nef', '.orf', '.pbm', '.pgm', '.png',
    '.pnm', '.ppm', '.raw', '.sr2', '.tif', '.tiff', '.webp'
]


class ImageToPixelArt:
    ext = None
    img = None
    size = None
    max_l = None
    small = None
    resized = None
    displayed = None

    num = 512
    max_a = 85

    border_color = (0, 0, 0)
    mode = 0
    colormenu = None

    slider_text = None
    border_text = None

    old_slider_value = (None, None)

    border_c = None

    folder = []
    file_index = 0

    last_element = lambda _, x: x[-1]

    denom = (255 ** 4) * 100


    def __init__(self):
        window = Tk()

        window.title('ImageToPixelArt')
        window.resizable(False, False)

        default_font = font.Font(window, ('pix PixelFJVerdana12pt', 6))

        call = window.tk.call

        call('source', 'sun-valley.tcl')
        call('set_theme', 'light')

        ## ===================== MENU ===================== ##

        # FILE HANDLERS

        menubar = Menu(window)

        filemenu = Menu(menubar, tearoff = 0)

        filemenu.add_command(label = 'Open', command = self.open_file)
        filemenu.add_command(label = 'Save Big', command = self.file_save_big)
        filemenu.add_command(label = 'Save Small', command = self.file_save_small)
        filemenu.add_command(label = 'Close', command = self.close_file)

        self.filemenu = filemenu

        menubar.add_cascade(label = 'File', menu = filemenu)

        # SETTINGS

        setmenu = Menu(menubar, tearoff = 0)
        display = Menu(setmenu, tearoff = 0)

        display.add_command(label = '1',        command = lambda: self.change_num(0))
        display.add_command(label = '2',        command = lambda: self.change_num(1))
        display.add_command(label = '3',        command = lambda: self.change_num(2))
        display.add_command(label = '4',        command = lambda: self.change_num(3))

        setmenu.add_cascade(label = 'Image Size',       menu = display)

        # MODE

        modemenu = Menu(menubar, tearoff = 0)

        modemenu.add_command(label = 'Yes', command = lambda: self.change_mode(1))
        modemenu.add_command(label = 'No',  command = lambda: self.change_mode(0))

        # COLORS

        colormenu = Menu(menubar, tearoff = 0)

        colormenu.add_command(label = 'Black 1',        command = lambda: self.change_color(0))
        colormenu.add_command(label = 'Black 2',        command = lambda: self.change_color(1))
        colormenu.add_command(label = 'Grey 1',         command = lambda: self.change_color(2))
        colormenu.add_command(label = 'Grey 2',         command = lambda: self.change_color(3))
        colormenu.add_command(label = 'Grey 3',         command = lambda: self.change_color(4))
        colormenu.add_command(label = 'Brown 1',        command = lambda: self.change_color(5))
        colormenu.add_command(label = 'Brown 2',        command = lambda: self.change_color(6))
        colormenu.add_command(label = 'Brown 3',        command = lambda: self.change_color(7))
        colormenu.add_command(label = 'Dark Brown 1',   command = lambda: self.change_color(8))
        colormenu.add_command(label = 'Dark Brown 2',   command = lambda: self.change_color(9))

        self.colormenu = colormenu

        # PLACE COMMANDS

        setmenu.add_cascade(label = 'Borders',          menu = modemenu)
        setmenu.add_cascade(label = 'Border Color',     menu = colormenu)
        menubar.add_cascade(label = 'Settings',         menu = setmenu)

        menubar.add_command(label = 'Theme', command = lambda: call('set_theme',
            ['dark', 'light'][call("ttk::style", "theme", "use") == "sun-valley-dark"]))
        menubar.add_command(label = '?', command = lambda: '')

        menubar.entryconfig('Settings',     state = 'disabled')
        setmenu.entryconfig('Border Color', state = 'disabled')

        self.setmenu = setmenu

        filemenu.entryconfig('Save Big',    state = 'disabled')
        filemenu.entryconfig('Save Small',  state = 'disabled')
        filemenu.entryconfig('Close',       state = 'disabled')

        self.menubar = menubar

        ## ==================== CONFIG ==================== ##

        window.option_add('*Font', default_font)

        window.config(menu = self.menubar)

        # displayed image

        self.displayed = Label(window)
        self.displayed.pack()

        # text label displaying image size

        self.size = Label(window)
        self.size.pack()

        # sliders

        self.border_c = DoubleVar()
        self.border_slid = ttk.Scale(window, from_ = 0, to = self.max_a,
            length = self.num, orient = 'horizontal', variable = self.border_c)
        self.border_slid.pack(side = 'bottom')
        self.border_slid['state'] = 'disabled'

        self.border_text = Label(window, text = 'Border')
        self.border_text.pack(side = 'bottom')

        self.slider = ttk.Scale(window, from_ = 0, to = 100, length = self.num, orient = 'horizontal')
        self.slider.pack(side = 'bottom')
        self.slider['state'] = 'disabled'

        self.slider_text = Label(window, text = 'Scale')
        self.slider_text.pack(side = 'bottom')

        window.geometry(str(self.num) + 'x' + str(self.num + 120))

        self.window = window


    # FILE COMMANDS

    def load_image(self, i):
        path = self.folder[i]

        self.img = Image.open(path)

        imgtk = ImageTk.PhotoImage(self.img)

        self.displayed.configure(image = imgtk)
        self.displayed.image = imgtk

        self.size.configure(text = str(self.img.size[0]) + 'x' + str(self.img.size[1]))
        self.size.text = str(self.img.size[0]) + 'x' + str(self.img.size[1])

        # get the widest between image width and height
        # and resize the image to make it fit the screen

        self.max_l = max(self.img.size)
        self.resized = self.img.resize(
            (self.num * self.img.size[0] // self.max_l, self.num * self.img.size[1] // self.max_l),
            0
        )

        # display the image

        imgtk = ImageTk.PhotoImage(self.img)

        self.displayed.configure(image = imgtk)
        self.displayed.image = imgtk

        # set the text label

        self.size.configure(text = str(self.img.size[0]) + 'x' + str(self.img.size[1]))
        self.size.text = str(self.img.size[0]) + 'x' + str(self.img.size[1])

        self.slider.set(0)
        self.ext = path.split('.')[-1]
        self.old_slider_value = (None, None)

        self.window.title('ImageToPixelArt - ' + path.replace('\\', '/').split('/')[-1])


    def open_file(self):
        '''ask for file to open and loads the image'''

        path = filedialog.askopenfilename(filetypes = [('Image File', file_ext)])

        try:
            self.img = Image.open(path)
        except AttributeError: # if the user closes the window without selecting any file
            return

        # get the widest between image width and height
        # and resize the image to make it fit the screen

        self.max_l = max(self.img.size)
        self.resized = self.img.resize(
            (self.num * self.img.size[0] // self.max_l, self.num * self.img.size[1] // self.max_l),
            0
        )

        # display the image

        imgtk = ImageTk.PhotoImage(self.img)

        self.displayed.configure(image = imgtk)
        self.displayed.image = imgtk

        # set the text label

        self.size.configure(text = str(self.img.size[0]) + 'x' + str(self.img.size[1]))
        self.size.text = str(self.img.size[0]) + 'x' + str(self.img.size[1])

        # activate slider and set it to 0

        self.slider['state'] = 'normal'
        self.slider.set(0)
        self.old_slider_value = (None, None)

        # save the opened file extention, to use it as the default when saving the result

        self.ext = path.split('.')[-1]

        # activate options

        self.menubar.entryconfig('Settings',        state = 'normal')

        self.filemenu.entryconfig('Save Big',       state = 'normal')
        self.filemenu.entryconfig('Save Small',     state = 'normal')
        self.filemenu.entryconfig('Close',          state = 'normal')

        # set new title

        *self.folder, filename = path.replace('\\', '/').split('/')
        self.folder = '/'.join(self.folder)
        self.folder = [
            self.folder + '/' + i for i in os.listdir(self.folder)
            if '.' + i.split('.')[-1] in file_ext
        ]
        self.file_index = self.folder.index(path)
        self.window.title('ImageToPixelArt - ' + filename)


    def file_save_big(self):
        '''saves the displayed image with the original one's size'''

        if self.img:
            # ask to save file

            path = filedialog.asksaveasfile(
                mode = 'w',
                filetypes = [('Image File', file_ext)], defaultextension = self.ext
            )

            try:
                # resize the pixeled image to the original image's size and save it

                self.small.resize(self.img.size, 0).save(path.name)
                path.close()
            except AttributeError:
                pass


    def file_save_small(self):
        '''saves the displayed image with the displayed size'''

        if self.img:
            # ask to save file

            path = filedialog.asksaveasfile(
                mode = 'w',
                filetypes = [('Image File', file_ext)], defaultextension = self.ext
            )

            try:
                # save the small image

                self.small.save(path.name)
                path.close()
            except AttributeError:
                pass


    def close_file(self):
        '''set all variables back to default and block commands in menubar'''

        if self.img:
            self.img = None

            self.displayed.configure(image = None)
            self.displayed.image = None

            self.size.configure(text = None)
            self.size.text = None

            self.slider.set(0)
            self.slider['state'] = 'disabled'

            self.old_slider_value = (None, None)

            self.border_slid.set(0)
            self.border_slid['state'] = 'disabled'

            self.menubar.entryconfig('Settings',        state = 'disabled')
            self.setmenu.entryconfig('Border Color',    state = 'disabled')

            self.filemenu.entryconfig('Save Big',       state = 'disabled')
            self.filemenu.entryconfig('Save Small',     state = 'disabled')
            self.filemenu.entryconfig('Close',          state = 'disabled')

            self.folder = []
            self.file_index = 0

            self.window.title('ImageToPixelArt')


    # OTHER MENU COMMANDS

    def change_num(self, new_num):
        '''change displayed image and window's size'''

        self.num = [128, 256, 384, 512][new_num]
        self.old_slider_value = (None, None)


    def change_mode(self, mode):
        '''set the selected one between 'no borders' and 'yes borders\''''

        self.mode = [0, 1][mode]
        self.old_slider_value = (None, None)

        if mode == 0:
            self.setmenu.entryconfig('Border Color', state = 'disabled')
            self.border_slid['state'] = 'disabled'
        else:
            self.setmenu.entryconfig('Border Color', state = 'normal')
            self.border_slid['state'] = 'normal'

    def change_color(self, color):
        '''set new border color'''

        self.border_color = [
            (  0,   0,   0),
            ( 10,  10,  10),

            ( 30,  30,  30),
            ( 50,  50,  50),
            ( 70,  70,  70),

            (160,  82,  45),
            (150,  75,   0),
            (139,  69,  19),

            (100,  67,  33),
            ( 80,  60,  30)
        ][color]

        self.old_slider_value = (None, None)


    # KEYPRESSES

    def get_keypress(self, key):
        if len(self.folder) != 0:
            if key.keycode == 37:
                if self.file_index:
                    self.file_index -= 1
                    self.load_image(self.file_index)
            elif key.keycode == 39:
                if self.file_index < len(self.folder) - 1:
                    self.file_index += 1
                    self.load_image(self.file_index)


    def display_image(self):
        # resize small image to make it fit the screen

        width, height = self.img.size

        res = self.small.resize((self.num * width // self.max_l, self.num * height // self.max_l), 0)
        tkimg = ImageTk.PhotoImage(res)

        # change text label

        txt = str(self.small.size[0]) + 'x' + str(self.small.size[1])
        self.size.configure(text = txt)
        self.size.text = txt

        # display resized image

        self.displayed.configure(image = tkimg)
        self.displayed.image = tkimg

    # MAIN FUNCTION

    def update_image(self):
        '''updates the displayed image based on the sliders' values'''

        # if there's not image loaded, skips the loop and retry after 10 ms

        slid, b_slid = self.slider.get(), self.border_slid.get()

        if self.img and (slid, b_slid) != self.old_slider_value:
            self.old_slider_value = slid, b_slid
            size = self.img.size
            val = slid * (self.max_l // 2 + 1) // 100
            width1, height1 = size

            # if the slider value is 0, simply display the same image

            if not val:
                res = self.img.resize((self.num * width1 // self.max_l, self.num * height1 // self.max_l), 0)

                txt = str(width1) + 'x' + str(height1)
                self.size.configure(text = txt)
                self.size.text = txt

                tkimg = ImageTk.PhotoImage(res)

                self.displayed.configure(image = tkimg)
                self.displayed.image = tkimg

                self.window.after(10, self.update_image)
                return

            # scale down image by the selected value

            val = 1.0 / val
            self.small = self.img.resize((max(int(width1 * val), 1), max(int(height1 * val), 1)))

            if not self.mode:
                self.display_image()
                self.window.after(10, self.update_image)
                return

            pix = self.small.load()
            width, height = self.small.size

            # if pixels have the alpha channel replace the most transparest ones with the border

            if (not isinstance(pix[0, 0], tuple)) or len(tuple(pix[0, 0])) != 4:
                self.display_image()
                self.window.after(10, self.update_image)
                return

            # get the highest alpha value of the image

            max_alpha = sorted(self.small.split()[-1].getdata())[-1]

            # get the highest and the lowest value that gets replaced

            max_alpha_2 = max_alpha ** 5
            max_alpha_3 = b_slid * max_alpha_2 // (self.denom)
            max_alpha_2 = self.max_a * max_alpha_2 // (self.denom)
            bor_c = self.border_color
            transparent = (0, 0, 0, 0)

            # replace

            # this part can be really slow if the image is big :(
            # it loops through all pixels and checks their alpha value

            for i in range(width * height):
                index = i % width, i // width
                pixel = pix[index][-1]

                if pixel == 0:
                    continue
                elif pixel <= max_alpha_3:
                    pix[index] = transparent
                elif max_alpha_3 < pixel < max_alpha_2:
                    pix[index] = bor_c + (max_alpha,)

            self.display_image()

        self.window.after(10, self.update_image)


    def run(self):
        '''run the GUI'''

        self.window.after(100, self.update_image)
        self.window.bind('<Key>', self.get_keypress)
        self.window.mainloop()


if __name__ == '__main__':
    itpa = ImageToPixelArt()
    itpa.run()
