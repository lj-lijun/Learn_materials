# python3
# code: utf-8
# author: 长大地测院 李军

from ftplib import FTP
from tqdm import tqdm
import os


def ftpconnect(host, username, password):
    ftp = FTP()  # 设置变量
    timeout = 30
    port = 21
    ftp.connect(host, port, timeout)  # 连接FTP服务器
    ftp.login(username, password)  # 登录
    return ftp


def ftp_download(ftp, remote_file, local_file):
    # 获取文件大小
    total_size = ftp.size(remote_file)

    # 打开本地文件并准备写入
    with open(local_file, 'wb') as f:
        # 定义回调函数用于更新下载进度
        def callback(data):
            f.write(data)
            pbar.update(len(data))

        # 使用 tqdm 创建进度条
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            # 下载文件并传递回调函数
            ftp.retrbinary('RETR {}'.format(remote_file), callback)


# 表文件下载网址之一： ftp://garner.ucsd.edu/pub/gamit/tables/

host = 'garner.ucsd.edu'
username = 'anonymous'
password = '82309349@qq.com'

tables_files = ['ut1.usno',
                'pole.usno',
                'leap.sec',
                'dcb.dat',
                'pmu.bull_f',
                'rcvant.dat',
                'svnav.dat',
                'igb14_comb.apr',
                'antmod.dat',
                'vmf1grd.2024']  # 定义需要下载的表文件

dirname = os.getcwd()  # 获取当前路径
print('dirname', dirname)
ftp_filepath = '/archive/garner/gamit/tables/'  # 远程服务器tables文件路径

print('登录远程服务器中 garner.ucsd.edu ……')
ftp = ftpconnect(host, username, password)  # 登录远程服务器
ftp.cwd(ftp_filepath)  # 进入远程服务器文件目录
print('已进入远程服务器文件目录 ！')

# print('文件目录如下 ： ！')
# ftp.dir()

num = len(tables_files)
for i in range(num):
    load_file = tables_files[i]
    print(load_file, '正在下载 ……')
    local_path = dirname + '/' + load_file  # 定义文件保存路径
    remote_file = ftp_filepath + '/' + load_file
    total_size = ftp.size(remote_file)  # 获取文件大小
    ftp_download(ftp, remote_file, local_path)





# ===================================
# ftp相关命令操作

# ftp.cwd(pathname) #设置FTP当前操作的路径
# ftp.dir() #显示目录下所有目录信息
# ftp.nlst() #获取目录下的文件
# ftp.mkd(pathname) #新建远程目录
# ftp.pwd() #返回当前所在位置
# ftp.rmd(dirname) #删除远程目录
# ftp.delete(filename) #删除远程文件
# ftp.rename(fromname, toname)#将fromname修改名称为toname。
# ftp.storbinaly(“STOR filename.txt”,file_handel,bufsize) #上传目标文件
# ftp.retrbinary(“RETR filename.txt”,file_handel,bufsize) #下载FTP文件

# 参考网站：https://cloud.tencent.com/developer/article/1741033

# ===================================
