import glob
from tkinter import *
import sys
from PIL import Image, ImageTk
from natsort import natsorted
import os
import shutil

sys.setrecursionlimit(10 ** 6)

i = 0

rotation = [0, 90, 180, 270]
orientation_ = 0
current = 0


def available_dir(path):
    return path.replace("\\", "//")


image_link = available_dir(os.getcwd()) + "//"

# image_link = "path/to/photo/folder/"
un_fav_img_path = image_link + "Down//"
fav_img_path = image_link + "Up//"
img_path_1 = image_link + "1//"
img_path_2 = image_link + "2//"
img_path_3 = image_link + "3//"
img_path_4 = image_link + "4//"
img_path_5 = image_link + "5//"
img_path_6 = image_link + "6//"
img_path_7 = image_link + "7//"
img_path_8 = image_link + "8//"
img_path_9 = image_link + "9//"
img_path_10 = image_link + "10//"

files = glob.glob(image_link + '*.jpg', recursive=True)
files = natsorted(files)
# print(files)

status = True


def log(lines):
    f = open(os.path.join(image_link + "log.txt"), "w")
    f.writelines(lines)
    f.close()


def move_and_show(path, i):
    if not os.path.exists(path):
        os.mkdir(path)
    shutil.move(files[i], path + "/" + os.path.basename(files[i]))
    files.remove(files[i])
    if i > len(files) - 1:
        i = 0
    log(files[i])
    show_img(files[i], i)


def orientation(status):
    global current
    if status == "next":
        current += 1
        if current > 3:
            current = 0
        return rotation[current]
    if status == "previous":
        current -= 1
        if current < 0:
            current = 3
        return rotation[current]


def key(event):
    # print(str(len(inspect.stack())) + " / " + str(sys.getrecursionlimit()))
    global i
    global status
    global orientation_
    if event.keysym == "Right":
        i += 1
        # print(files[i])
        if i > len(files) - 1:
            i = 0
        log(files[i])
        show_img(files[i], i)
    if event.keysym == "Left":
        i -= 1
        if i < 0:
            i = len(files) - 1
        # print(files[i])
        log(files[i])
        show_img(files[i], i)
    if event.keysym == "Up":
        move_and_show(fav_img_path, i)
    if event.keysym == "Down":
        move_and_show(un_fav_img_path, i)
    if event.keysym == "1":
        move_and_show(img_path_1, i)
    if event.keysym == "2":
        move_and_show(img_path_2, i)
    if event.keysym == "3":
        move_and_show(img_path_3, i)
    if event.keysym == "4":
        move_and_show(img_path_4, i)
    if event.keysym == "5":
        move_and_show(img_path_5, i)
    if event.keysym == "6":
        move_and_show(img_path_6, i)
    if event.keysym == "7":
        move_and_show(img_path_7, i)
    if event.keysym == "8":
        move_and_show(img_path_8, i)
    if event.keysym == "9":
        move_and_show(img_path_9, i)
    if event.keysym == "0":
        move_and_show(img_path_10, i)

    if event.keysym == "End":
        orientation_ = orientation("next")
    if event.keysym == "Home":
        orientation_ = orientation("previous")

    if event.keysym == "Return":
        if status:
            root.overrideredirect(True)
            status = False
        else:
            root.overrideredirect(False)
            status = True


root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(False)
root.geometry("%dx%d+0+0" % (w, h))

root.focus_set()
root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit(), sys.exit()))
root.bind("<Key>", key)
canvas = Canvas(root, width=w, height=h, highlightthickness=0)
canvas.pack()
canvas.configure(background='black')

# return last viewed image
try:
    g = open(os.path.join(image_link + "log.txt"), "r")
    lines = g.read().split("\n")
    last_line = lines[0]
    indices = [i for i, s in enumerate(files) if last_line in s][0]  # get index at 0 position
    # print(indices)
    image = files[indices]
    i = indices
except FileNotFoundError:
    video = files[0]
    i = 0
    pass


def show_img(file, i):
    if root.winfo_width() == 1:
        w_, h_ = root.winfo_screenwidth(), root.winfo_screenheight()
    else:
        w_, h_ = root.winfo_width(), root.winfo_height()
    canvas.delete("all")
    pilImage = Image.open(file)
    pilImage = pilImage.rotate(orientation_, expand=1)
    imgWidth, imgHeight = pilImage.size

    if imgWidth > w_ or imgHeight > h_:
        ratio = min(w_ / imgWidth, h_ / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)

    image = ImageTk.PhotoImage(pilImage)
    text = str(i + 1) + "/" + str(len(files)) + " : " + os.path.basename(files[i])
    canvas.create_image(w_ / 2, h_ / 2, anchor=CENTER, image=image)
    canvas.create_text(w_ / 2, h_ / 30, text=text, font=("TimeNewRoman", 16))
    canvas.mainloop()


show_img(files[i], i)
root.mainloop()
