# coding:utf-8

import logging

from PIL import ImageTk, Image
import Tkinter
from Tkinter import Tk, BOTH, Menu, Label, Canvas
from ttk import Frame, Button, Style
import tkFileDialog
import tkSimpleDialog

from image_processor import create_images


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

        self.img_labels = [Label(self), Label(self)]

    def initUI(self):
        self.bg_color = '#333'

        # self.parent.title("Comparação de imagens")
        self.style = Style()
        self.style.configure('TFrame', background=self.bg_color)

        self.pack(fill=BOTH, expand=1)

        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)

        size = self.parent.size

        select_image_btn = Button(self, text='Selecionar Imagem', command=self.select_image_file)
        select_image_btn.place(x=10, y=10)

        quit_button = Button(self, text='Sair', command=self.quit)
        quit_button.place(x=size[0] - 100, y=size[1] - 50)

        self.canvas = Canvas(self, bg=self.bg_color, bd=10)
        self.canvas.pack()
        self.canvas.place(x=0, y=600, height=200, width=650)

    def text_dialog_box(self, box_title, msg):
        return tkSimpleDialog.askstring(box_title, msg)

    def draw_result(self, results):
        self.canvas.grid_forget()
        self.canvas = Canvas(self, bg=self.bg_color, bd=10)
        self.canvas.pack()

        self.canvas.place(x=0, y=600, height=200, width=650)

        font = ('Helvetica', '12')
        self.canvas.create_text(20, 40, anchor=Tkinter.W, font=font, text='Probability of being the same image according different algorithms:', fill='white')
        self.canvas.create_text(20, 65, anchor=Tkinter.W, font=font, text=results[0], fill='white')
        self.canvas.create_text(20, 90, anchor=Tkinter.W, font=font, text=results[1], fill='white')
        self.canvas.create_text(20, 115, anchor=Tkinter.W, font=font, text=results[2], fill='white')

    def load_image(self, file_name, position, label):
        image = Image.open(file_name)
        image = ImageTk.PhotoImage(image)
        label.__setitem__('image', image)
        label.image = image
        label.place(x=position[0], y=position[1])


    def select_image_file(self):
        file_types = [('PNG Image', '*.png'), ('Todos arquivos', '*')]
        dialog_box = tkFileDialog.Open(self, filetypes=file_types)

        file_name = dialog_box.show()
        self.file_name = file_name

        msg = 'Qual a largura desejada (em pixels) da imagem?\nO menor valor aceito é 20, e o maior, 200'
        image_width = self.text_dialog_box('Largura da imagem', msg)
        while not image_width.isdigit() or int(image_width) < 20 or int(image_width) > 200:
            msg = 'Valor Inválido! Os valores aceitos para largura (em pixels) vão de 20 a 200\nEntre com novo valor:'
            image_width = self.text_dialog_box('Largura da imagem', msg)
        msg = 'Qual a altura desejada (em pixels) da imagem?\nO menor valor aceito é 20, e o maior, 150'
        image_height = self.text_dialog_box('Altura da imagem', msg)
        while not image_height.isdigit() or int(image_height) < 20 or int(image_height) > 150:
            msg = 'Valor Inválido! Os valores aceitos para altura (em pixels) vão de 20 a 150\nEntre com novo valor:'
            image_height = self.text_dialog_box('Altura da imagem', msg)
        image_size = (int(image_width), int(image_height))

        if file_name is not None:
            logging.debug('Imagem selecionada: ' + file_name)

            file_names, results = create_images(file_name, image_size)

            self.load_image(file_names[0], (10, 50), self.img_labels[0])

            x_position = self.parent.size[0] / 2 - 200
            self.load_image(file_names[1], (x_position, 50), self.img_labels[1])

            print results
            self.draw_result(results)
        else:
            logging.debug('Nenhum arquivo de imagem foi selecionado')


class RootWindow(Tk):

    def __init__(self, size=(1000, 800)):
        Tk.__init__(self)

        self.title("Comparação de Imagens")

        self.size = size
        self.center_window()
        self.frame = Example(self)
        self.mainloop()

    def center_window(self):
        screen_size = (self.winfo_screenwidth(), self.winfo_screenheight())
        x_position = (screen_size[0] - self.size[0]) / 2
        y_position = (screen_size[1] - self.size[1]) / 2

        geometry_arg = '{}x{}+{}+{}'.format(self.size[0], self.size[1], x_position, y_position)
        self.geometry(geometry_arg)


def main():
    RootWindow()


if __name__ == '__main__':
    print ''
    logging.basicConfig(level=logging.DEBUG)
    main()
