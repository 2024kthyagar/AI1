import PIL
import urllib.request
import io, sys
import tkinter as tk
from PIL import Image, ImageTk
import time

URL = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpoliticsandwar.com%2Fuploads%2F4d9aee1eb2b42d5ac53a288ce9705b1303e5264e1000x56217.jpeg&f=1&nofb=1&ipt=36f2a9ec33b33f3a03f21bfdace06e22faf7744b99f3340d98ef5b86006d0b28&ipo=images"
URL2 = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.kinja-img.com%2Fgawker-media%2Fimage%2Fupload%2Fs--W6mHh1KL--%2Fc_fill%2Cfl_progressive%2Cg_center%2Ch_900%2Cq_80%2Cw_1600%2F18m4flryve9m4jpg.jpg&f=1&nofb=1&ipt=702be96d9d3c91bc2d98a547bb3bcac337e9019a35bd1734f40b3405569736c9&ipo=images"

# window = tk.Tk()
imagefile = io.BytesIO(urllib.request.urlopen(URL).read())
img = Image.open(imagefile)
img.resize((600, 400))

imgfile2 = io.BytesIO(urllib.request.urlopen(URL2).read())
img2 = Image.open(imgfile2)
img2.resize((600, 400))

def chrome(color):
    return tuple(map(lambda x: int(x * 1.5), color))

def invert(color):
    return tuple(map(lambda x: 255 - x, color))

def tint(color, color2, amount=0.5):
    return tuple(map(lambda x, y: int(x * (1 - amount) + y * amount), color, color2))


def grayscale(color):
    return tuple(map(lambda x: int(sum(color) / 3), color))

def contrast(color, amount=0.5):
    return tuple(map(lambda x: int(x*(1+amount) if x > 2*255//3 else (x if x > 255//3 else x*(1-amount))), color))

def overlay(color, color2, amount=0.5):
    return tuple(map(lambda x, y: int(x * (1 - amount) + y * amount), color, color2))


pix = img.load()
pix2 = img2.load()

gif = []

for i in range(100):
    print(i)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            # pix[x,y] = chrome(pix[x,y])
            # pix[x,y] = tint(pix[x,y], (22, 81, 5), 0.2)
            # pix[x,y] = contrast(pix[x,y], .3)
            # pix[x,y] = invert(pix[x,y])
            pix[x,y] = overlay(pix[x,y], pix2[x,y], 1-i/100)
    gif.append(img.copy())

gif[0].save('out.gif', save_all=True, append_images=gif[1:], optimize=False, loop=0)




