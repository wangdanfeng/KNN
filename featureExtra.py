# coding:utf-8
'''
获取LBP特征
'''
from skimage import feature as ft, io, color, data, img_as_float, img_as_ubyte
import numpy as np
from config import *
# import features.color64 as fc64

def get_lbp_fea(img_gray, P, R, bins=10):
    # img_gray = color.rgb2gray(image)
    # method='uniform'保证旋转不变性
    mat_lbp = ft.local_binary_pattern(img_gray, P, R, method='uniform')#从灰度图得到lbp图
    # 计算直方图量化，进行归一化处理，得到各直方图连成的特征向量
    # density=False 否归一化，结果是int64，统计mat_lbp中元素分别落到各区间的个数n
    # density=True 是归一化，结果是float64, 统计落到各个区间的概率proba = (n/sum)/bins
    # np.sum(hist_fea)#mat_lbp落到区间里的元素总数,#np.sum(hist_fea) < len(mat_lbp)
    # bin_edges,# [min,单位区间,..,max],其中单位区间：float(max-min)/(bins),max-min代表总区间：mat_lbp中元素的max-min
    hist_fea, bin_edges = np.histogram(mat_lbp, bins, density=True)
    return hist_fea

# def get_color64_fea(impath):
#     # qry_vec = fc64.extractColor64("test.png")
#     qry_vec = fc64.extractColor64(impath)
#     # print " ".join(map(str, qry_vec))
#     return qry_vec
def get_sift_feat(impath):
    pass
if __name__ == '__main__':
    pass
    # img = data.astronaut()
    # feat_lbp = get_lbp_fea(img, LBP_P, LBP_R, LBP_bins)  # lbp图