# coding:utf-8

import logging

from PIL import ImageTk, Image
from Tkinter import Tk, BOTH, Menu, Label
from ttk import Frame, Button, Style
import tkFileDialog
import tkSimpleDialog

from image_processor import create_images


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

        self.img_labels = [None] * 2
        self.img_file_names = [None] * 2

    def initUI(self):
        # self.parent.title("Comparação de imagens")
        self.style = Style()
        self.style.configure('TFrame', background='#333')

        self.pack(fill=BOTH, expand=1)

        menu_bar = Menu(self.parent)
        self.parent.config(menu=menu_bar)

        size = self.parent.size

        select_image_btn = Button(self, text='Selecionar Imagem', command=self.select_image_file)
        select_image_btn.place(x=10, y=10)

        quit_button = Button(self, text='Sair', command=self.quit)
        quit_button.place(x=size[0] - 100, y=size[1] - 50)

    def text_dialog_box(self, box_title, msg):
        return tkSimpleDialog.askstring(box_title, msg)

    # def select_image_1(self):
    #     logging.debug('Selecionando a primeira imagem.')
    #     self.select_image_file(0)

    # def select_image_2(self):
    #     self.select_image_file(1)

    def load_image(self, file_name, position):
        image = Image.open(file_name)
        image = ImageTk.PhotoImage(image)
        label = Label(self, image=image)
        label.image = image
        label.place(x=position[0], y=position[1])

    def select_image_file(self):
        file_types = [('PNG Image', '*.png'), ('Todos arquivos', '*')]
        dialog_box = tkFileDialog.Open(self, filetypes=file_types)

        file_name = dialog_box.show()
        self.file_name = file_name

        msg = 'Qual a largura desejada (em pixels) da imagem?\nO menor valor aceito é 20, e o maior, 200'
        image_width = self.text_dialog_box('Largura da imagem', msg)
        msg = 'Qual a altura desejada (em pixels) da imagem?\nO menor valor aceito é 20, e o maior, 150'
        image_height = self.text_dialog_box('Altura da imagem', msg)
        image_size = (int(image_width), int(image_height))

        if file_name is not None:
            logging.debug('Imagem selecionada: ' + file_name)

            file_name_1, file_name_2 = create_images(file_name, image_size)

            self.load_image(file_name_1, (10, 50))

            x_position = self.parent.size[0] / 2
            self.load_image(file_name_2, (x_position, 50))
        else:
            logging.debug('Nenhum arquivo de imagem foi selecionado')


class RootWindow(Tk):

    def __init__(self, size=(800, 600)):
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
