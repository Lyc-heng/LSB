from PIL import Image
import numpy as np
import cv2
import time
import os
import random

# 用来记录嵌入比特数
count0 = 0
count1 = 0


# 将十进制数转8位二进制数
def bin_value(value, bitsize):
    binval = bin(value)[2:]
    if len(binval) > bitsize:
        print("Larger than expexted size")
    while len(binval) < bitsize:
        binval = "0" + binval
    return binval


# 提取图片中的水印信息
# image_path:所要提取的图片名称
def embed(image_path):
    # 查看所要嵌入的图片格式是否是bmp
    # 非bmp的话，转化为bmp格式
    if os.path.splitext(image_path)[1] != 'bmp':
        im = Image.open(image_path).save('temp.bmp')

    # 将图片转化为灰度图片的形式
    im = Image.open("temp.bmp").convert('L')

    # 以数组的格式将图片数据取出
    im_array = np.array(im)

    # 将二维数组转化为一维数组
    im_array_flatten = im_array.flatten()

    # 初始化，为读取前八位数据做准备
    start_bin = bin(0)

    # 前8位数据中存储了水印长度信息
    for c in range(0, 8):
        start_bin = start_bin + bin_value(im_array_flatten[c], 8)[7:]

    # 获取隐藏信息长度
    code_length = int_value(start_bin[3:])
    start_bin = bin(0)

    # 存储结构的数组
    temp_bin = [0 for x in range(code_length)]

    # 用来标记读取到第几个数据
    index = 8
    # 将水印信息挨个提取出来
    for c in range(0, code_length):
        for n in range(0, 8):
            start_bin = start_bin + bin_value(im_array_flatten[index], 8)[7:]
            index += 1
        temp_bin[c] = int_value(start_bin[3:])
        start_bin = bin(0)

    # 数字转ASCII码
    for c in range(0, code_length):
        print(chr(temp_bin[c]), end='')


# 将整串水印转化为二进制形式
def watermark_to_encode(watermark):
    binval = bin(0)[2:0]
    data_length = len(watermark)  # 获取字符串长度
    bindata = bin_value(data_length, 8)  # 将十进制的水印长度转化为8位二进制
    for c in bindata:
        binval = binval + c
    for char in watermark:
        # ord函数将当前字符转化为整数
        # bin_value将字符对应的整数转化为二进制字符串
        # 然后用for循环逐一去除二进制字符串的单个字符为C
        for c in bin_value(ord(char), 8):
            binval = binval + c
    return binval


# 实现8位二进制转十进制
def int_value(bin_code):
    code_number = 0
    index = 7
    for c in bin_code:
        code_number = code_number + int(c) * (2 ** index)
        index -= 1
    return code_number


# 将水印嵌入到图片当中去
# image_path:所要嵌入水印的图片
# markedfile:嵌入水印后的图片
# str:所要嵌入的字符串
def encode(image_path, markedfile, str):
    global count0
    global count1
    # 以彩色图片的形式读取图片
    rgb_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # 将颜色空间进行转换，RGB -> YCRCB
    ycbcr_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2YCR_CB)

    # 提取灰度分量Y
    y = ycbcr_image[:, :, 0]
    sp = rgb_image.shape

    # 转化为一维数组
    im_array_flatten = y.flatten()

    # 将要嵌入的消息全部转为二进制数据
    watermark = watermark_to_encode(str)
    # 水印长度
    watermark_len = len(watermark)

    # 用来存储嵌入图片后的图像
    output = [0 for i in range(0, len(im_array_flatten))]

    # 对图片进行全嵌入
    for i in range(len(im_array_flatten)):
        temp = bin_value(im_array_flatten[i], 8)

        if temp[-1] == watermark[i % watermark_len]:
            output[i] = int_value(temp)
        elif im_array_flatten[i] == 0:
            output[i] = int_value(temp) + 1
        elif im_array_flatten[i] == 255:
            output[i] = int_value(temp) - 1
        else:
            rand = random.randint(0, 1)
            output[i] = int_value(temp)
            if rand == 0:
                count0 += 1
                output[i] += 1
            else:
                count1 += 1
                output[i] -= 1


    # 将一维数组转为二维数组
    watermarked_dct_image = np.reshape(output, (sp[0], sp[1]))

    # 获取源图片的其他两个位面信息
    new_ycbcr_image = ycbcr_image

    # 将灰度界面变为嵌入水印后的界面
    new_ycbcr_image[:, :, 0] = watermarked_dct_image

    # 将图片转为RGB模式
    watermarked_rgb = cv2.cvtColor(new_ycbcr_image, cv2.COLOR_YCR_CB2BGR)

    # 以RGB模式进行图片保存
    cv2.imwrite(markedfile, watermarked_rgb)

if __name__ == '__main__':
    # 要加入到图片中的水印信息
    str = "helloxld"

    # 将水印嵌入到图片中
    start_CPU = time.clock()
    encode("3-0.bmp", "match.bmp", str)
    end_CPU = time.clock()
    print("本次程序运行的时间为%.10f秒" % (end_CPU - start_CPU))
    print(count0)
    print(count1)
    print(((count1+count0)/(512*512))*100)
    # 将图片水印中的信息提取出来
    # embed("test.bmp")
