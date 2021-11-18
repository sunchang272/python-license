# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: python-auth
File Name: gui.py
Author: sunch
Create Date: 2021/11/10 10:36 
-------------------------------------------------
"""

from tkinter import Tk, Toplevel, Label, Entry, Button, Menu, PhotoImage, StringVar, filedialog
from func import GenKey, EncLic, data_folder
import datetime


class NewKeyGUI:
    def __init__(self, frame):
        self.frame = frame
        self.key_name = None
        self.key_value = None
        self.gen_log = None
        self.key_name_label = None
        self.key_value_label = None
        self.gen_log_label = None
        self.help_text_label = None
        self.key_name_entry = None
        self.key_value_entry = None
        self.gen_key_btn = None
        self.rand_key_btn = None

    def init_window(self):
        self.frame.title('秘钥生成')  # 窗口名
        self.frame.geometry('520x200+600+100')
        self.frame['bg'] = '#F8F8FF'  # 窗口背景色，其他背景色见: blog.csdn.net/chl0000/article/details/7657887
        self.frame.attributes('-alpha', 0.95)  # 虚化，值越小虚化程度越高

        # StringVar
        self.key_name = StringVar()
        self.key_value = StringVar()
        self.gen_log = StringVar()

        # Label
        self.key_name_label = Label(self.frame, text='秘钥标识：', bg='#F8F8FF', font=('YaHei', 10))
        self.key_name_label.grid(row=0, column=0, pady=10, padx=10)
        self.key_value_label = Label(self.frame, text='AES秘钥：', bg='#F8F8FF', font=('YaHei', 10))
        self.key_value_label.grid(row=1, column=0, pady=10, padx=10)
        self.gen_log_label = Label(self.frame, textvariable=self.gen_log, bg='#F8F8FF', font=('YaHei', 10))
        self.gen_log_label.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky='W')
        self.help_text_label = Label(self.frame, text='帮    助：TODO', bg='#F8F8FF', font=('YaHei', 10))
        self.help_text_label.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='W')

        # Entry
        self.key_name_entry = Entry(self.frame, width=50, bd=1, textvariable=self.key_name, font=('YaHei', 10))
        self.key_name_entry.grid(row=0, column=1, pady=10, padx=5)
        self.key_value_entry = Entry(self.frame, width=50, bd=1, textvariable=self.key_value, font=('YaHei', 10))
        self.key_value_entry.grid(row=1, column=1, pady=10, padx=5)

        # Button
        self.gen_key_btn = Button(self.frame, text='生成秘钥', command=self.gen_key, bd=1, bg='#F8F8FF', width=15,
                                  font=('YaHei', 10))
        self.gen_key_btn.grid(row=2, column=0, pady=5, padx=10)
        self.rand_key_btn = Button(self.frame, text='随机生成', command=self.rand_key, bd=1, bg='#F8F8FF', width=15,
                                   font=('YaHei', 10))
        self.rand_key_btn.grid(row=2, column=1, pady=5, padx=5, sticky='W')

    def gen_key(self):
        key_gener = GenKey(self.key_name.get(), self.key_value.get())
        self.gen_log.set(key_gener.gen_keys())

    def rand_key(self):
        rand_name, rand_key = GenKey.rand_key()
        self.key_name.set(rand_name)
        self.key_value.set(rand_key)
        # self.gen_key()


class EncLicGUI:
    def __init__(self, frame):
        self.frame = frame
        self.aes_key_path = None
        self.ori_lic_path = None
        self.due_time = None
        self.gen_log = None
        self.aes_key_select_btn = None
        self.ori_lic_select_btn = None
        self.due_time_label = None
        self.gen_log_label = None
        self.help_text_label = None
        self.key_path_entry = None
        self.lic_path_entry = None
        self.due_time_entry = None
        self.enc_lic_btn = None

    def init_window(self):
        self.frame.title('License加密')  # 窗口名
        self.frame.geometry('520x400+600+100')
        self.frame['bg'] = '#F8F8FF'  # 窗口背景色，其他背景色见: blog.csdn.net/chl0000/article/details/7657887
        self.frame.attributes('-alpha', 0.95)  # 虚化，值越小虚化程度越高

        # StringVar
        self.aes_key_path = StringVar()
        self.ori_lic_path = StringVar()
        self.due_time = StringVar()
        self.gen_log = StringVar()

        # Button
        self.aes_key_select_btn = Button(self.frame, text='选择AES秘钥', command=self.get_key_path, bd=1, bg='#F8F8FF',
                                         width=15, font=('YaHei', 10))
        self.aes_key_select_btn.grid(row=0, column=0, pady=10, padx=10)
        self.ori_lic_select_btn = Button(self.frame, text='选择License', command=self.get_lic_path, bd=1, bg='#F8F8FF',
                                         width=15, font=('YaHei', 10))
        self.ori_lic_select_btn.grid(row=1, column=0, pady=10, padx=10)

        # Label
        self.due_time_label = Label(self.frame, text='输入到期时间：', bg='#F8F8FF', font=('YaHei', 10))
        self.due_time_label.grid(row=2, column=0, pady=10, padx=10)
        self.due_time.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.gen_log_label = Label(self.frame, textvariable=self.gen_log, bg='#F8F8FF', font=('YaHei', 10))
        self.gen_log_label.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky='W')
        self.help_text_label = Label(self.frame, text='帮    助：TODO', bg='#F8F8FF', font=('YaHei', 10))
        self.help_text_label.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky='W')

        # Entry
        self.key_path_entry = Entry(self.frame, textvariable=self.aes_key_path, width=50, font=('YaHei', 10))
        self.key_path_entry.grid(row=0, column=1, pady=10, padx=10)
        self.lic_path_entry = Entry(self.frame, textvariable=self.ori_lic_path, width=50, font=('YaHei', 10))
        self.lic_path_entry.grid(row=1, column=1, pady=10, padx=10)
        self.due_time_entry = Entry(self.frame, textvariable=self.due_time, width=50, font=('YaHei', 10))
        self.due_time_entry.grid(row=2, column=1, pady=10, padx=10)

        # Button
        self.enc_lic_btn = Button(self.frame, text='加密License', command=self.enc_lic, bd=1, bg='#F8F8FF', width=15,
                                  font=('YaHei', 10))
        self.enc_lic_btn.grid(row=3, column=0, pady=10, padx=10)

    def get_key_path(self):
        file_path = filedialog.askopenfilename(parent=self.frame, initialdir=data_folder, filetypes=[('ori', '*.ori')])
        self.aes_key_path.set(file_path)

    def get_lic_path(self):
        file_path = filedialog.askopenfilename(parent=self.frame, initialdir=data_folder, filetypes=[('ori', '*.ori')])
        self.ori_lic_path.set(file_path)

    def enc_lic(self):
        lic_enc = EncLic(self.aes_key_path.get(), self.ori_lic_path.get(), self.due_time.get())
        self.gen_log.set(lic_enc.enc_lic())


class AuthMainGUI:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        # Main Menu
        self.main_menu = None
        self.file_menu = None
        self.logo_img = None
        self.logo_img_label = None
        self.help_text_label = None
        self.copyright_text_label = None
        # New Key Window
        self.new_key_window = None
        self.new_key_portal = None
        # ENC LIC Window
        self.enc_lic_window = None
        self.enc_lic_portal = None

    # 设置窗口
    def init_window(self):
        self.init_window_name.title('注册工具_v1.0')  # 窗口名
        self.init_window_name.geometry('320x100+500+300')
        self.init_window_name['bg'] = '#F8F8FF'  # 窗口背景色，其他背景色见: blog.csdn.net/chl0000/article/details/7657887
        self.init_window_name.attributes('-alpha', 0.95)  # 虚化，值越小虚化程度越高

        # Main Menu Settings
        self.main_menu = Menu(self.init_window_name)
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.file_menu.add_command(label='New', command=self.display_new_key_frame)
        self.file_menu.add_command(label='Enc Lic', command=self.display_enc_lic_frame)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.init_window_name.quit)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.init_window_name.config(menu=self.main_menu)

        # Label
        self.logo_img = PhotoImage(file='assets/logo.png')
        self.logo_img_label = Label(self.init_window_name, image=self.logo_img, bg='#F8F8FF', width=50, height=50)

        self.help_text_label = Label(self.init_window_name, text='TODO', bg='#F8F8FF', font=('YaHei', 10))
        self.copyright_text_label = Label(self.init_window_name, text='TODO', bg='#F8F8FF', underline=0,
                                          font=('YaHei', 8, 'italic'))
        self.logo_img_label.grid(row=0, column=1)
        self.help_text_label.grid(row=0, column=0, padx=20)
        self.copyright_text_label.grid(row=1, column=0, padx=20, pady=20)

    def display_new_key_frame(self):
        self.new_key_window = Toplevel()
        self.new_key_portal = NewKeyGUI(self.new_key_window)
        self.new_key_portal.init_window()
        self.new_key_window.mainloop()

    def display_enc_lic_frame(self):
        self.enc_lic_window = Toplevel()
        self.enc_lic_portal = EncLicGUI(self.enc_lic_window)
        self.enc_lic_portal.init_window()
        self.enc_lic_window.mainloop()


def gui_open():
    # 实例化出一个父窗口
    init_window = Tk()
    main_portal = AuthMainGUI(init_window)
    # 设置根窗口默认属性
    main_portal.init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_open()
