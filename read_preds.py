# coding:utf-8
'''
分别从文件读取预测详细结果和追确率结果
'''
import os, re, time, json
import numpy as np
from config import *
# def dict_show(filepath, l='0', k1=5, k2=10):
#     '''
#     :param filepath: pred_res_file
#     :param l: label index
#     :param k1: return k1 个相似图片（train data）
#     :param k2: return k2 条 l 类别的数据(test data)
#     :return: k个 label_index == l 的pred res 的dict
#     '''
#     preds_list = readFile(filepath)
#     label_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#
#
#     # 用于保存准确率结果的文件
#
#     dict_i_acc = {}
#     list_dict_item = []
#     testimg_dir = '/static/img/tests/'
#     img_dir = '/static/img/trains/'
#     for i in xrange(len(label_names)):
#         dict_i_acc[str(i)] = 0
#     for x in preds_list:
#         x = re.split('#', x)
#         pred_label, list_pred_res = x[1], x[2]
#         test_img = re.split('-', x[0])
#         actual_label = test_img[0]
#         test_imgid = x[0]
#         # 页面上显示并分析预测结果 list_show
#         label = l
#         dict_test = {}
#         dict_img = {}
#         trains = []
#         dict_item = {}
#
#         if actual_label == label:
#             test_imgpath = os.path.join(testimg_dir, x[0])
#             dict_test['img_path'] = test_imgpath
#             dict_test['img_id'] = test_imgid
#             dict_test['pred_label'] = pred_label
#             # print 'test_imgpath:', test_imgpath
#             # list_1_k_img.append(test_imgpath)
#             # list_1_k_img.append(pred_label)
#
#             # test_imgpath: C:\workspace\python2\ABC\KNN\data\img\tests\3-domestic_cat_s_000907.png
#         # test_labels.append(actual_label)
#         #页面上显示并分析预测结果 list_show
#             img_items = re.split(',',list_pred_res)
#             for img_item in img_items:
#                 if img_item != '':
#                     dict_img = {}
#                     img = re.split(':', img_item)
#                     # print img
#                     imgid = img[0]
#                     img_distance = round(float(img[1]),2)#保留两位小数
#                     imgpath = os.path.join(img_dir, imgid)
#
#                     dict_img['path'] = imgpath
#                     dict_img['id'] = imgid
#                     dict_img['distance'] = img_distance
#                     trains.append(dict_img)
#             dict_item['trains'] = trains
#             dict_item['test'] = dict_test
#             list_dict_item.append(dict_item)
#
#     print "list_dict_item:", list_dict_item[:k2]
#     return list_dict_item[:k2]
#     # exit(0)
# # def dict_show(filepath, l='0', k1=5, k2=10):
# #     '''
# #     :param filepath: pred_res_file
# #     :param l: label index
# #     :param k1: return k1 个相似图片（train data）
# #     :param k2: return k2 条 l 类别的数据(test data)
# #     :return: k个 label_index == l 的pred res的list
# #     '''
# #     preds_list = readFile(filepath)
# #     label_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
# #
# #
# #     # 用于保存准确率结果的文件
# #
# #     dict_i_acc = {}
# #     list_dict_show = []
# #     testimg_dir = '/static/img/tests/'
# #     img_dir = '/static/img/trains/'
# #     for i in xrange(len(label_names)):
# #         dict_i_acc[str(i)] = 0
# #     for x in preds_list:
# #         x = re.split('#', x)
# #         pred_label, list_pred_res = x[1], x[2]
# #         test_img = re.split('-', x[0])
# #         actual_label = test_img[0]
# #         test_imgid = test_img[1]
# #         # 页面上显示并分析预测结果 list_show
# #         label = l
# #         # dict_show = {} #{testid:[test_imgpath,pred_label,k_imgpath,...]}
# #         # dict_k_img = {}
# #         list_show = []  # [testid,testimgpath,pred_label,[[test_imgpath,ditance],[test_imgpath,ditance],...]]
# #         list_1_k_img = []
# #         w_l_k_img = []
# #         if actual_label == label:
# #             test_imgpath = os.path.join(testimg_dir, x[0])
# #             # print 'test_imgpath:', test_imgpath
# #             # list_1_k_img.append(test_imgpath)
# #             # list_1_k_img.append(pred_label)
# #
# #             # test_imgpath: C:\workspace\python2\ABC\KNN\data\img\tests\3-domestic_cat_s_000907.png
# #         # test_labels.append(actual_label)
# #         #页面上显示并分析预测结果 list_show
# #             img_items = re.split(',',list_pred_res)
# #             for img_item in img_items:
# #                 if img_item != '':
# #                     l_k_img = []
# #                     img = re.split(':', img_item)
# #                     # print img
# #                     imgid = img[0]
# #                     img_distance = round(float(img[1]),2)#保留两位小数
# #
# #                     imgpath = os.path.join(img_dir, imgid)
# #                     # print 'imgpath:', imgpath
# #                     # imgpath: C:\workspace\python2\ABC\KNN\data\img\trains\4-dama_dama_s_000494.png
# #                     # dict_k_img[imgpath] = img_distance
# #                     l_k_img.append(imgpath)
# #                     l_k_img.append(imgid)
# #                     l_k_img.append(img_distance)
# #                     w_l_k_img.append(l_k_img)
# #             # print w_l_k_img[:2]
# #             # exit(0)
# #             # list_1_k_img.append(w_l_k_img[:2])
# #             list_show.append(x[0])
# #             list_show.append(test_imgpath)
# #             list_show.append(pred_label)
# #             list_show.append(w_l_k_img[:k1])
# #             list_dict_show.append(list_show)
# #             # dict_show[x[0]] = list_1_k_img
# #             # print 'dict_show:',dict_show
# #             # list_dict_show.append(dict_show)
# #     # return list_dict_show[:k]
# #     # print "list_dict_show[:k]",list_dict_show[:k]
# #     print "list_show:", list_dict_show[:k2]
# #     return list_dict_show[:k2]
# #     # exit(0)
# # def readFile(root, n=1):
# #     k =''
# #     L = ''
# #     data_list = []
# #     for x in os.listdir(root):
# #
# #         res = re.split('_', x)
# #         if(len(res) == 4):
# #             k = res[2]
# #             L = re.split('.txt', res[3])
# #             k_l = "%s_%s" % (k, L[0])
# #             print k_l
# #             pathname = os.path.join(root, x)
# #             with open(pathname, 'r') as f:
# #               lines = [line.strip() for line in f.readlines()]
# #               data_list.append(lines)
# #     return data_list[n-1]
# #               # # for lin in lines:
# #               # for line in f:
# #               #   print line
# #               #   exit(0)
# def readFile(path):
#     with open(path, 'r') as f:
#         lines = [line.strip() for line in f.readlines()]
#         return lines
# def get_acc_dict(preds_list):
#     start_t = time.time()
#     tests_num = len(preds_list)
#     test_labels = []
#     label_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#     list_pred_label = []
#     list_list_pred_res = []
#
#
#     # 用于保存准确率结果的文件
#
#     dict_i_acc = {}
#     dict_iname_acc = {}
#     acc_num = 0
#
#     for i in xrange(len(label_names)):
#         dict_i_acc[str(i)] = 0
#     for x in preds_list:
#         x = re.split('#', x)
#         pred_label, list_pred_res = x[1], x[2]
#         test_img = re.split('-', x[0])
#         actual_label = test_img[0]
#         test_imgid = test_img[1]
#
#         test_labels.append(actual_label)
#             #下面是计算准确率并保存的
#         # list_pred_label.append(pred_label)
#         # list_list_pred_res.append(list_pred_res)
#         # if (x + 1) % 200 == 0:
#         #     save_pred_res(file, test_labels[((x - 199)):(x + 1)], test_filenames[((x - 199)):(x + 1)],
#         #                   list_pred_label[((x - 199)):(x + 1)], list_list_pred_res[((x - 199)):(x + 1)])
#         #     print "写了%s条数据了" % (x + 1)
#         # if (x+1) % 100 == 0:
#         #     save_pred_res(file, test_labels[((x-99)):(x+1)], test_filenames[((x-99)):(x+1)], list_pred_label[((x-99)):(x+1)], list_list_pred_res[((x-99)):(x+1)])
#         #     print "写了%s条数据了" % x+1
#         # exit(0)
#         if pred_label == actual_label:
#             acc_num = acc_num + 1
#             dict_i_acc[actual_label] += 1
#
#
#     print "dict_i_acc：", dict_i_acc
#     # labels = list(set(test_labels))
#     u_labels, num = np.unique(test_labels, return_counts=True)
#     for k, v in dict_i_acc.items():
#         i = list(u_labels).index(k)
#         l_sum = num[i]
#         dict_i_acc[k] = v / np.float(l_sum)
#         dict_iname_acc[label_names[i]] = v / np.float(l_sum)
#
#     acc = acc_num * 1.0 / tests_num
#
#     # dict_i_acc = {0: 0.433, 1: 0.212, 2: 0.37, 3: 0.179, 4: 0.384, 5: 0.222, 6: 0.301, 7: 0.251, 8: 0.548, 9: 0.2}
#     label_acc_max = dict_i_acc.keys()[np.argmax(dict_i_acc.values())]
#     label_acc_min = dict_i_acc.keys()[np.argmin(dict_i_acc.values())]
#     print "预测中----:"
#     print "acc:", acc
#     print 'dict_i_acc:', dict_i_acc
#     print 'dict_iname_acc:', dict_iname_acc
#     print 'label_acc_max:', label_acc_max
#     print 'label_acc_min:', label_acc_min
#     print 'total time:', time.time() - start_t
#     exit(0)
#     return acc, dict_i_acc, label_acc_max, label_acc_min, test_labels
#
# def save_pred_acc(file, dict):
#     with open(file, 'w') as f:
#             f.write(json.dumps(dict))

