import os
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile, asksaveasfile
import PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont

window = Tk()
window.geometry("1000x500")
window.title("Watermark App")
OPTIONS = ['Calibri', 'Arial', 'Verdana']
COLOR_OPTIONS=['Black', 'White', "Yellow", "Pink", "Blue", "Green"]
text_id = " "
position_var = IntVar()

def add_watermark():
    global text_id
    global font
    global color
    global position_x
    global position_y
    global fontsize_info
    global watermark_info
    global color
    if text_id != " ":
        canvas.delete(text_id)
    watermark_info = watermark_text.get()
    fontsize_info = fontsize.get()
    font = font_chosen.get()
    color = color_chosen.get()
    position_choice = position_var.get()
    if position_choice == 1:
        position_y = 5
        position_x = 5

    if position_choice == 2:
        position_y = 0
        position_x = img.width()- (len(watermark_info) * (int(fontsize_info)/2)) - int(fontsize_info)*.7

    if position_choice == 3:
        position_x = 5
        position_y = img.height() - int(fontsize_info) * 1.3

    if position_choice == 4:
        position_x = img.width()- (len(watermark_info) * (int(fontsize_info)/2)) - 8
        position_y = (img.height() - int(fontsize_info) * 1.3)


    text_id = canvas.create_text(position_x, position_y, anchor = NW, text=watermark_info, font=(font, fontsize_info), fill=color)


upload_button = Button(window, text="Upload Image", width=20, command = lambda:upload_file())
upload_button.grid(column=5,row=0)
canvas = Canvas(window, height=300, width=600)
canvas.grid(column=5, row=1, rowspan=5)
text_label = Label(text="Enter your watermark text:")
text_label.grid(column=3, row=1)
watermark_text = Entry()
watermark_text.grid(column=4, row=1)
fontsize_label = Label(text="Enter the desired font size")
fontsize_label.grid(column=3, row=3)
fontsize = Entry()
fontsize.grid(column=4, row=3)
font_label = Label(text="Pick your desired font")
font_label.grid(column=3, row=4)
font_chosen = StringVar(window)
font_chosen.set(OPTIONS[0])
font_dropdown = OptionMenu(window, font_chosen, *OPTIONS)
font_dropdown.grid(column=4, row=4)
color_label = Label(text="Pick your font color:")
color_label.grid(column=3, row=5)
color_chosen = StringVar(window)
color_chosen.set(COLOR_OPTIONS[0])
color_dropdown = OptionMenu(window, color_chosen, *COLOR_OPTIONS)
color_dropdown.grid(column=4, row=5)

r1= Radiobutton(window, text="Top Left", variable=position_var,value=1)
r1.grid(column=3, row=6)
r2 = Radiobutton(window, text="Top Right", variable=position_var,value=2)
r2.grid(column=4, row=6)
r3= Radiobutton(window, text="Bottom Left", variable=position_var,value=3)
r3.grid(column=3, row=7)
r4= Radiobutton(window, text="Bottom Right", variable=position_var,value=4)
r4.grid(column=4, row=7)
watermark_button= Button(window, text='Add Watermark', width=20, command=lambda:add_watermark())
watermark_button.grid(column=3, row=9)


def save_image():
    edit_image = ImageDraw.Draw(image)
    position_choice = position_var.get()

    if position_choice == 1:
        position_tuple = (0,0)

    if position_choice == 2:
        position_tuple= (image.width - 30, 0)

    if position_choice== 3:
        position_tuple = (0, image.height - 20)

    if position_choice == 4:
        position_tuple= (image.width - 30, image.height - 20)

    draw_font = ImageFont.truetype(fr"C:\Windows\Fonts\{font}.ttf", int(fontsize_info))
    edit_image.text(position_tuple, text= watermark_info, fill = color, font=draw_font)
    file_types = [('Jpg files', '*.jpg')]

    file = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=file_types)
    image.save(file)
    os.remove(f'{save_name}')

save_button=Button(window, text="Save Image", width=20, command=lambda:save_image())
save_button.grid(column=4, row=9)

def upload_file():
    global img
    global image
    global file_name
    global save_name
    file_types = [('Jpg files', '*.jpg')]
    file_name = filedialog.askopenfilename(filetypes=file_types)
    fixed_height = 300
    image = Image.open(file_name)
    if image.mode != "RGB":
        image = image.convert("RGB")
    height_percent = (fixed_height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    image = image.resize((width_size, fixed_height), PIL.Image.NEAREST)
    new_name = file_name.split('.')[0]
    save_name = f'{new_name}_preview.jpg'
    image.save(f'{save_name}')
    img = ImageTk.PhotoImage(Image.open(f'{save_name}'))
    canvas.create_image(0, 0, anchor=NW, image=img)



window.mainloop()

