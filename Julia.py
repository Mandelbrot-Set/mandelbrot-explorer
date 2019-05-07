# Python code for Julia Fractal
# https://www.geeksforgeeks.org/julia-fractal-python/
from PIL import Image
import opt
import time

# driver function
if __name__ == "__main__":

    # setting the width, height and zoom
    # of the image to be created
    w, h, zoom = 1920, 1080, 1

    # creating the new image in RGB mode
    bitmap = Image.new("RGB", (w, h), "white")

    # Allocating the storage for the image and
    # loading the pixel data.
    pix = bitmap.load()

    # setting up the variables according to
    # the equation to create the fractal
    cX, cY = -0.7, 0.27015
    moveX, moveY = 0.0, 0.0
    maxIter = 255

    start = time.time()
    for x in range(w):
        for y in range(h):
            zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
            zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY

            z, c = complex(zx, zy), complex(cX, cY)
            i = opt.julia_escape_time(z, c, maxIter)

            # i = maxIter
            # while zx * zx + zy * zy < 4 and i > 1:
            #     tmp = zx * zx - zy * zy + cX
            #     zy, zx = 2.0 * zx * zy + cY, tmp
            #     i -= 1

            # convert byte to RGB (3 bytes), kinda
            # magic to get nice colors
            pix[x, y] = (i << 21) + (i << 10) + i * 8

    print("执行时间 {} 秒".format(round(time.time() - start, 2)))
    # to display the created fractal
    bitmap.show()
