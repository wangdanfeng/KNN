# coding:utf-8
'''
包装前端所需要的接口
'''
from flask import Flask, flash, request, render_template, Response,make_response,jsonify
import os
from read_preds import *
app  = Flask(__name__)

@app.route('/acc',methods=['GET', 'POST'])
def acc():
    module_path = os.path.dirname(__file__)
    paths = []
    feat_type = request.args.get('rtype')
    if feat_type == 'c64':
        paths = ['/static/data/c64/pred_acc_5_L2_c64.txt', '/static/data/c64/pred_acc_5_L1_c64.txt','/static/data/c64/pred_acc_1_L1_c64.txt','/static/data/c64/pred_acc_1_L2_c64.txt']#后续完善为url参数形式
    if feat_type == 'sift':
        paths = ['/static/data/sift/pred_acc_5_L2_sift.txt', '/static/data/sift/pred_acc_5_L1_sift.txt','/static/data/sift/pred_acc_1_L1_sift.txt','/static/data/sift/pred_acc_1_L2_sift.txt']
    if feat_type == 'lbp64':
        paths = ['/static/data/lbp/pred_acc_5_L2_lbp64.txt', '/static/data/lbp/pred_acc_5_L1_lbp64.txt','/static/data/lbp/pred_acc_1_L1_lbp64.txt', '/static/data/lbp/pred_acc_1_L2_lbp64.txt']
    if feat_type == 'lbp8':
        paths = ['/static/data/lbp/pred_acc_5_L2_lbp8.txt', '/static/data/lbp/pred_acc_5_L1_lbp8.txt','/static/data/lbp/pred_acc_1_L1_lbp8.txt', '/static/data/lbp/pred_acc_1_L2_lbp8.txt']
    labelAcc = []
    for path in paths:
        path = module_path + path
        d = read_acc(path)
        labelAcc.append(d)
    res_dict = {"code": 200, "content": labelAcc}
    # res = json.dumps(labelAcc)
    res = jsonify(res_dict)
    # make_response()
    return res
@app.route('/similar',methods=['GET', 'POST'])
def res():#10个分类里面，每个类分错的前5个和分对的前5个结果显示

    module_path = os.path.dirname(__file__)#获取当前目录
    path = '/static/data/lbp/pred_res_5_L2_lbp8.txt'
    feat_type = request.args.get('rtype')
    if feat_type == 'lbp8':
        path = '/static/data/lbp/pred_res_5_L2_lbp8.txt'
    if feat_type == 'lbp64':
        path = '/static/data/lbp/pred_res_5_L2_lbp64.txt'
    if feat_type == 'sift':
        path = '/static/data/sift/pred_res_5_L2_sift.txt'
    if feat_type == 'c64':
        path = '/static/data/c64/pred_res_5_L2_c64.txt'
    path = module_path + '/' + path
    labelAcc = read_res(path, res_k)
    res_dict = {"code": 200, "content": labelAcc}
    # res = json.dumps(res_dict)
    res = jsonify(res_dict)
    return res

# @app.route('/list.html',methods=['GET', 'POST'])
# def home():
#
#     return render_template('list.html')
# @app.route('/list/id',methods=['GET', 'POST'])
# def list():
#     filen = 'data/pred_res_5_L2.txt'
#     list_w = dict_show(filen, l='0')
#     print 'list_w:',list_w
#
#     return render_template('list.html', list_w=list_w, msg="wdf!")
# @app.route('/signin',methods=['GET'])
# def signin_form():
#     return '''<form action="/signin" method="post">
#               <p><input name="username"></p>
#               <p><input name="password" type="password"></p>
#               <p><button type="submit">Sign In</button></p>
#               </form>'''
# @app.route('/signin', methods=['POST'])
# def signin():
#     if request.form['username'] == 'admin' and request.form['password'] == 'password':
#         return '<h3>Hello, admin!</h3>'
#     return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    # res()
    # exit(0)
    cache = ''
    # app.run()
    app.run(host='172.18.24.28', port=5001, debug=True)#在243服务器上测试