def read_acc(filepath):
    with open(filepath, 'r') as fo:
        d = json.load(fo)
        return d
def wrap_img(lines, label, k):
    img_list_00 = []
    img_list_01 = []
    for line in lines:
        l_img = line.split('#')
        # print l_img
        img = l_img[0]
        true = img.split('-')[0]
        preb = l_img[1]
        if (true == label) & (preb == label):
            img_list_00.append(l_img)
        elif (true == label) & (preb != label):
            img_list_01.append(l_img)
    l_res = img_list_00[:k] + img_list_01[:k]#拿到某类别的分错和分对的K条数据
    l_d_img = []
    for y in l_res:
        file = y[0]
        label = y[1]
        similar = y[2][:-1]
        l_similar = similar.split(',')
        wrap_l_s_img = []
        for x in l_similar:
            l_s_img = x.split(':')
            lab = l_s_img[0].split('-')[0]
            l_s_img.append(lab)
            wrap_l_s_img.append(l_s_img)
        d_img = {'file':file,'label':label, 'similar':wrap_l_s_img}
        l_d_img.append(d_img)
    return l_d_img
def read_res(path, k):
    '''
    :param path:
    :param label:
    :param k:
    :return:
    '''
    lines = [line.strip() for line in open(path, 'r').readlines()]
    labels = [str(i) for i in range(0, 10)]
    wrap_dict = {}
    for lab in labels:
        l_d_img = wrap_img(lines, lab, k)
        wrap_dict[lab] = l_d_img
    return wrap_dict


