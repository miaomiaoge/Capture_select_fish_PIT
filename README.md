鱼类图像采集、PIT信息读取记录、特定候选个体预警提示
============================================  

**主要功能**：在对体内注射有PIT标签的鱼类进行图像采集时，同步实现鱼类图像采集、PIT信息读取、特定个体筛选报警提醒等功能。

## 介绍：
* 1、 文件 Cand_ID.xlsx 存储的是需要挑选的特定候选个体，ID 表示 需要挑选的特定鱼类候选群体的PIT标签，Family表示鱼类所属的家系，如GS3，GS6，GS11等，若无挑选不同家系候选个体的需求，则将Family一列全部设置为GS，
* 2、 目录 voice 存储的是各种警报的声音，可根据个人喜好更改为自己喜欢的声音
* 3、 文件 cap_select_fish.py 是主程序，在python环境下运行即可打开摄像头和PIT扫描器的扫码功能，
* 4、 文件 requirement.txt 是环境依赖，运行代码前请先安装安装anaconda，接着：
## 安装使用：
      创建虚拟环境：`conda create -n CeFish python=3.8 -y`
      激活环境：`conda activate CeFish`
      安装依赖：`pip install -r requirement.txt`
