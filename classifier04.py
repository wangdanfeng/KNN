# coding:utf-8
'''
用于颜色特征，lbp和sift的预测，
其中sift特征提取代码在colordescriptors40/x86_64-linux-gcc下面的：
exampleCreateCodebook.py和extraDescriptor.py
预测结果和特征分别保存在static/data/lbp,sift,c64 和feats目录下
'''
import json
import numpy as np
import cv2
import PIL
import cPickle, os, time, json
import matplotlib.pyplot as plt
from scipy.misc import imsave
from KNN import KNN
from featureExtra import *
def predict(k, L, fea_name=''):
    '''

    :param k: 指定返回k个想相近的结果
    :param L: 指定哪种距离计算方式
    :param fea_name: 指定抽取不同的特征
    :return:准确率，类别准确率，预测最优和最差类别
    tips: 预测过程会保存预测详细和预测结果数据，供显示和分析结果使用
    '''
    train_data, train_labels, train_filenames, test_data, test_labels, test_filenames = load_data_5(5, fea_name=fea_name)

    labels = list(set(test_labels))
    u_labels, num = np.unique(test_labels, return_counts=True)
    tests_num = len(test_labels)

    classifier = KNN(train_data, train_labels, train_filenames)
    # 测试某条数据
    # k = 5
    # L = 'L2'
    # pred_label, list_pred_res = classifier.predict(test_data[17], k=k, L=L)
    # print"cow_pony_s_000038.png:", test_data[17], pred_label, list_pred_res[:5]
    # exit(0)
    dict_i_acc = {}
    list_i_acc = []
    for i in u_labels:
        dict_i_acc[i] = 0
    acc_num = 0
    u_labels, num = np.unique(test_labels, return_counts=True)


    # 用于保存预测准确率的文件
    bins = ''
    if fea_name == 'lbp':
        bins = LBP_bins
    pre_acc_filepath = 'static/data/%s/pred_acc_%s_%s_%s%s.txt' % (fea_name, str(k), L, fea_name, bins)
    # 用于保存所有图片预测结果的文件
    list_pred_label = []
    list_list_pred_res = []
    k = k
    L = L
    label = '%s_%s' % (L, str(k))#k,L,featname标记
    file = 'static/data/%s/pred_res_%s_%s_%s%s_%s.txt' % (fea_name, str(k), L, fea_name, bins, time.time())
    print "k值和距离函数：%s" % file
    start_t = time.time()

    for x in xrange(tests_num):
        # pred_label, list_pred_res = classifier.predict(test_data[x], k=k, L=L)
        pred_label, list_pred_res = classifier.predict(test_data[x], k=k, L=L, isscale=True)
        actual_label = test_labels[x]
        # 一次写100 * n行
        # actual_filename = test_filenames[x]
        list_pred_label.append(pred_label)
        list_list_pred_res.append(list_pred_res)
        if (x + 1) % 200 == 0:
            save_pred_res(file, test_labels[((x - 199)):(x + 1)], test_filenames[((x - 199)):(x + 1)],
                          list_pred_label[((x - 199)):(x + 1)], list_list_pred_res[((x - 199)):(x + 1)])
            print "写了%s条数据了" % (x + 1)

        if pred_label == actual_label:
            acc_num = acc_num + 1
            dict_i_acc[actual_label] += 1

    for k, v in dict_i_acc.items():
        l_sum = num[int(k)]
        dict_i_acc[k] = dict_i_acc[k] / np.float(l_sum)
        list_i_acc.append(dict_i_acc[k])

    acc = acc_num * 1.0 / tests_num

    label_acc_max = dict_i_acc.keys()[np.argmax(dict_i_acc.values())]
    label_acc_min = dict_i_acc.keys()[np.argmin(dict_i_acc.values())]
    pred_dict = {"kl": label, "acc": acc, 'labelAcc': list_i_acc}
    save_pred_acc(pre_acc_filepath, pred_dict)#保存预测准确率结果
    print "acc:", acc
    print 'dict_i_acc:', dict_i_acc
    print 'list_i_acc:', list_i_acc
    print 'label_acc_max:', label_acc_max
    print 'label_acc_min:', label_acc_min
    return acc, label, list_i_acc, test_labels, list_pred_label
