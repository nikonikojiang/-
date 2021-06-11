import win32api,win32gui,win32con,win32ui
import os
import time
from ctypes import windll
from PIL import Image
import cv2
import numpy

##########################自定义设置#######################

#模糊比对精度，越靠近1，精度越高。
treshold = 0.8
#target存放目录
targetDir = './Target'
#窗口名称
wndName = '雷电模拟器'


######################获取窗口句柄#########################

print('正在获取窗口句柄...')
hWnd = win32gui.FindWindow(0,wndName)
if(hWnd):
    print('父窗口句柄为：',hWnd)
else:
    print('获取窗口句柄失败')

hWnd2 = win32gui.FindWindowEx(hWnd,0,0,None)
if(hWnd):
    print('子窗口句柄为:',hWnd2)
else:
    print('获取子窗口句柄失败')



#获取后台窗口的句柄，注意后台窗口不能最小化
#获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = (int)((right - left)*1.25)
height = (int)((bot - top)*1.25)
#返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
#创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
#创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()
#创建位图对象准备保存图片
saveBitMap = win32ui.CreateBitmap()

######################模拟左键点击函数#########################
    
def Click(position):
    #传入需要点击的坐标[x,y]
    l_param = win32api.MAKELONG((int)(position[0]/1.25),(int)(position[1]/1.25))
    print('点击位置',position)
    win32api.SendMessage(hWnd2, win32con.WM_LBUTTONDOWN, 0, l_param)
    time.sleep(0.5)
    win32api.SendMessage(hWnd2, win32con.WM_LBUTTONUP, 0, l_param)
    time.sleep(0.5)

######################获取子窗口客户区屏幕快照#########################
    
def ScreenShot():
    #获取当前窗口屏幕快照
    
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)

    #如果要截图到打印设备：
    ###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
    result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),0)
    if (result == 1):
        print('屏幕截图成功') #PrintWindow成功则输出1
    else:
        print('屏幕截图失败')
    #保存图像
    ##方法一：windows api保存
    ###保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC,"./ScreenShot/screen.bmp")
    screen = cv2.imread('./ScreenShot/screen.bmp')
    return screen
########################目标搜寻#########################################

def Locate(target):
    #传入target为图片,返回该图片中心点的[x,y]
    screen = ScreenShot()
    result = cv2.matchTemplate(screen, target, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= treshold)
    print(location)
    try:
        y,x = location[0][0]-33,location[1][0]
    except:
        return 0
    else:
        
        high,width = target.shape[:-1]
        x=(int)(width/2+x)
        y=(int)(high/2+y)
        position = [x,y]
        print('坐标',position)
        return position

########################寻找目标点击并确认点击成功################################

def FindTouch(target):
    #传入图片对象target
    position=Locate(target)
    while(position == 0):
        print('未找到目标')
        print('3秒后重试')
        time.sleep(1)
        print('2秒后重试')
        time.sleep(1)
        print('1秒后重试')
        time.sleep(1)
        position = Locate(target)
    print('成功找到目标')
    Click(position)
######################加载target文件函数#############################
    
def LoadTarget():
#返回值是target图片文件列表targetList
    targetDir = './Target/'
    print('正在从'+targetDir+'文件夹中读取target...')
    targetNameList = os.listdir(targetDir)

    print('targetNameList\n',targetNameList)
    #创建target列表，将文件夹内图片依次读入
    targetList = []
    for i in targetNameList:
        targetList.append(cv2.imread(targetDir+i))

    print('读取成功！target个数：',len(targetList))
    return targetList



######################脚本本体#################################



    



    
