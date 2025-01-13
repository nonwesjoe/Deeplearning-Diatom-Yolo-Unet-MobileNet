from collections import Counter
import tkinter as tk
from tkinter import filedialog
import super
from PIL import Image, ImageTk

segout=super.segout

def clear_all_labels():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
def model_out():
    path=select_image()
    clear_all_labels()

    label = tk.Label(root, text="Your Image", font=("Arial", 15), bg="gray")
    label.place(x=300,y=10)

    dec,dit=super.dectect(path)
    show_image(dec)
    show_subimage(dit)
    countdit=counter(dit)

    return dec

def show_image(img,img_size=(740, 554),place=[35, 55]):
    # 创建标签
    x=place[0]
    y=place[1]
    img = Image.fromarray(img).resize(img_size)
    image=ImageTk.PhotoImage(img)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=x,y=y)

def show_subimage(dit):
    x = 30
    y = 660
    n=0
    for path,cla in dit.items():
        n=n+1
        # name = os.path.join(segout, path)
        img = Image.open(path)
        img = img.resize((224,224) )
        image = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=image)
        label.photo = image
        label.place(x=x, y=y)

        label = tk.Label(root, text=f'{n}-{cla}', font=("Arial", 15), bg="white")
        label.place(x=x, y=y)

        x = x + 270
def select_image(): # 打开文件对话框，选择图片文件
    # 初始化Tkinter的根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # 打开文件对话框，选择图片文件
    file_path = filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif")]
    )
    # 打印并返回文件路径
    if file_path:
        print(f"选择的图片路径: {file_path}")
    else:
        print("未选择图片")
    return file_path

def background():
    label = tk.Label(root, text="Your Image", font=("Arial", 15), bg="white")
    label.place(x=100,y=10)

def counter(dit):
    empty = []
    for key, v in dit.items():
        empty.append(v)
    animal_count = dict(Counter(empty))
    x=800
    y=200
    all=len(empty)
    label = tk.Label(root, text=f'All: : {all}', font=("Arial", 15), bg="white")
    label.place(x=x,y=y)
    for key, value in animal_count.items():
        y=y+40
        label = tk.Label(root, text=f'{key}: {value}', font=("Arial", 15), bg="white")
        label.place(x=x,y=y)

    return animal_count

root = tk.Tk()
root.title("wsz GUI")  # 设置窗口标题
root.config(bg='black')
root.geometry("1240x850")  # 设置窗口大小

button = tk.Button(root, text="SELECT  IMAGE", command=model_out,padx=12,pady=12,font=("Arial", 15),fg='white',bg='green')
button4 =tk.Button(root, text="EXIT", command=root.quit,padx=12,pady=12,font=("Arial", 15),fg='white',bg='red')

button.pack(pady=10)
button4.pack(pady=10)  # 使用 pack 布局，pady设置上下间距

button.place(x=800,y=80)
button4.place(x=800,y=500)
# 启动GUI主循环
root.mainloop()