if __name__  == "__main__":
    path = 'data/lbp/pred_res_5_L2_lbp8.txt'
    labelAcc = read_res(path, res_k)
    exit(0)
    # path = 'data/pred_res_5_L2_lbp8_1530152222.93.txt'
    # l1, l2 = read_res(path, '0')
    # print l1[:10],l2[:10]
    # exit(0)
    path = 'data/lbp/pred_acc_5_L2_lbp8.txt'
    d = read_acc(path)
    print d
    exit(0)

    # root = os.getcwd()+'\\data'
    #
    # # filen = 'pred_res_1_L1.txt'
    # # file = './data/pred_res_acc_1_L1.txt'
    # # filen = 'pred_res_1_L2.txt'
    # # file = './data/pred_res_acc_1_L2.txt'
    # # filen = 'pred_res_5_L1.txt'
    # # file = './data/pred_res_acc_5_L1.txt'
    # file = './data/pred_res_acc_5_L2.txt'
    # filen = 'pred_res_5_L2.txt'
    # # print filen
    # filepath = os.path.join(root, filen)
    # list_s = dict_show(filepath)
    # #返回距离？
    # print len(list_s)
    # exit(0)
    # # acc, dict_i_acc, label_acc_max, label_acc_min, test_labels = get_acc_dict(lines_1)
    #
    #
    # # acc = 0.3859
    # # dict_i_acc = {'1': 0.297, '0': 0.523, '3': 0.264, '2': 0.407, '5': 0.306, '4': 0.452, '7': 0.343, '6': 0.371,
    # #              '9': 0.276, '8': 0.62}
    # #
    # # label_acc_max = '8'
    # # label_acc_min = '3'
    # # start_t = time.time()
    # # test_labels = ['8', '3', '5']
    # pred_dict = {"acc:": acc, 'dict_i_acc:': dict_i_acc, 'label_acc_max:': label_acc_max,
    #              'label_acc_min:': label_acc_min}
    # save_pred_acc(file, pred_dict)

