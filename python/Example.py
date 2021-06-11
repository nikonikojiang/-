import GameScript,time
#默认加载targetList
targetList = GameScript.LoadTarget()

##########################自定义设置#######################
#目标窗口可以遮挡，移动，但不能最小化
#模糊比对精度，越靠近1，精度越高，默认0.8。
GameScript.treshold = 0.8
#target存放目录
GameScript.targetDir = './Target'
#窗口名称
GameScript.wndName = '雷电模拟器'


#函数列表

#传入坐标[x,y]模拟左键点击(内置1秒间隔)
#GameScript.Click(pisition)

#获取当前窗口截图
#GameScript.ScreenShot()

#传入target图片，在当前窗口截图中寻找该图片
#若成功则返回坐标[x,y]，失败则返回0
#GameScript.Locate(target)

#加载target文件
#GameScript.LoadTarget()

#延迟指定秒数
#time.sleep(second)            



######示例识图点击

#首先获取图片坐标
#n为要识别的图片编号
n=0
position = GameScript.Locate(targetList[0])
print('position坐标为',position)

#使用点击函数模拟点击
if (position):
    GameScript.Click(position)
else:
    print('未找到目标')
