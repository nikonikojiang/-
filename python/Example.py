import GameScript,time
#默认加载targetList
targetList = GameScript.LoadTarget()

##########################自定义设置#######################
#ver 1.0

#目标窗口可以遮挡，移动，但不能最小化
#模糊比对精度，越靠近1，精度越高，默认0.8。
GameScript.treshold = 0.8
#target存放目录
GameScript.targetDir = './Target/'
#窗口名称
GameScript.wndName = '雷电模拟器'


#函数列表

#传入坐标[x,y]模拟左键点击(内置1秒间隔)
#GameScript.Click(position)
#模拟鼠标从position1移动到position2
#LButtonDownMoveUP(position1,position2)

#获取当前窗口截图
#GameScript.ScreenShot()

#传入target图片，在当前窗口截图中寻找该图片
#若成功则返回坐标[x,y]，失败则返回0
#GameScript.Locate(target)

#加载target文件
#GameScript.LoadTarget()

#延迟指定秒数
#time.sleep(second)            


##等待
def Wait(second):
    for i in range(0,second):
        print('等待',second-i,'秒...')
        time.sleep(1)

######示例识图点击
def FindClick(n,name,  n2=-1, position2 = -1):
    i=0
    position = GameScript.Locate(targetList[n])
    while(position == 0):
        i=i+1
        #如4次找不到，则在第五次找备用点
        if(n2 !=-1 and position2 != -1 and i==5):
            position = GameScript.Locate(targetList[n2])
            if(position):
                GameScript.Click(position2)
            i=0
            
        print('未找到'+name+'\n3秒后重试...')
        Wait(3)
        position = GameScript.Locate(targetList[n])
    if(position):
        print('找到'+name)
        time.sleep(1)
        GameScript.Click(position)
        
#######自定义点击函数        
middle = [642,391]
north = [122,248]
south = [1147,502]
west = [127,512]
mapPosition = [100,100]
def CornerFindClick(n,name,direction, n2=-1,direction2=-1):
    i=0
    position = GameScript.Locate(targetList[n])
    

    while(position == 0):
        Wait(2)
        print('等待进入'+name)
        i=i+1
        ##若输入后两个参数会在没找到时找指定图片以及点击位置
        if(n2!=-1 and direction2 != -1 and i == 5):
            print('检查上一节点是否正常点击...')
            position = GameScript.Locate(targetList[n2])
            if(position):
                GameScript.Click(direction2)
            i=0
            
        position = GameScript.Locate(targetList[n])
        
    time.sleep(1)
    GameScript.Click(direction)


#####################卖出装备###########################
def SellEquipment():
    FindClick(17,'背包')
    position = GameScript.Locate(targetList[18])
    if(position == 0):
        FindClick(19,'全部')
    else:
        GameScript.Click(position)
    FindClick(20,'整理')
    FindClick(21,'自动选择')
    position = GameScript.Locate(targetList[22])
    if(position == 0):
        FindClick(23,'选择1')
        for i in range(26,31):
            FindClick(i,'选择')
    FindClick(24,'取消')
    FindClick(25,'出售')
    FindClick(11,'确认')
    Wait(3)
    GameScript.Click([1219,339])


###########刷9-4################################
def GameStart9_4(gameTimes = 10):
    
    gameTimes = input('输入你要刷的次数:')
    while(gameTimes.isdigit() == 0):
        print('输入非法，请重新输入')
        gameTimes = input('输入你要刷的次数:')
    gameTimes = int(gameTimes)
    
    gameCnt = 0
    print('循环',gameTimes,'次')
    Wait(3)
    while(gameCnt < gameTimes):
        ##找到9-4
        FindClick(0,'9-4')
        Wait(2)
        ##找到'选择队伍'
        FindClick(1,'选择队伍')
        Wait(2)
        ##找到'战斗开始'
            
        FindClick(2,'战斗开始')
        Wait(2)
        ##检查是否正常开始
        ###装备满了
        position = GameScript.Locate(targetList[31])
        if(position):
            print('装备已满')
            position = GameScript.Locate(targetList[33])
            GameScript.Click(position)
            SellEquipment()
            FindClick(2,'战斗开始')
            Wait(2)
        
        ##第一次路口
        CornerFindClick(5,'第一个路口',south)
        ##第二次路口
        CornerFindClick(6,'第二个路口',west,   5,south)
        ##第三次路口
        CornerFindClick(7,'第三个路口',south,  6,west)
        ##第四次路口
        CornerFindClick(8,'第四个路口',west,   7,south)
        ##BOSS房1 
        CornerFindClick(9,'BOSS房1',mapPosition,  8,west)
        Wait(2)
        GameScript.LButtonDownMoveUP([420,300],[350,450])
        GameScript.Click([722,55])
        #找到确认
        FindClick(11,'确认')
        ##移动到下一个BOSS房
        CornerFindClick(12,'BOSS房2',west)
        ##第五次路口
        CornerFindClick(13,'第五个路口',north,   12,west)
        ##第六次路口
        CornerFindClick(14,'第六个路口',mapPosition,  13,north)
        ##找到出口
        FindClick(15,'出口')
        #找到确认
        FindClick(11,'确认')
        #找到下一个BOSS房
        CornerFindClick(12,'BOSS房2',middle)
        #找到探险结束
        FindClick(10,'探险结束')
        Wait(3)
        GameScript.Click([1174,476])
        GameScript.Click([1174,476])
        ##找到确认
        FindClick(16,'确认')
        gameCnt = gameCnt+1
        print('结束，3秒后重新开始，当前完成数：',gameCnt)
        Wait(3)

##################界面#####
def Menu():
    print('----------------------------------')
    print('|功能1：自动刷9-4  GameStart9_4()|')
    print('----------------------------------')
    print('|功能2：正在开发...              |')
    print('----------------------------------')
    print('| ↓↓请输入相应的功能编号↓↓   |')
    if(input() =='1'):
        print('开始自动刷9-4,请先自行打开9-4地图界面')
        GameStart9_4()
    else:
        print('非法输入')
        Menu()
##############
Menu()