def save_dict(impath, feat, filepath):
    with open(filepath, 'a') as fo:
        fo.write(impath+"#"+feat)
        fo.write('\n')
        # json.dump(data, fo, ensure_ascii=False)
def save_data_info(): # 存储all-data-info,
#TypeError: array([6, 9, 9, ..., 9, 1, 1]) is not JSON serializable

    train_data, train_labels, train_filenames, test_data, test_labels, test_filenames = load_data_5(5, False)
    d_dict = {
        'train_data': train_data,
        'train_labels': train_labels,
        'train_filenames': train_filenames,
        'test_data': test_data,
        'test_labels': test_labels,
        'test_filenames': test_filenames
              }
    file = 'all_data_info.txt'
    # d_dict = {'a':1, 'b':'qdd'}
    with open(file, 'w') as fo:
        json.dump(d_dict, fo, ensure_ascii=False)
def save_pred_acc(file, dict):
    with open(file, 'w') as f:
        # f.write(json.dumps(dict))
        json.dump(dict, f, ensure_ascii=False, skipkeys=True)
        f.write('\n')
def save_pred_res(file,actual_labels, actual_filenames, pred_labels, list_pred_ress):
    # 拼接数据：testimg_id pre_label 前10个[{trainimg_id: score},...],分别k=1,5和L='L1','L2'等4个文件
    #testimg_id ： 0-airbus_s_001259.png

    # print 'testimg_id:',testimg_id
    with open(file, 'a') as f:
        for x in range(len(actual_labels)):
            actual_label, actual_filename, pred_label, list_pred_res = actual_labels[x], actual_filenames[x], pred_labels[x], list_pred_ress[x]
            testimg_id = np.str(actual_label) + '-' + actual_filename
            f.write(testimg_id+'#'+np.str(pred_label)+'#')
            for tuple_item in list_pred_res:
                trainimg_id = np.str(tuple_item[0])+'-'+tuple_item[1]
                f.write(trainimg_id + ':' + np.str(tuple_item[2]) + ',')
            f.write('\n')
def nptest():
    A = [[1, 2], [3, 4], [5, 6], [1, 2]]
    mat1 = [1, 2]
    print np.array(A)-np.array(mat1)
    print type(A)
    print type(np.array(A))

def mat_to_img(mat, save_file):
    img = np.reshape(mat, (3, 32, 32))
    img = img.transpose(1, 2, 0)
    imsave(save_file, img)
    # plt.imshow(img)
    # plt.show()
def load_label_names(root):
    '''@brief:装载batchs.meta,包含了label_names'''
    file = os.path.join(root, 'batches.meta')
    with open(file, 'rb') as of:
        meta = cPickle.load(of)
    return meta["label_names"]
