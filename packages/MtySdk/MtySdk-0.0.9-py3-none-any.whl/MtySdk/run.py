from MtyApi import *
import time
import datetime

USERNAME    = "请输入你的账号"
PASSWORD    = "请输入你的密码"
SYMBOLNAME  = "CZCE.CF107"

# 注册信息模型
auth = MtyAuth(USERNAME,PASSWORD)
# 注册操作工厂
data2Api = Data2Api(auth);
# 注册一个品种的数据池
data2Api.registerData(symbolname=SYMBOLNAME);

# 在业务中快速的通过10位时间戳寻找这个时间的历史数据
for num in range(0,10):
    item = data2Api.getResiterDataByTime(1622011560)
    print(item);

# SYMBOLNAME  =   "CZCE.CF107"
# FILEPATH    =   "E://%s.csv" %SYMBOLNAME
# USERNAME    =   "username"
# PASSWORD    =   "password"
#
# # 声明数据操作工具
# data2Api = Data2Api();
#
# # B . 期货数据上传
# # 从本地csv文件加载期货数据
# mathlist = data2Api.clearMath(FILEPATH)
# # 为期货挂载手续费和保证金计算结果
# for item in mathlist:
#     item['earnestmoney']              = "请在这里填写期货保证金计算结果"
#     item['servicechargeOpenclose']       = "请在这里填写期货开仓/平昨手续费计算结果"
#     item['servicechargeClosetoday'] = "请在这里填写期货平今手续费计算结果"
#     print(item)
#
# # 上传数据到云
# uploadresult = data2Api.upload(symboname=SYMBOLNAME,username=USERNAME,password=PASSWORD,mathlist=mathlist);
# print(uploadresult)

# 使用员工账号连接系统
# api = MtyApi(auth=MtyAuth('account', 'password'))
# 按需求注册服务
# math = api.query_math('kq_m_shfe_au','2018-01-02','2018-01-04')
# print(math)

# 注册成功情况下消费服务
# while True:
#     result = api.get_math(math)
#     print(result)
#     if result is None :
#         api.close();
#         break
# from MtyApi import *
#
# #   上传文件本地地址
# filePath   = 'E:\\CZCE.CF107P12600.csv';
# #   品种名称
# sysbolname = 'CZCE.CF107P12600';
#
# #   数据清洗
# dataApi = DataApi()
# list = dataApi.clearMath(filePath)
#
# #   数据上传
# dataApi.upload(symboname=sysbolname,username='accountname',password='password',mathlist=list)