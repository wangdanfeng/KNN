# KNN
#使用KNN算法对图片进行打标分类，并对结果进行分析展示。
* **使用前需要先把sift和color64的第三方库放到KNN目录下,data放到static下**
*  **sift:**
KNN\colordescriptors40\x86_64-linux-gcc
* **color64:**
KNN\features
* **data:**
 static\data
* **原始数据，图片集：**  static\data\cifar-10-python
* **从原始数据保存的图片集：**  static\data\img
 	由于图片太多，已经删除，需要先生成到相应目录下。
  另外特征也需要生成，文件太大了。
* **生成的特征：** static\data\feats
* **预测结果以及准确率结果：** static\data\c64,lbp,sift等
* **预测结果分析页面：** static\index.html
* **c64第三方库：** features
* **sift提取特征和生成codebook的第三方库：** colordescriptors40\x86_64-linux-gcc

* **c64特征提取和sift特征提取要跑代码：** 040.py
* **lbp特征提取直接跑代码：** classifier04.py
* **结果分析时服务启动代码：** server.py
