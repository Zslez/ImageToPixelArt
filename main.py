import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk


file_ext = [
    '.avci', '.avcs', '.avif', '.avifs', '.bmp', '.cr2', '.eps', '.gif', '.heic', '.heics', '.heif', '.heifs',
    '.jpeg', '.jpg', '.nef', '.orf', '.pbm', '.pgm', '.png', '.pnm', '.ppm', '.raw', '.sr2', '.tif', '.tiff', '.webp'
]


class ImageToPixelArt:
    m = None
    ext = None
    img = None
    size = None
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

    border_c = None

    folder = []
    file_index = 0


    def __init__(self):
        window = Tk()
        window = window

        window.title('ImageToPixelArt')
        window.resizable(False, False)

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

        #menubar.add_command(label = 'Theme', command = lambda: self.window.tk.call('set_theme',
        #   ['dark', 'light'][self.window.tk.call("ttk::style", "theme", "use") == "sun-valley-dark"]))
        menubar.add_command(label = '?', command = lambda: '')

        menubar.entryconfig('Settings',     state = 'disabled')
        setmenu.entryconfig('Border Color', state = 'disabled')

        self.setmenu = setmenu

        filemenu.entryconfig('Save Big',    state = 'disabled')
        filemenu.entryconfig('Save Small',  state = 'disabled')
        filemenu.entryconfig('Close',       state = 'disabled')

        self.menubar = menubar

        ## ==================== CONFIG ==================== ##

        window.config(menu = self.menubar)

        # displayed image

        self.displayed = ttk.Label(window)
        self.displayed.pack()

        # text label displaying image size

        self.size = ttk.Label(window)
        self.size.configure(font = ('pix PixelFJVerdana12pt', 6))
        self.size.pack()

        # sliders

        self.slider_text = ttk.Label(window, text = 'Scale')
        self.slider_text.configure(font = ('pix PixelFJVerdana12pt', 6))
        self.slider_text.place(x = self.num // 2 - 15, y = self.num + 30)

        self.slider = ttk.Scale(window, from_ = 0, to = 1000, length = self.num, orient = HORIZONTAL)
        self.slider.place(x = 0, y = self.num + 50)
        self.slider['state'] = 'disabled'

        self.border_text = ttk.Label(window, text = 'Border')
        self.border_text.configure(font = ('pix PixelFJVerdana12pt', 6))
        self.border_text.place(x = self.num // 2 - 20, y = self.num + 70)

        self.border_c = DoubleVar()
        self.border_slid = ttk.Scale(window, from_ = 0, to = self.max_a, length = self.num, orient = HORIZONTAL, variable = self.border_c)
        self.border_slid.place(x = 0, y = self.num + 90)
        self.border_slid['state'] = 'disabled'

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

        # get the widest between image width and height and resize the image to make it fit the screen

        self.m = max(self.img.size)
        self.resized = self.img.resize((self.num * self.img.size[0] // self.m, self.num * self.img.size[1] // self.m), 0)

        # display the image

        imgtk = ImageTk.PhotoImage(self.img)

        self.displayed.configure(image = imgtk)
        self.displayed.image = imgtk

        # set the text label

        self.size.configure(text = str(self.img.size[0]) + 'x' + str(self.img.size[1]))
        self.size.text = str(self.img.size[0]) + 'x' + str(self.img.size[1])

        self.slider.set(0)
        self.ext = path.split('.')[-1]

        self.window.title('ImageToPixelArt - ' + path.replace('\\', '/').split('/')[-1])


    def open_file(self):
        '''ask for file to open and loads the image'''

        path = filedialog.askopenfilename(filetypes = [('Image File', file_ext)])

        try:
            self.img = Image.open(path)
        except AttributeError: # if the user closes the window without selecting any file
            return

        # get the widest between image width and height and resize the image to make it fit the screen

        self.m = max(self.img.size)
        self.resized = self.img.resize((self.num * self.img.size[0] // self.m, self.num * self.img.size[1] // self.m), 0)

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
        self.folder = [self.folder + '/' + i for i in os.listdir(self.folder) if '.' + i.split('.')[-1] in file_ext]
        self.file_index = self.folder.index(path)
        self.window.title('ImageToPixelArt - ' + filename)


    def file_save_big(self):
        '''saves the displayed image with the original one's size'''

        if self.img:
            # ask to save file

            path = filedialog.asksaveasfile(mode = 'w', filetypes = [('Image File', file_ext)], defaultextension = self.ext)

            try:
                # resize the pixeled image to the original image's size and save it

                self.small.resize(self.img.size, 0).save(path.name)
                path.close
            except AttributeError:
                pass


    def file_save_small(self):
        '''saves the displayed image with the displayed size'''

        if self.img:
            # ask to save file

            path = filedialog.asksaveasfile(mode = 'w', filetypes = [('Image File', file_ext)], defaultextension = self.ext)

            try:
                # save the small image

                self.small.save(path.name)
                path.close
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

    def change_num(self, c):
        '''change displayed image and window's size'''

        self.num = [128, 256, 384, 512][c]


    def change_mode(self, mode):
        '''set the selected one between 'no borders' and 'yes borders\''''

        self.mode = [0, 1][mode]

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


    # KEYPRESSES

    def get_keypress(self, key: Event):
        if len(self.folder):
            if key.keycode == 37:
                if self.file_index:
                    self.file_index -= 1
                    self.load_image(self.file_index)
            elif key.keycode == 39:
                if self.file_index < len(self.folder) - 1:
                    self.file_index += 1
                    self.load_image(self.file_index)


    # MAIN FUNCTION

    def update_image(self):
        '''updates the displayed image based on the sliders' values'''

        # if there's not image loaded, skips the loop and retry after 10 ms

        if self.img:
            size = self.img.size
            val = self.slider.get() * (max(size) // 2 + 1) // 1000
            w1, h1 = size
            m = max(size)

            # if the slider value is 0, simply display the same image

            if not val:
                res = self.img.resize((self.num * w1 // m, self.num * h1 // m), 0)

                txt = str(w1) + 'x' + str(h1)
                self.size.configure(text = txt)
                self.size.text = txt

                tkimg = ImageTk.PhotoImage(res)

                self.displayed.configure(image = tkimg)
                self.displayed.image = tkimg

                self.window.after(10, self.update_image)
                return

            # scale down image by the selected value

            val = 1.0 / val
            self.small = self.img.resize((max(int(w1 * val), 1), max(int(h1 * val), 1)))

            if self.mode:
                pix = self.small.load()
                w, h = self.small.size

                # if pixels have the alpha channel replace the most transparest ones with the border

                if isinstance(pix[0, 0], tuple):
                    if len(pix[0, 0]) == 4:
                        # get the highest alpha value of the image

                        max_alpha = sorted(list(self.small.getdata()), key = lambda x: x[-1], reverse = True)[0][-1]

                        # get the highest and the lowest value that gets replaced

                        max_alpha_2 = max_alpha ** 5
                        max_alpha_3 = self.border_slid.get() * max_alpha_2 // ((255 ** 4) * 100)
                        max_alpha_2 = self.max_a * max_alpha_2 // ((255 ** 4) * 100)

                        # replace

                        for i in range(w * h):
                            x, y = i % w, i // w

                            if max_alpha_3 < pix[x, y][-1] < max_alpha_2:
                                pix[x, y] = self.border_color + (max_alpha, )
                            elif pix[x, y][-1] >= max_alpha_2:
                                pix[x, y] = pix[x, y][:-1]
                            else:
                                pix[x, y] = (0, 0, 0, 0)

            # resize small image to make it fit the screen

            res = self.small.resize((self.num * w1 // m, self.num * h1 // m), 0)
            tkimg = ImageTk.PhotoImage(res)

            # change text label

            txt = str(self.small.size[0]) + 'x' + str(self.small.size[1])
            self.size.configure(text = txt)
            self.size.text = txt

            # display resized image

            self.displayed.configure(image = tkimg)
            self.displayed.image = tkimg

        self.window.after(10, self.update_image)


    def run(self):
        '''run the GUI'''

        self.window.after(100, self.update_image)
        self.window.bind('<Key>', self.get_keypress)
        self.window.mainloop()


if __name__ == '__main__':
    itpa = ImageToPixelArt()
    itpa.run()