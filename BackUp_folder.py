#用迭代的方法实现文件夹的同步
'''
首先要求输入一个FROM文件夹,再要求输入一个TO文件夹,
第二步,同步这两个文件夹的文件和子文件夹,
第三步,子文件夹一样处理,对于文件是否需要同步,检查文件夹的时间即可
'''
import os
import shutil
import time
def syncopy(from_path,to_path):
    '''将from_path中文件同步至to_path'''
    if not os.path.exists(to_path):
        os.makedirs(to_path)
        for root,dirs,files in os.walk(from_path):
            for file in files:
                src_file=os.path.join(root,file)
                shutil.copy(src_file,to_path)
            for dir in dirs:
                syncopy(os.path.join(root,dir),os.path.join(to_path,dir))
            break
        os.utime(to_path,(os.path.getatime(from_path),os.path.getmtime(from_path)))
    else:
        #存在文件夹,则直接比较一下时间,看看时间一直么?一直的话,不管文件,不一致的话,即管文件也管文件夹.
        if os.path.getmtime(from_path)==os.path.getmtime(to_path):
            #只管子文件夹
            for root, dirs, files in os.walk(from_path):
                for dir in dirs:
                    syncopy(os.path.join(root, dir), os.path.join(to_path, dir))
                break
        else:
            #目标里面的文件删掉,重考(删掉),文件夹不存在也删掉
            for root, dirs, files in os.walk(to_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    os.remove(src_file)
                for dir in dirs:
                    src_folder = os.path.join(from_path, dir)
                    if not os.path.exists(src_folder):
                        shutil.rmtree(os.path.join(root, dir))
                break
            # 目标里面的文件删掉,重考(重拷)
            for root, dirs, files in os.walk(from_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    shutil.copy(src_file, to_path)
                for dir in dirs:
                    syncopy(os.path.join(root, dir), os.path.join(to_path, dir))
                break
            os.utime(to_path, (os.path.getatime(from_path), os.path.getmtime(from_path)))
t_statr=time.time()
current_dir=os.path.dirname(__file__)
to_path=input("请输入 TO 文件夹:")
from_path=input("请输入 FROM 文件夹:")
if os.path.exists(to_path) and os.path.exists(from_path)  :
    if input("COPY " + from_path + " TO " + to_path + " (Y//N):") == "Y":
        s_t = time.time()
        syncopy(from_path, to_path)
        e_t = time.time()
    print("复制完毕耗时{0}".format(e_t - s_t))
else:
    print("文件夹不存在")
input("按任意键结束")

