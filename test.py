# coding:utf-8
'''
相关代码简单测试用
'''
from skimage import feature as ft, io, color, data, img_as_float, img_as_ubyte
import numpy as np
import json, os
from config import *
# import features.color64 as fc64

def get_lbp_fea(image, P, R, bins=10):
    img_gray = color.rgb2gray(image)
    mat_lbp = ft.local_binary_pattern(img_gray, P, R, method='default')#从灰度图得到lbp图
    # 计算直方图量化，进行归一化处理，得到各直方图连成的特征向量
    hist_fea, bin_edges = np.histogram(mat_lbp, bins, density=True)
    return hist_fea
def hog(image, ori, ppc, cpb):
    features = ft.hog(image,  # input image
                      orientations=ori,  # number of bins
                      pixels_per_cell=ppc,  # pixel per cell
                      cells_per_block=cpb,  # cells per blcok
                      block_norm='L1',  # block norm : str {'L1', 'L1-sqrt', 'L2', 'L2-Hys'}
                      transform_sqrt=True,  # power law compression (also known as gamma correction)
                      feature_vector=True,  # flatten the final vectors
                      visualize=False)  # return HOG map
    return features

# def color64(impath):
#     # print fc64
#     # qry_vec = fc64.extractColor64("test.png")
#     qry_vec = fc64.extractColor64(impath)
#     # print " ".join(map(str, qry_vec))
#     return qry_vec

def do_px(img, i=10, j=10):
    img[i, :] = img[j, :]
    img[:, i] = 100
    img[:100, :50].sum() # 计算前100行，前50列所有数值的和
    img[50:100, 50:100] #50~100行，50~100列，但不包括第100行和第100列
    img[i].mean() # 第i行所有数值的平均值
    img[:, -1]  # 倒数第一列
    img[-2, :] # or img[-2] #倒数第二行
    #将宇航员图片进行二值化，像素值大于128的变为1, 否在变为0
    img = data.astronaut()
    img_gray = color.rgb2gray(img)
    rows, cols = img_gray.shape
    for i in range(rows):
        for j in range(cols):
            if (img_gray[i, j] <= 0.5):
                img_gray[i, j] = 0
            else:
                img_gray[i, j] = 1
    show(img_gray)
def label2rgb(): #  可以根据标签值对图片进行着色。以后的图片分类后着色就可以用这个函数。
    im = data.coffee()
    im_gray = color.rgb2gray(im)
    rows, cols = im_gray.shape

    labels = np.zeros([rows, cols])
    for i in range(rows):
        for j in range(cols):
            if im_gray[i, j] < 0.4:
                labels[i, j] = 0
            elif im_gray[i, j] < 0.75:
                labels[i, j] = 1
            else:
                labels[i, j] = 2
    ims = color.label2rgb(labels)
    show(ims)
def color_convert():
    img = data.coffee()
    img_hsv = color.convert_colorspace(img, 'RGB', 'HSV')
    show(img)
    show(img_hsv)
def change_G():# 先对R通道的所有像素值进行判断，如果大于170，则将这个地方的像素值变为[0,255,0], 即G通道值为255，R和B通道值为0。
    img = data.astronaut()
    img_float = img_as_float(img)
    print "img_float:", img_float.dtype.name
    img_uint8 = img_as_ubyte(img_float)
    print "img_uint8:", img_uint8.dtype.name

    # img_gray = color.rgb2gray(img)
    # print 'img_gray:',(img_gray.dtype.name)
    # img_idx_modify = img[:, :, 0] > 170
    # print (img_idx_modify.dtype.name)
    # print img.dtype.name
    # print '------'
    # img[img_idx_modify] = [0, 255, 0]
    # print img
def change_salt(img):
    rows, cols, dims = img.shape

    for i in range(5000):
        x = np.random.randint(0, rows)
        y = np.random.randint(0, cols)#表示随机生成一个整数， 范围在0到cols之间。
        img[x, y, :] = 255
    return img
def dom(img):
    print(type(img))  # 类型
    print(img.shape)  # 形状
    print(img.shape[0])  # 图片宽度
    print(img.shape[1])  # 图片高度
    print(img.shape[2])  # 图片通道数
    print(img.size)  # 显示总像素个数
    print(img.max())  # 最大像素值
    print(img.min())  # 最小像素值
    print(img.mean())  # 像素平均值
def show(img):
    io.imshow(img)
    io.show()
