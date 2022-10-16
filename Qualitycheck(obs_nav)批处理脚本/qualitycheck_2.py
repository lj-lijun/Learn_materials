#Quality check for RINEX observation files using TEQC software.
#python3.8
#lijun
import argparse
import os,sys
import glob
from concurrent import futures
import datetime
import subprocess

check_information = \
(
    {'name': 'start', 'flag': 'Time of start of window :', 'pos': slice(25, 51)},
    {'name': 'end', 'flag': 'Time of  end  of window :', 'pos': slice(37, 51)},
    {'name': 'length', 'flag': 'Time line window length :', 'pos': slice(26, 42)},
    {'name': 'MP1', 'flag': 'Moving average MP12     :', 'pos': slice(26, 32)},
    {'name': 'MP2', 'flag': 'Moving average MP21     :', 'pos': slice(26, 32)},
    {'name': 'SN1', 'flag': 'Mean S1                 :', 'pos': slice(26, 31)},
    {'name': 'SN2', 'flag': 'Mean S2                 :', 'pos': slice(26, 31)}
)
#slice(start,end)从已有数组中返回选定的元素，返回一个新数组，包含从start到end（不包含该元素）的数组元素
# 定义命令行中的参数
def get_args():
    parser = argparse.ArgumentParser(description="quality check of using TEQC") #创建解释器-创建ArgumentParser()的对象parser
    parser.add_argument('-nav',type=str,metavar='<nav_files>',                  #通过add_argument添加参数nav
                        default='',help="Navigation files for complete mode")
    parser.add_argument('-obs',type=str,metavar='<obs_files>',                  #通过add_argument添加参数obs
                        default='', help="Observition files for complete mode" )
    parser.add_argument('-out',metavar='<format>',                              #通过add_argument添加参数out
                        choices=['table','t'],help="Out format to txt or screen")
    parser.add_argument('-fn',type=str,metavar='<filename>',                    #通过add_argument添加参数fn
                        default='result.txt',help="Custom file name")
    args=parser.parse_args()                                                    #命令行参数解析parser.parse_args()
    return args

#根据返回的参数获取文件并遍历存储
def get_files():
    global count                                 # 定义局部的全局变量
    args = get_args()

    nav_fn, obs_fn = args.nav, args.obs          # 获取文件夹名称
    out_format, out_fn = args.out, args.fn       # 获取输出形式和文件名

    path = os.getcwd()
    path_nav = os.path.join( path,nav_fn )       # 将当前路径与文件夹拼接（如'D:\\PycharmProjects\\nav'）
    path_obs = os.path.join( path,obs_fn )

    filename_nav=os.listdir(path_nav)            # 遍历文件夹下的文件,存储为列表
    filename_obs=os.listdir (path_obs)

    obs_count = len(filename_obs)                # 获取文件数量
    nav_count = len(filename_nav)
    #异常处理
    try:
        if obs_count == nav_count:
            count=obs_count
    except:
        print ( "|-----Tips:The number of obs does not equal the number of nav-----|\n"
                "|-----The process is about to terminate----|" )
        sys.exit ( 0 )

    return nav_fn,obs_fn,filename_nav,filename_obs,count,out_format,out_fn

#
def quality_check(nav_file,obs_file):
    args='teqc','+qc','-nav',nav_file,obs_file
    status,output=subprocess.getstatusoutput(' '.join(args))
    #print('status=',status)
    #print('output=',output)
    if status > 0:
        out = None
    else:
        out = output.split('\n')
    return out


def parallel_teqc():
    nav_fn,obs_fn,nav_file0, obs_file0, num, out_fmt,out_fn0=get_files ()
    #nav_fn,obs_fn文件夹名（brdc，bjfs）；nav_file, obs_file文件名(1.11n,1.11o)
    if out_fmt in ['t','table']:
        f=open ( out_fn0, mode='a+', encoding='utf-8' )
        header=print_header ()
        f.write (header+'\n')
        f.close ()
    else:
        print ( 'num=', num )
        print ( print_header () )
    # 线程池中创建最多执行1个线程，同时通过ThreadPoolExecutor来生成一个executor对象
    with futures.ThreadPoolExecutor(max_workers=1) as executor:

        for i in range(num):
            # 路径拼接(如：obs/bfdc1530.11n)
            path_nav_file=nav_fn+'/'+nav_file0[i]
            path_obs_file=obs_fn+'/'+obs_file0[i]
            # 调用executor对象的submit方法，提交1个任务
            future = executor.submit(quality_check,path_nav_file,path_obs_file)
            # 调用Future对象的result方法，返回被执行函数的结果
            res=future.result ()
            if res:
                record=parse_report(res)
                results=str(obs_file0[i])+str(record)
                res_0=results.replace("('",' ').replace("', '",' ').replace("', ",' ').replace(", '",' ')
                res=res_0.replace(' ','  ').replace("')",'\n')

                if out_fmt in ['t','table']:
                    f=open ( out_fn0, mode='a+', encoding='utf-8' )
                    f.write ( res )
                    f.close ()
                else:
                    print ( res )

# 从报表中获取需要的参数
def parse_report(report):
    marks = {}
    for item in check_information:
        for line in report:
            if item['flag'] in line:
                marks[item['name']] = line[item['pos']].strip()
                break

    # 获取字典中对应键的值
    sn1 = format(float(marks.get('SN1', 'nan')),'.2f')
    sn2 = format(float(marks.get('SN2', 'nan')),'.2f')
    mp1 = format(float(marks.get('MP1', 'nan')),'.2f')
    mp2 = format(float(marks.get('MP2', 'nan')),'.2f')
    date = datetime.datetime.strptime(marks['start'][0:11], '%Y %b %d')
    start = marks['start'][11:].strip()
    end = marks['end']

    last_line = next(l for l in reversed(report) if l.startswith('SUM'))
    last_line_pieces = last_line.split()
    length = float(last_line_pieces[-8])

    # Get the percentage of data, maybe unknown
    percentage = last_line_pieces[-4]
    if percentage == '-':
        percentage = float('nan')
    else:
        percentage = format(float(percentage),'.2f')

    # Get CSR from the last line of report, the olps may equal 0
    olps =round(float(last_line_pieces[-1]),0)
    if olps == 0:
        csr = float ( 'nan' )
    else:
        csr = format(1000 / olps,'.3f')
    result = (date.strftime('%Y-%m-%d'), start, end, length, percentage, sn1,
              sn2, mp1, mp2, olps, csr)
    return result

# 打印表头
def print_header():
    header=('file', 'date', 'start', 'end', 'hours', 'percent',
            'SN1', 'SN2', 'MP1', 'MP2', 'olsp' ,'CSR')
    style=('\n{0: ^14s} {1: ^12s} {2: ^14s} {3: ^14s} {4: >6s}  {5: >7s}'
           '{6: >6s}  {7: >6s}  {8: >6s}  {9: >5s}  {10: >5s} {11: >5s}')
    format=style.format ( *header )
    return format

if __name__ == '__main__':
    parallel_teqc()