def load_data_5(n, issave=False, isFirst=False, fea_name=''):#'',lbp, c64,sift
    ''''' @n There are n batches is need to load
          @issave, Do you need to save the images
       '''
    data_dir = 'static/data/cifar-10-python/'
    batchs = range(1, n+1)
    dataset_5 = ''
    # dataset_5 = np.array([], dtype=np.uint8).reshape(0, 3072)
    #这样初始化后，就能使用
    # np.concatenate((dataset_5, dict_data["data"]), axis=0)

    labels_5 = ''
    filenames_5 = ''
    for n in batchs:
        dict_data = load_data(data_dir, 'data_batch_' + str(n))
        if n == 1:
            dataset_5 = dict_data['data']
            labels_5 = dict_data["labels"]
            filenames_5 = dict_data['filenames']
        else:
            dataset_5 = np.concatenate((dataset_5, dict_data['data']), axis=0)
            labels_5 = np.concatenate((labels_5, dict_data["labels"]), axis=0)
            filenames_5 = np.concatenate((filenames_5, dict_data['filenames']), axis=0)
        # print n , len(dataset_5)
    tests = load_data(data_dir, 'test_batch')
    test_data = tests["data"]
    test_labels = tests["labels"]
    test_filenames = tests["filenames"]
    if fea_name == 'sift':
        # r1 = np.load(feat_sift_trains_cbk_filepath)
        # r2 = np.load(feat_sift_tests_cbk_filepath)
        r1 = np.load(feat_sift_trains_filepath)
        r2 = np.load(feat_sift_tests_filepath)
        dataset_5 = r1['codebook']
        test_data = r2['codebook']
    if fea_name == 'lbp':# dataset_5 和 test_data 更新为lbp特征向量
        if isFirst is True:
            dataset_5_new = np.array([], dtype=np.float64).reshape(0, LBP_bins)
            test_data_new = np.array([], dtype=np.float64).reshape(0, LBP_bins)
            for x in range(len(labels_5)):
                impath = 'static/data/img/trains/%s-%s' % (labels_5[x], filenames_5[x])
                img = io.imread(impath, as_gray=True)
                feat = get_lbp_fea(img, LBP_P, LBP_R, LBP_bins)  # lbp图归一化得到
                dataset_5_new = np.row_stack((dataset_5_new, feat))
            dataset_5 = dataset_5_new
            for x in range(len(test_labels)):
                impath = 'static/data/img/tests/%s-%s' % (test_labels[x], test_filenames[x])
                img = io.imread(impath, as_gray=True)
                feat = get_lbp_fea(img, LBP_P, LBP_R, LBP_bins)  # lbp图
                test_data_new = np.row_stack((test_data_new, feat))
            test_data = test_data_new



            np.savez(feat_lbp_filepath, dataset_5=dataset_5, test_data=test_data)
        else:
            r = np.load(feat_lbp_filepath)
            dataset_5 = r['dataset_5']
            test_data = r['test_data']
    if issave is True:
        # 存储所有图片（6w张）,图片命名格式，只要能分清楚 0-airbus_s_001259.png
        #存储一次就好
        for x in xrange(len(labels_5)):
            mat_to_img(dataset_5[x], 'static/data/img/trains/%s-%s' % (labels_5[x], filenames_5[x]))
        for x in xrange(len(test_labels)):
            mat_to_img(test_data[x], 'static/data/img/tests/%s-%s' % (test_labels[x], test_filenames[x]))

    return dataset_5, labels_5, filenames_5, test_data, test_labels, test_filenames
def load_data(root, batch):
    ''''' @brief: There are 5 batches and a test-batch
           in ../data/cifar-10-python. 每个batch打开有key:['data'
           , 'labels', 'batch_label', 'filenames']
           @param batch: batch-n/test-batch
       '''
    file = os.path.join(root, batch)
    with open(file, 'rb') as fo:
        dataset= cPickle.load(fo)
    return dataset
if __name__ == "__main__":
    # load_data_5(5, isFirst=True, fea_name=fea_name_lbp)
    # exit(0)

    start = time.time()
    print "预测中"
    # k = 5
    # L = 'L2'
    # fea_name = 'c64'
    # fea_name = 'lbp'
    # fea_name = 'sift'
    # acc, label, list_i_acc, test_labels, list_pred_label = predict(k5, L2, fea_name_lbp)
    # acc, label, list_i_acc, test_labels, list_pred_label = predict(k5, L1, fea_name_lbp)
    # acc, label, list_i_acc, test_labels, list_pred_label = predict(k1, L1, fea_name_lbp)
    # acc, label, list_i_acc, test_labels, list_pred_label = predict(k1, L2, fea_name_lbp)

    acc, label, list_i_acc, test_labels, list_pred_label = predict(k5, L2, fea_name_sift)
    acc, label, list_i_acc, test_labels, list_pred_label = predict(k5, L1, fea_name_sift)
    acc, label, list_i_acc, test_labels, list_pred_label = predict(k1, L1, fea_name_sift)
    acc, label, list_i_acc, test_labels, list_pred_label = predict(k1, L2, fea_name_sift)
    print "预测结束，耗时%s s" % (time.time()-start)


