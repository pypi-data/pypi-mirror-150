from MtySdk import *

USERNAME    =   "请输入你的账号"
PASSWORD    =   "请输入你的密码"

# 注册信息模型
auth = MtyAuth(USERNAME,PASSWORD)
# 声明数据操作工具
mty2Api = Mty2Api(auth);

# 目标品种
symbolnames  = ["CZCE.CF107","CZCE.CF107P12600"]
# 时间颗粒度  mty2Api.FIVE_MINUTE： 5分钟，  mty2Api.SIXTY_MINUTE： 整点
timeStepSize = mty2Api.SIXTY_MINUTE;

# 数据时间段
starttime    =  "2020-10-09 09:00:00"
endtime      =  "2020-10-12 09:00:00"

# 数据挂载数据工厂
mty2Api.initmath(symbolnames=symbolnames , starttime=starttime , endtime=endtime ,timeStepSize=timeStepSize);

# 消费数据
while mty2Api.ishaving():
    # 获取下一条数据的时间间隔 ， 秒为单位
    item = mty2Api.getmath(None);
    print(item)