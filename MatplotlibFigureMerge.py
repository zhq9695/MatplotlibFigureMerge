import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import matplotlib.image as mpimg
from ProcessFigure import ProcessFigure


class MatplotlitFigureMerge():
    def __init__(self):
        # 初始化设置
        self.window = tk.Tk()
        self.window.geometry('600x360')
        self.window.title('MatplotlibFigureMerge')

        # 初始化选择图片按钮
        self.select_path_btn = tk.Button(self.window, text='图片文件夹选择', command=self.select_path)
        self.select_path_btn.grid(row=1, column=1, padx=5, pady=5)

        # 初始化合成图片按钮
        self.merge_btn = tk.Button(self.window, text='合成', command=self.figs_merge)
        self.merge_btn.grid(row=1, column=2, padx=5, pady=5)

        # 初始化图片路径
        self.imgs_path = None
        self.imgs_name = None
        self.imgs_labels = None

        # 初始化图片位置设置
        self.imgs_posx_label_1 = None
        self.imgs_posy_label_1 = None
        self.imgs_posx_label_2 = None
        self.imgs_posy_label_2 = None
        self.imgs_posx = None
        self.imgs_posy = None

    def select_path(self):
        # 获取图片路径
        self.imgs_path = filedialog.askopenfilenames(title='选择图片',
                                                     filetypes=[('jpg files',
                                                                 '*.jpg;*.JPG;*.jpeg;*.JPEG;*.png;*.PNG;*.bmp;*.BMP')])
        self.imgs_name = [path[path.rfind('/') + 1:] for path in self.imgs_path]
        for i in range(len(self.imgs_name)):
            if len(self.imgs_name[i]) > 10:
                self.imgs_name[i] = self.imgs_name[i][:10]
        if len(self.imgs_path) == 0:
            return
        if len(self.imgs_path) > 16:
            messagebox.showerror('错误', '选择文件数量请小于16个')
            return

        # 清除原先的控件
        if self.imgs_labels != None:
            for i in range(len(self.imgs_labels)):
                self.imgs_labels[i].grid_remove()
                self.imgs_posx[i].grid_remove()
                self.imgs_posy[i].grid_remove()

        # 添加图片位置提示
        self.imgs_posx_label_1 = tk.Label(self.window, text='行')
        self.imgs_posx_label_1.grid(row=2, column=2, padx=5, pady=5)
        self.imgs_posy_label_1 = tk.Label(self.window, text='列')
        self.imgs_posy_label_1.grid(row=2, column=3, padx=5, pady=5)
        if len(self.imgs_path) > 8:
            self.imgs_posx_label_2 = tk.Label(self.window, text='行')
            self.imgs_posx_label_2.grid(row=2, column=5, padx=5, pady=5)
            self.imgs_posy_label_2 = tk.Label(self.window, text='列')
            self.imgs_posy_label_2.grid(row=2, column=6, padx=5, pady=5)

        # 添加图片位置输入
        self.imgs_labels = [None for i in range(len(self.imgs_path))]
        self.imgs_posx = [None for i in range(len(self.imgs_path))]
        self.imgs_posy = [None for i in range(len(self.imgs_path))]
        for i in range(len(self.imgs_path)):
            if i < 8:
                self.imgs_labels[i] = tk.Label(self.window, text=self.imgs_name[i], justify='left')
                self.imgs_labels[i].grid(row=i + 3, column=1, padx=5, pady=5)

                self.imgs_posx[i] = tk.Entry(self.window, width=5, justify='left')
                self.imgs_posx[i].grid(row=i + 3, column=2, padx=5, pady=5)
                self.imgs_posy[i] = tk.Entry(self.window, width=5, justify='left')
                self.imgs_posy[i].grid(row=i + 3, column=3, padx=5, pady=5)
            else:
                self.imgs_labels[i] = tk.Label(self.window, text=self.imgs_name[i], justify='left')
                self.imgs_labels[i].grid(row=i - 5, column=4, padx=5, pady=5)

                self.imgs_posx[i] = tk.Entry(self.window, width=5, justify='left')
                self.imgs_posx[i].grid(row=i - 5, column=5, padx=5, pady=5)
                self.imgs_posy[i] = tk.Entry(self.window, width=5, justify='left')
                self.imgs_posy[i].grid(row=i - 5, column=6, padx=5, pady=5)

    def figs_merge(self):
        # 判断输入是否正确
        posx = np.array([x.get() for x in self.imgs_posx])
        posy = np.array([y.get() for y in self.imgs_posy])

        try:
            t = [float(x) for x in posx]
            t = [float(y) for y in posy]
        except:
            messagebox.showerror('错误', '请输入非零开头整数坐标')
            return

        if not np.array([x[0] != '0' for x in posx]).all() or \
                not np.array([y[0] != '0' for y in posy]).all() or \
                not np.array([x != None for x in posx]).all() or \
                not np.array([y != None for y in posy]).all():
            messagebox.showerror('错误', '请输入非零开头整数坐标')
            return

        posx = np.array([int(x) for x in posx])
        posy = np.array([int(y) for y in posy])

        t = np.zeros((posx.max(), posy.max()))
        for i in range(len(posx)):
            t[posx[i] - 1, posy[i] - 1] = 1
        if t.sum() != len(posx) or len(posx) != posx.max() * posy.max():
            messagebox.showerror('错误', '坐标无法填满一张图')
            return

        # 构建dict
        figure_mat = {}
        for i in range(len(self.imgs_path)):
            figure_mat[str(posx[i]) + '_' + str(posy[i])] = self.imgs_path[i]

        # 拼接图片
        proc = ProcessFigure(figure_mat)
        proc.start()
        proc.join()
        img = proc.get_result()

        # 保存图片
        save_path = filedialog.asksaveasfilename(title='保存图片', filetypes=[('all', '*.*')])
        mpimg.imsave(save_path + '.png', img)
        messagebox.showinfo('提示', '合成图片完成')

    def start(self):
        self.window.mainloop()


if __name__ == '__main__':
    MatplotlitFigureMerge().start()