def getMoney(a,b,c):
    x = 540
    y = 2.87
    z = 464.48
    A = a-x
    B = b-y
    C = c-z
    # M = A - (B+C)
    M = a - (b+c)
    return  M
if __name__ == '__main__':
    '''
    4.5,         +72
    7K，          36.4     -36.25
    8K,          -23
    9k,  384.15  -83   -155.85
    10k, 444.35  -143
    11k, 448.75  --258.6  -331.25
    12k, 431.15  -369
    13k, 413
    15k，378.35  -809
    16k, 360.75
    17k, 306
    18k, 250.35
    20k, 137.35
    22k, 24.35
    23k, -32.15
    a,b,c:分别是调整后需要缴纳的公积金，五险，税
    '''
    b = 714
    a= 840
    c= 89.6
    print a+b+c
    res = getMoney(a,b,c)
    print res
    exit(0)
    # 4526.6
    # 620.75
    r = np.load(feat_c64_filepath)
    test_c64 = r["test_data"]
    print 'test_c64:',test_c64
    exit(0)

    a = np.array([[1,2,3],[4,5,6]])
    b = np.arange(0, 1.0, 0.1)
    c = np.sin(b)
    np.savez('res.npz',a,b,c)
    r = np.load('res.npz')
    print r['arr_0'] == a
    print r['arr_1'] == b
    print r['arr_2'] == c
    exit(0)
    path = 'data/img/trains/'
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        print file_path
    exit(0)
        # impath = 'cat.png'
    # image = io.imread(impath, as_gray=True)
    # img = data.hubble_deep_field()
    # img = data.chelsea()
    img = data.astronaut()

    # impath = 'test.png'
    # img = io.imread(impath)
    img2 = data.astronaut()
    img2 = color.rgb2grey(img2)
    # io.imshow(img2)
    # io.imsave('data-img2.png',img2)
    # print img #小数表示的是颜色程度
    # print "lbp"
    # print img2
    # exit(0)
    # show(img)
    # 像素读取, 显示B通道的20行，10列的像素值
    # print (img[20, 10, 2])
    # 显示红色单通道图片的程序如下
    img_R = img[:, :, 0]
    # show(img_R)
    # 像素修改，例如，对宇航员图片随机添加椒盐噪声
    # 随机生成5000个椒盐点
    # img = change_salt(img)
    # show(img)
    # 图片裁剪
    # partial_img = img[50:150, 170:270, :]
    # show(partial_img)
    # do_px(img)
    # change_G()
    # color_convert()
    # label2rgb()


    # ori = 9
    # ppc = (10, 10)
    # cpb = (20, 20)
    # features_hog = hog(img, ori, ppc, cpb)
    # # print features_hog

    # feat_lbp = get_lbp_fea(img, LBP_P, LBP_R, LBP_bins)# lbp图
    # print  feat_lbp
    print 'img2:',img2
    # ft.local_binary_pattern()
    # method='uniform'保证旋转不变性
    mat_lbp = ft.local_binary_pattern(img2, 8, 1, method='uniform')
    mat_lbp = np.arange(0, 10)
    print 'mat_lbp:',mat_lbp
    # 计算直方图量化，进行归一化处理，得到各直方图连成的特征向量
    # density=True 是归一化，结果是float64，0-9, 统计落到各个区间的概率proba = (n/sum)/bins
    # density=False 否归一化，结果是int64，0-255，统计mat_lbp中元素分别落到各区间的个数n
    # np.sum(hist_fea)#mat_lbp落到区间里的元素总数,#np.sum(hist_fea) < len(mat_lbp)
    # bin_edges,# [min,单位区间,..,max],其中单位区间：float(max-min)/(bins),max-min代表总区间：mat_lbp中元素的max-min
    hist_fea, bin_edges = np.histogram(mat_lbp, 10, density=False)
    print 'np.histogram:',np.histogram(mat_lbp, 10, density=True)
    print 'hist_fea:',hist_fea,np.sum(hist_fea),len(mat_lbp)
    print 'bin_edges',
    file = 'test_jsondump.txt'
    with open(file, 'a') as fo:
        fo.write("#"+str(hist_fea))
        fo.write('\n')
    # 1,保存特征，2整理提取特征的代码
    # file = 'test_jsondump.txt'
    # #test json.dump()
    # dict = {'name':'tom','id':102,'年龄':28}
    # with open(file, 'a') as f:
    #     json.dump(dict, f, ensure_ascii=False,skipkeys=True,separators=(',',":"))
    #     f.write('\n')

