import numpy as np
import matplotlib.image as mpimg
import threading


class ProcessFigure(threading.Thread):
    def __init__(self, figure_mat):
        threading.Thread.__init__(self)
        self.figure_mat = figure_mat

        # 图片的最大像素
        self.max_x = 0
        self.max_y = 0
        self.max_z = 0

        # 坐标列表
        self.pos = []

        # 去除图片的白边
        # 获取图片的最大像素
        # 获取坐标列表
        for key, value in self.figure_mat.items():
            self.figure_mat[key] = self.resize_figure(value)

            self.max_x = max(self.max_x, self.figure_mat[key].shape[1])
            self.max_y = max(self.max_y, self.figure_mat[key].shape[0])
            self.max_z = max(self.max_z, self.figure_mat[key].shape[2])

            self.pos.append([int(key[:key.find('_')]), int(key[key.find('_') + 1:])])

        self.pos = np.array(self.pos)

        # 空白拼接图片
        self.figure_img = np.ones((self.max_y * self.pos[:, 0].max(),
                                   self.max_x * self.pos[:, 1].max(), self.max_z))

    # 去除图片白边
    def resize_figure(self, img):
        img = mpimg.imread(img)
        x = 0
        xx = img.shape[0]
        y = 0
        yy = img.shape[1]
        for channel in range(img.shape[2]):
            for i in np.arange(0, img.shape[0], 1):
                if img[i, :, channel].sum() != img.shape[1]:
                    x = max(x, i)
                    break
            for i in np.arange(img.shape[0] - 1, -1, -1):
                if img[i, :, channel].sum() != img.shape[1]:
                    xx = min(xx, i)
                    break
            for j in np.arange(0, img.shape[1], 1):
                if img[:, j, channel].sum() != img.shape[0]:
                    y = max(y, j)
                    break
            for j in np.arange(img.shape[1] - 1, -1, -1):
                if img[:, j, channel].sum() != img.shape[0]:
                    yy = min(yy, j)
                    break
        return img[x - 5:xx + 5, y - 5:yy + 5, :]

    # 拼接图片
    def run(self):
        for x, y in self.pos:
            fig_y = self.figure_mat[str(x) + '_' + str(y)].shape[0]
            fig_x = self.figure_mat[str(x) + '_' + str(y)].shape[1]
            bias_y = int((self.max_y - fig_y) / 2)
            bias_x = int((self.max_x - fig_x) / 2)
            for channel in range(self.figure_img.shape[2]):
                self.figure_img[(x - 1) * self.max_y + bias_y:(x - 1) * self.max_y + bias_y + fig_y,
                (y - 1) * self.max_x + bias_x:(y - 1) * self.max_x + bias_x + fig_x,
                channel] = self.figure_mat[str(x) + '_' + str(y)][:, :, channel]

    def get_result(self):
        return self.figure_img
