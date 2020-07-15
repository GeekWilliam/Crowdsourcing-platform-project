from flask import Flask
from flask_script import Manager   # 启动命令的管理类
from flask import request
from flask_cors import CORS
from Class_dome import Request_results
from pymongo import MongoClient#必要数据库第方三库
import re

#创建启动服务对象
app=Flask(__name__)
# 创建Manager管理类的
manager=Manager(app)

#暂停接口设置
@app.route('/statr_end/SE=<SE>')

#接口函数
def statr_end(SE):
    if len(re.compile('[01]').findall(SE))!=1:
        return Request_results.code_1()
    client = MongoClient()
    db=client['sands']
    sands_collection= db['start_end']
    ls=[{'id':1}]
    
    if client['sands']['start_end'].find().count()==0:#判断有没有插入数据
        if int(SE)==0:
            sands_collection.insert_many(ls)#插入数据
            return {"Message":"success stop","code":"0"}
        else:
            return Request_results.code_1()
    else:
        if int(SE)==1:
            client['sands']['start_end'].drop()#删除数据
            return {"Message":"success statr","code":"1"}
        else:
            return Request_results.code_1()
        

if __name__ == '__main__':
    '''启动接口代码python Statr_end_API.py runserver -h 127.16.23.34 -p 5000 -d
        启动路径为当前文件下，若端口5000被占用请修改
    '''
    #设置跨域
    CORS(app,supports_credentials=True)
    #ASCII设置不默认转换成ASCII码
    app.config['JSON_AS_ASCII'] = False
    #启动服务
    manager.run()