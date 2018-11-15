# 卡方独立性检验
from scipy.stats import chi2_contingency
from scipy.stats import chi2
from scipy import stats
import numpy as np
import cv2


def chi2_independence(alpha, data):
    g, p, dof, expctd = chi2_contingency(data)

    if dof == 0:
        print('自由度应该大于等于1')
    elif dof == 1:
        cv = chi2.isf(alpha * 0.5, dof)
    else:
        cv = chi2.isf(alpha * 0.5, dof - 1)

    if g > cv:
        re = 1
    else:
        re = 0

    return g, p, dof, re, expctd


def get_image_array(image_path):
    # 以彩色图片的形式读取图片
    rgb_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # 将颜色空间进行转换，RGB -> YCRCB
    ycbcr_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2YCR_CB)

    # 提取灰度分量Y
    y = ycbcr_image[:, :, 0]
    sp = rgb_image.shape

    # 转化为一维数组
    im_array_flatten = y.flatten()

    return im_array_flatten


if __name__ == '__main__':
    a = get_image_array("3-0.bmp")
    b = get_image_array("replace.bmp")
    c = get_image_array("match.bmp")
    alpha1 = 0.05  # 置信度，常用0.01，0.05，用于确定拒绝域的临界值

    pixil = [0 for i in range(256)]
    for i in c:
        pixil[i] += 1

    test1 = []
    test2 = []
    for i in range(len(pixil)):
        if i % 2 == 0 and pixil[i] != 0:
            test1.append(pixil[i])
        if i % 2 == 1 and pixil[i] != 0:
            test2.append(pixil[i])

    print(type(test1))
    print(len(test1))
    print(test1)
    print(type(test2))
    print(len(test2))
    print(test2)

    data1 = np.array([test2, test1[:-1]])
    g, p, dof, re, expctd = chi2_independence(alpha1, data1)
    print("g:%f" % (g))
    print("p:", end="")
    print(p)
    print("re:%d" % (re))
    print("====================================================")
