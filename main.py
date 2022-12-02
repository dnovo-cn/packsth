import globalData as gl
import tkinter as tk
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
from tkinter import font
from psth_function import handle_file, app_init, handle_config
import globalData as gl

common_bg_color = '#93A2A9'
common_font_color = '#FFFFFF'

win = tk.Tk()
win.title('PackSth')

# 程序窗口自适应
screenwidth = win.winfo_screenwidth()
screenheight = win.winfo_screenheight()
_ww = int(screenwidth * .5)
_wh = int(screenheight * .5)
size_geo = '%dx%d+%d+%d' % (_ww, _wh, (screenwidth - _ww) / 2, (screenheight - _wh) / 2)
win.geometry(size_geo)

# 窗口背景颜色
win.config(background="#93A2A9")
# 设置窗口的透明度
win.attributes('-alpha', 1)
win.iconbitmap('./favicon.ico')

def get_file_path():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askdirectory()
    if filename != '':
        label_file_path.config(text=filename)
        temp = {"file_path": filename}
        handle_config('update', temp)
    else:
        label_file_path.config(text='您没有选择任何文件')


def get_package_path():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askdirectory()
    if filename != '':
        label_package_path.config(text=filename)
        temp = {"package_path": filename}
        handle_config('update', temp)
    else:
        label_package_path.config(text='您没有选择任何文件')


def get_winara_path():
    # 从本地选择一个文件，并返回文件的目录
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        label_winara_path.config(text=filename)
        temp = {"WinARA_path": filename}
        handle_config('update', temp)
    else:
        label_winara_path.config(text='您没有选择任何文件')


btn_file_dir = Button(win, text='Select File Path', bd=0, padx=6, pady=2, command=get_file_path, bg='#409eff',
                      fg='#ffffff', activebackground='#79bbff', activeforeground='#ffffff')
btn_file_dir.place(x=20, y=20)
label_file_text = tk.Label(win, text="待处理文件目录：", font=14, fg='#FFFFFF', bg=common_bg_color, borderwidth=0)
label_file_text.place(x=20, y=60)
label_file_path = Label(win, text='', bg='#87CEEB')
label_file_path.place(x=200, y=60)

btn_package_dir = Button(win, text='Select Save Path', bd=0, padx=6, pady=2, command=get_package_path, bg='#409eff',
                         fg='#ffffff', activebackground='#79bbff', activeforeground='#ffffff')
btn_package_dir.place(x=20, y=100)
label_package_text = tk.Label(win, text="压缩包存放目录：", font=14, fg='#FFFFFF', bg=common_bg_color, borderwidth=0)
label_package_text.place(x=20, y=140)
label_package_path = Label(win, text='', bg='#87CEEB')
label_package_path.place(x=200, y=140)

btn_winara = Button(win, text='Select winARA Path', bd=0, padx=6, pady=2, command=get_winara_path, bg='#409eff',
                      fg='#ffffff', activebackground='#79bbff', activeforeground='#ffffff')
btn_winara.place(x=20, y=180)
label_winara_text = tk.Label(win, text="winARA压缩软件执行文件路径：", font=14, fg='#FFFFFF', bg=common_bg_color, borderwidth=0)
label_winara_text.place(x=20, y=220)
label_winara_path = Label(win, text='', bg='#87CEEB')
label_winara_path.place(x=300, y=220)

btn_dir_select = Button(win, text='开始处理', bd=0, padx=4, command=handle_file)
btn_dir_select.place(x=20, y=260)

if __name__ == "__main__":
    gl._init()
    app_init()
    win.mainloop()
