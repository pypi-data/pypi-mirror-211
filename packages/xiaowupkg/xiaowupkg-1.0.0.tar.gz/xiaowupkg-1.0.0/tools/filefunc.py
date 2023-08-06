import os

def readfilename(path, filetype):     #获取ktr文件
    L=[]
    for root,dirs,files in os.walk(path):
        if root == path:
            for i in files:
                if os.path.splitext(i)[1] == filetype:
                    print(i)
                    L.append(i)
    return L