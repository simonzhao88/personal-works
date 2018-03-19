from ctypes import *


dllpath = 'C:\\Users\\MooN\\Desktop\\潮阳异地医保文件\\读卡DEMO\\SSCardDriver.dll'
bloom = CDLL(dllpath)
print(bloom.iReadCardBas(1, str))