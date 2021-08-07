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
    num = 400
    size = None
    small = None
    resized = None
    displayed = None

    border_color = (0, 0, 0)
    mode = 0
    modemenu_var = None
    colormenu = None


    def __init__(self):
        window = Tk()
        self.window = window

        self.window.title('ImageToPixelArt')
        self.window.resizable(False, False)
        self.window.geometry(str(self.num) + 'x' + str(self.num + 50))

        self.window.tk.call('source', 'sun-valley.tcl')
        self.window.tk.call('set_theme', 'light')

        ## ===================== MENU ===================== ##

        # FILE HANDLERS

        menubar = Menu(self.window)

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

        setmenu.add_cascade(label = 'Image Size',    menu = display)
        menubar.add_cascade(label = 'Settings',         menu = setmenu)

        # MODE

        self.modemenu_var = [DoubleVar(), DoubleVar()]

        modemenu = Menu(menubar, tearoff = 0)

        modemenu.add_checkbutton(label = 'Yes', command = lambda: self.change_mode(1), variable = self.modemenu_var[1])
        modemenu.add_checkbutton(label = 'No',  command = lambda: self.change_mode(0), variable = self.modemenu_var[0])

        menubar.add_cascade(label = 'Borders', menu = modemenu)

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

        menubar.add_cascade(label = 'Border Color', menu = colormenu)

        menubar.add_command(label = 'Theme', command = lambda: self.window.tk.call('set_theme',
            ['dark', 'light'][self.window.tk.call("ttk::style", "theme", "use") == "sun-valley-dark"]))
        menubar.add_command(label = '?', command = lambda: '')

        menubar.entryconfig('Settings',     state = 'disabled')
        menubar.entryconfig('Borders',      state = 'disabled')
        menubar.entryconfig('Border Color', state = 'disabled')

        filemenu.entryconfig('Save Big',    state = 'disabled')
        filemenu.entryconfig('Save Small',  state = 'disabled')
        filemenu.entryconfig('Close',       state = 'disabled')

        self.menubar = menubar

        ## ==================== CONFIG ==================== ##

        self.window.config(menu = self.menubar)

        self.displayed = Label(self.window)
        self.displayed.pack()

        self.size = Label(self.window)
        self.size.pack()

        self.slider = ttk.Scale(self.window, from_ = 0, to = 1000, length = self.num, orient = HORIZONTAL)
        self.slider.pack(side = 'bottom')
        self.slider['state'] = 'disabled'



    def open_file(self):
        path = filedialog.askopenfilename(filetypes = [('Image File', file_ext)])

        try:
            self.img = Image.open(path)
        except:
            return

        self.m = max(self.img.size)
        self.resized = self.img.resize((self.num * self.img.size[0] // self.m, self.num * self.img.size[1] // self.m), 0)

        imgtk = ImageTk.PhotoImage(self.img)

        self.displayed.configure(image = imgtk)
        self.displayed.image = imgtk

        self.size.configure(text = str(self.img.size[0]) + 'x' + str(self.img.size[1]))
        self.size.text = str(self.img.size[0]) + 'x' + str(self.img.size[1])

        self.slider['state'] = 'normal'
        self.slider['length'] = self.resized.size[0]
        self.slider.set(0)

        self.ext = path.split('.')[-1]

        self.menubar.entryconfig('Borders',         state = 'normal')
        self.menubar.entryconfig('Settings',        state = 'normal')

        self.filemenu.entryconfig('Save Big',       state = 'normal')
        self.filemenu.entryconfig('Save Small',     state = 'normal')
        self.filemenu.entryconfig('Close',          state = 'normal')

        self.window.title('ImageToPixelArt - ' + path.replace('\\', '/').split('/')[-1])


    def file_save_big(self):
        if self.img:
            name = filedialog.asksaveasfile(mode = 'w', filetypes = [('Image File', file_ext)], defaultextension = self.ext)

            try:
                self.small.resize(self.img.size, 0).save(name.name)
            except:
                pass

            name.close


    def file_save_small(self):
        if self.img:
            name = filedialog.asksaveasfile(mode = 'w', filetypes = [('Image File', file_ext)], defaultextension = self.ext)

            try:
                self.small.save(name.name)
            except:
                pass

            name.close


    def close_file(self):
        if self.img:
            self.img = None

            self.displayed.configure(image = None)
            self.displayed.image = None

            self.size.configure(text = '')
            self.size.text = ''

            self.slider.set(0)
            self.slider['state'] = 'disabled'
            self.slider['length'] = self.window.winfo_width()

            self.menubar.entryconfig('Settings',        state = 'disabled')
            self.menubar.entryconfig('Borders',         state = 'disabled')
            self.menubar.entryconfig('Border Color',    state = 'disabled')

            self.filemenu.entryconfig('Save Big',       state = 'disabled')
            self.filemenu.entryconfig('Save Small',     state = 'disabled')
            self.filemenu.entryconfig('Close',          state = 'disabled')

            self.window.title('ImageToPixelArt')


    def change_num(self, c):
        self.num = [200, 400, 600, 800][c]
        self.window.geometry(str(self.num) + 'x' + str(self.num + 50))
        self.slider['length'] = self.num
    

    def change_mode(self, mode):
        self.modemenu_var[mode].set(1.0)
        self.modemenu_var[1 - mode].set(0.0)
        self.mode = mode

        if mode == 0:
            self.menubar.entryconfig('Border Color', state = 'disabled')
        else:
            self.menubar.entryconfig('Border Color', state = 'normal')
    
    def change_color(self, color):
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


    def update_image(self):
        if self.img:
            size = self.img.size
            val = self.slider.get() * (max(size) // 2 + 1) // 1000
            w1, h1 = size
            m = max(size)

            if not val:
                res = self.img.resize((self.num * size[0] // m, self.num * size[1] // m), 0)

                txt = str(size[0]) + 'x' + str(size[1])
                self.size.configure(text = txt)
                self.size.text = txt

                tkimg = ImageTk.PhotoImage(res)

                self.displayed.configure(image = tkimg)
                self.displayed.image = tkimg

                self.window.after(10, self.update_image)
                return

            val = 1 / val
            self.small = self.img.resize((max(int(w1 * val), 1), max(int(h1 * val), 1)))

            if self.mode:
                pix = self.small.load()
                w, h = self.small.size
                max_alpha = sorted(list(self.small.getdata()), key = lambda x: x[-1], reverse = True)[0][-1]
                max_alpha_2 = 85 * (max_alpha ** 5) // ((255 ** 4) * 100)

                if isinstance(pix[0, 0], tuple):
                    if len(pix[0, 0]) == 4:
                        for i in range(w * h):
                            x, y = i % w, i // w

                            if 0 < pix[x, y][-1] < max_alpha_2:
                                pix[x, y] = self.border_color + (max_alpha, )

            res = self.small.resize((self.num * size[0] // m, self.num * size[1] // m), 0)
            tkimg = ImageTk.PhotoImage(res)

            txt = str(self.small.size[0]) + 'x' + str(self.small.size[1])
            self.size.configure(text = txt)
            self.size.text = txt

            self.displayed.configure(image = tkimg)
            self.displayed.image = tkimg

        self.window.after(10, self.update_image)

    def run(self):
        self.window.after(100, self.update_image)
        self.window.mainloop()


if __name__ == '__main__':
    a = ImageToPixelArt()
    a.run()