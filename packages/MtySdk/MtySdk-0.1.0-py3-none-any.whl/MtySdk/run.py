from MtySdk import *

SYMBOLNAME  =   "CZCE.CF107"
FILEPATH    =   "E://%s.csv" %SYMBOLNAME
USERNAME    =   "请输入你的账号"
PASSWORD    =   "请输入你的密码"

# 注册信息模型
auth = MtyAuth(USERNAME,PASSWORD)
# 声明数据操作工具
data2Api = Data2Api(auth);

# B . 期货数据上传
# 从本地csv文件加载期货数据
mathlist = data2Api.clearMath(FILEPATH)
# 为期货挂载手续费和保证金计算结果
for item in mathlist:
    item['earnestmoney']              = "请在这里填写期货保证金计算结果"
    item['servicechargeOpenclose']  = "请在这里填写期货开仓/平昨手续费计算结果"
    item['servicechargeClosetoday'] = "请在这里填写期货平今手续费计算结果"
    print(item)

# 上传数据到云
uploadresult = data2Api.upload(symboname=SYMBOLNAME,mathlist=mathlist);
print(uploadresult)