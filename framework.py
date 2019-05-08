# coding: utf-8
import argparse
import math
import time
import random
from tkinter import *
from PIL import Image, ImageTk
from mandelbrot import Mandelbrot
import opt


class Framework(Frame):
    def __init__(self, parent, h, x=-0.75, y=0, m=1, iterations=None, img_width=None,
                 img_height=None, save=False, color_palette=False, spec_set='J'):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Mandelbrot && Julia")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.palette = None
        self.color_palette = color_palette
        self.background = None
        if None in {img_width, img_height}:
            img_width, img_height = int(h*1.6), h
        if img_width > img_height:
            ratio = img_height/img_width
            self.canvasW, self.canvasH = h, round(h*ratio)
        else:
            ratio = img_width/img_height
            self.canvasW, self.canvasH = round(h*ratio), h

        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations,
                                  w=img_width, h=img_height, color_palette=color_palette, spec_set=spec_set)
        self.set_palette()
        self.img = None
        self.save = save
        self.draw(color_palette)

        # fix the issue: clicking on window's title bar will generate event
        self.canvas.bind("<Control-1>", self.zoom_in)
        self.canvas.bind("<Control-2>", self.zoom_out)
        self.canvas.bind("<B1-Motion>", self.shift_view)
        self.canvas.bind("<Button-1>", self.change_palette)
        self.canvas.bind("<Button-2>", self.save_image)
        self.canvas.bind("<Motion>", self.mouse_pos)

    def mouse_pos(self, event):
        # print("鼠标状态：", event.type)
        # print("鼠标位置：", event.x, event.y)
        pass

    def zoom_in(self, event):
        print('Tip: zoom_in')
        self.fractal.zoom_in(event)
        self.draw(self.color_palette)

    def zoom_out(self, event):
        print('Tip: zoom_out')
        self.fractal.zoom_out(event)
        self.draw(self.color_palette)

    def shift_view(self, event):
        print('Tip: shift_view')
        self.fractal.shift_view(event)
        self.draw()

    def change_palette(self, event):
        if self.color_palette:
            print('change_palette')
            self.set_palette()
            self.draw_pixels()
            self.canvas.create_image(0, 0, image=self.background, anchor=NW)
            self.canvas.pack(fill=BOTH, expand=1)

    def save_image(self, event):
        print('Tip: save_image')
        self.img.save("pictures/{}.png".format(time.strftime("%Y-%m-%d-%H:%M:%S")), "PNG", optimize=True)

    def draw(self, color_flag=False):
        """
        绘制图片主功能
        :return:
        """
        print('-' * 60)
        start = time.time()

        if color_flag is True:
            self.fractal.get_color_pixels(color_flag)
            print("get_color_pixels {} 秒".format(round(time.time() - start, 2)))
            start = time.time()
            self.draw_pixels()
            print("draw_pixels执行时间 {} 秒".format(round(time.time() - start, 2)))
            start = time.time()
            self.canvas.create_image(0, 0, image=self.background, anchor=NW)
            self.canvas.pack(fill=BOTH, expand=1)
        else:
            self.img = self.fractal.get_color_pixels(color_flag)
            self.background = ImageTk.PhotoImage(self.img.resize((self.canvasW, self.canvasH)))
            self.canvas.create_image(0, 0, image=self.background, anchor=NW)
            self.canvas.pack(fill=BOTH, expand=1)

        print("create_image执行时间 {} 秒".format(round(time.time()-start, 2)))

    def set_palette(self):
        """
        返回256个颜色值的数组列表
        :return:
        """
        if self.color_palette:
            print('Color palette used!')
            self.palette = [(0, 0, 0)]
            red_b = 2 * math.pi / (random.randint(0, 128) + 128)
            red_c = 256 * random.random()
            green_b = 2 * math.pi / (random.randint(0, 128) + 128)
            green_c = 256 * random.random()
            blue_b = 2 * math.pi / (random.randint(0, 128) + 128)
            blue_c = 256 * random.random()
            for i in range(256):
                r = clamp(int(256 * (0.5 * math.sin(red_b * i + red_c) + 0.5)))
                g = clamp(int(256 * (0.5 * math.sin(green_b * i + green_c) + 0.5)))
                b = clamp(int(256 * (0.5 * math.sin(blue_b * i + blue_c) + 0.5)))
                self.palette.append((r, g, b))
        else:
            print('Color palette not used!')

    def draw_pixels(self):
        """
        生成图片
        :return:
        """
        self.img = Image.new('RGB', (self.fractal.w, self.fractal.h), "black")
        pixels = self.img.load()  # create the pixel map

        opt.get_colors(pixels, self.fractal.pixels, self.palette)
        # for index, p in enumerate(self.fractal.pixels):
        #     pixels[int(p[0]), int(p[1])] = self.palette[p[2] % 256]
        #
        if self.save:
            self.save_image(None)
        photo_img = ImageTk.PhotoImage(self.img.resize((self.canvasW, self.canvasH)))
        self.background = photo_img


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = round(master.winfo_screenheight())
    parser = argparse.ArgumentParser(description='Generate the Mandelbrot set')
    parser.add_argument('-i', '--iterations', type=int, help='The number of iterations done for each pixel. '
                                                             'Higher is more accurate but slower.')
    parser.add_argument('-x', type=float, help='The x-center coordinate of the frame.')
    parser.add_argument('-y', type=float, help='The y-center coordinate of the frame.')
    parser.add_argument('-m', '--magnification', type=float, help='The magnification level of the frame.')
    parser.add_argument('-wi', '--width', type=int, help='The width of the image.')
    parser.add_argument('-he', '--height', type=int, help='The width of the image.')
    parser.add_argument('-s', '--save', action='store_true', help='Save the generated image.')
    parser.add_argument('-c', '--color_palette', action='store_false', help="if color palette is used.")
    parser.add_argument('-spec_set', type=str, help='J for Julia, M for mandelbrot. default is M')
    args = parser.parse_args()
    if None not in [args.x, args.y, args.magnification]:
        render = Framework(master, height, x=args.x, y=args.y, m=args.magnification, color_palette=args.color_palette,
                           iterations=args.iterations, img_width=args.width, img_height=args.height, save=args.save)
    else:
        if not all(arg is None for arg in [args.x, args.y, args.magnification]):
            print("Arguments ignored. Please provide all of x, y, & m.")
        render = Framework(master, height, color_palette=args.color_palette, iterations=args.iterations,
                           img_width=args.width, img_height=args.height, save=args.save)
    master.geometry("{}x{}".format(render.canvasW, render.canvasH))
    master.mainloop()

main()
