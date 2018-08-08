# coding:utf-8
import numpy as np
class KNN:
    '''分类器基类:
    __init__,初始化类
    predict,return 预测结果

    '''
    def __init__(self, X, Y, Z):
        self.Xtd = X
        self.ytd = Y
        self.ztd = Z
    def predict(self, x, k=1, L='L1', isscale=False):
        '''
        :param x:
        :param k:
        :param L:
        :param isscale: 是否处理那种随机分类的数据
        :return:
        '''
        distances = []
        # mat1 = self.Xtd.astype(np.int32)#需要先转uint类型，否则计算的距离不准，导致整个结果不准确
        # mat2 = x.astype(np.int32)
        mat1 = self.Xtd
        mat2 = x
        if(mat1.dtype == np.uint8):# 原始像素特征需要先转uint类型，否则计算的距离不准，导致整个结果不准确
            mat1 = mat1.astype(np.int32)
            mat2 = mat2.astype(np.int32)
        if L == 'L2':  # 返回欧式距离
            ms = np.sum(np.square(mat1 - mat2), axis=1)
            distances = np.sqrt(ms)
        else:
            # 计算普通距离
            distances = np.sum(np.abs(mat1 - mat2), axis=1)
        #构造预测结果，前10个最小距离
        index_sort = np.argsort(distances)[:10]
        list_pred_res = []
        for x in index_sort:
            tuple_item = (self.ytd[x], self.ztd[x], distances[x])
            list_pred_res.append(tuple_item)
            # dict_pred = {}
            # img_id = np.str(self.ytd[x]) +'-'+ self.ztd[x]
            # score = distances[x]
            # dict_pred[img_id] = score
            # list_pred_res.append(dict_pred)
        k_labels = [self.ytd[x] for x in np.argsort(distances)][:k]
        # k_labels = np.array([3, 2, 6, 4, 8])
        u, num = np.unique(k_labels, return_counts=True)
        max_num = num.tolist().count(num[np.argmax(num)])
        # k个类别中，哪个类别的个数最多，如果个数最多的不止一个类别，返回第一个，也就是距离较近
        #并设置阈值，看是否需要增加权重处理随机分类的数据
        if (max_num != 1) and isscale:#不唯一的类别的non_uniqueness_l
            non_uniqueness_l = [u[x] for x in np.argsort(num)][-max_num:]
            # 返回第一个在non_uniqueness_l，也就是距离较近的
            for i in k_labels:
                if i in non_uniqueness_l:
                    # print k_labels, u, num, max_num, k_l, i
                    return i, list_pred_res
        return u[np.argmax(num)], list_pred_res  # np.argmax(num)返回沿轴axis最大值的索引

 # k个类别中，哪个类别的个数最多，如果个数最多的不止一个类别，返回第一个，也就是距离较近
def non_uniqueness(k_labels):#可以删除，class KNN中并未调用，而是重写的。
    u, num = np.unique(k_labels, return_counts=True)
    max_num = num.tolist().count(num[np.argmax(num)])
    if max_num != 1:
        # 返回第一个最大的，也就是距离较近的
        k_l = [u[x] for x in np.argsort(num)][-max_num:]
        for i in k_labels:
            if i in k_l:
                return k_labels, u, num, max_num, k_l, i

if __name__ == '__main__':
    k_labels = np.array([3, 8, 6, 6, 8])
    k_labels, u, num, max_num, k_l, i = non_uniqueness(k_labels)
    print k_labels, u, num, max_num, k_l, i