# coding:utf-8
'''
获取LBP特征
'''
import numpy as np
from config import *
import features.color64 as fc64  #features/color64.py

def get_color64_fea(impath):
    # qry_vec = fc64.extractColor64("test.png")
    qry_vec = fc64.extractColor64(impath)
    # print " ".join(map(str, qry_vec))
    return qry_vec

if __name__ == '__main__':
    pass
    # img = data.astronaut()
    # feat_lbp = get_lbp_fea(img, LBP_P, LBP_R, LBP_bins)  # lbp图