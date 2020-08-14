'''在线网页爬虫接口1.0v 编写者:William Lincoln
   未经本人允许不得商用,个人主页https://github.com/GeekWilliam
'''
#导包
from flask import Flask,request,make_response,session
from Class_dome import Request_results
from flask_script import Manager   # 启动命令的管理类
from flask_cors import CORS
import json
import time
import re
#必要的爬虫导包以及数据库导包
import requests
from scrapy.selector import Selector
import urllib.request as r
from pymongo import MongoClient

#创建启动服务对象
app = Flask(__name__)
# 创建Manager管理类的
manager = Manager(app)

#设置爬虫接口
@app.route('/index',methods=['post'])

#接口函数，POST请求
def index():
    if  not request.data:   #检测是否有数据
        return Request_results.code_1()

    #检测数据是否符合要求
    data_ditc=json.loads(request.data)
    if re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['time1'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['home_page'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['trailer_page'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['Starting_number'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['End_number'])==0:
        return Request_results.code_1()

    #参数赋值
    time1=int(data_ditc['time1'])
    home_page=int(data_ditc['home_page'])
    trailer_page=int(data_ditc['trailer_page'])
    Starting_number=int(data_ditc['Starting_number'])
    End_number=int(data_ditc['End_number'])
    #任务模型
    Bidding_task=int(data_ditc['Bidding_task'])
    Employment_task=int(data_ditc['Employment_task'])
    #任务赏金是否托管
    Bounty_trust=int(data_ditc['Bounty_trust'])
    #任务时间
    Mission_time=int(data_ditc['Mission_time'])

    #原始参数
    url_data1='https://task.epwk.com/develop/'
    #参数判断
    #招标任务判断
    if Bidding_task==1:
        url_data1+='m4/'
    else:
        pass

    #雇佣任务判断
    if Employment_task==1:
        url_data1+='m5/'
    else:
        pass
    
    #判断赏金是否托管
    if Bounty_trust==1:#赏金未托管
        url_data1+='tn/'
    elif Bounty_trust==2:#赏金以托管
        url_data1+='t1/'
    else:
        pass
    
    # #任务时间
    if Mission_time==1:#一周到期
        url_data1+='e1/'
    elif Mission_time==2:#三天到期
        url_data1+='e2/'
    elif Mission_time==3:#两天到期
        url_data1+='e3/'
    else:
        pass

    #任务时间&赏金是否托管
    if Mission_time==4 and Bounty_trust==3:#一周到期，赏金未托管
        url_data1+='tne1/'
    elif Mission_time==5 and Bounty_trust==3:#三天到期，赏金未托管
        url_data1+='tne2/'
    elif Mission_time==6 and Bounty_trust==3:#两天到期，赏金未托管
        url_data1+='tne3/'
    elif Mission_time==4 and Bounty_trust==4:#一周到期，赏金以托管
        url_data1+='t1e1/'
    elif Mission_time==5 and Bounty_trust==4:#三天到期，赏金以托管
        url_data1+='t1e2/'
    elif Mission_time==6 and Bounty_trust==4:#两天到期，赏金以托管
        url_data1+='t1e3/'
    else:
        pass

    #更新url
    url_data2=url_data1+'page{}.html'


    #检测是否符合设置要求
    if int(time1)>86400:
        return Request_results.code_1()
    if int(home_page)<=1279:
        if int(home_page)>int(trailer_page):
            return Request_results.code_1()
    if int(home_page)==0:
        return Request_results.code_1()
    if int(Starting_number)<=39:
        if int(Starting_number)>int(End_number):
            return Request_results.code_1()
    if int(Starting_number)==0:
        return Request_results.code_1()

    #倒计时设置
    time.sleep(int(time1))


    #变量设置
    dict1={}
    dict2={}
    client = MongoClient()
    Number=0
    ls=[]
    db=client['temporary_data']
    crawling_data_collection= db['crawling_data']
    client['sands']['start_end'].drop()

    #爬取代码块
    try:
        for i in range(int(home_page),int(trailer_page)+1):
            url=url_data2.format(i)
            req=r.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})
            data=r.urlopen(req).read().decode('utf-8','ignore')
            selector=Selector(text=data)
            for k in range(int(Starting_number),int(End_number)+1):
                #暂停设置，根据数据库内容有无确定
                while True:
                    if int(client['sands']['start_end'].find().count())==0:
                        break
                    else:
                        continue
                zbjg='/html/body/div[10]/div[1]/div[2]/div[4]/div[{}]/div[1]/h3/b'.format(k)#招标价格
                zbrs='/html/body/div[10]/div[1]/div[2]/div[4]/div[{}]/div[1]/samp'.format(k)#招标人数
                zbrw='/html/body/div[10]/div[1]/div[2]/div[4]/div[{}]/div[2]/em'.format(k)#招标任务
                zbzt='/html/body/div[10]/div[1]/div[2]/div[4]/div[{}]/div[2]/span'.format(k)#招标状态
                zbbt='/html/body/div[10]/div[1]/div[2]/div[4]/div[{}]/div[1]/h3/a'.format(k)#招标标题
                
                zb_Price=selector.xpath(zbjg).xpath('string(.)').extract()[0].replace('\xa0','')#招标价格
                zb_people=selector.xpath(zbrs).xpath('string(.)').extract()[0].replace(' ','')#招标人数
                zb_task=selector.xpath(zbrw).xpath('string(.)').extract()[0]#招标任务
                zb_state=selector.xpath(zbzt).xpath('string(.)').extract()[0].replace(' ','').replace('\n','').replace('\t','').replace('\xa0','').replace('xa0','').replace('xa09','')#招标状态
                zb_title=selector.xpath(zbbt).xpath('string(.)').extract()[0].replace('\n','').replace('\t','').replace(' ','')#招标标题
                
                dict1[str(Number)]={'id':Number,'zb_title':zb_title,'zb_Price':zb_Price,'zb_people':zb_people,'zb_task':zb_task,'zb_state':zb_state}
                ls.append({'id':Number,'zb_title':zb_title,'zb_Price':zb_Price,'zb_people':zb_people,'zb_task':zb_task,'zb_state':zb_state})
                Number+=1
                if len(dict1)!=1:
                    dict1['length']=int(len(dict1)-1)
                else:
                    dict1['length']=int(len(dict1))
                dict2['data']=dict1
                dict2['Message']=("成功采集{}条数据".format(len(dict1)-1))
    except Exception as err:
        pass
    if len(dict1)==0:
        dict1[str(0)]={'id':0,'zb_title':"未查询到",'zb_Price':"未查询到",'zb_people':"未查询到",'zb_task':"未查询到",'zb_state':"未查询到"}
        dict1['length']=int(len(dict1))
        dict2['data']=dict1
        dict2['Message']=("成功采集{}条数据".format(0))
        return dict2
    else: 
        pass
    
    #写入数据库，不能使用文件操作，会使网页刷新
    crawling_data_collection.insert_many(ls)
    return dict2

@app.route('/index1',methods=['post'])

#接口函数，POST请求
def index1():
    if  not request.data:   #检测是否有数据
        return Request_results.code_1()
    
    #检测数据是否符合要求
    data_ditc=json.loads(request.data)
    if re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['time1'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['home_page'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['trailer_page'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['Starting_number'])==0 or re.compile('^\d{0,5}[0-9-]$').findall(data_ditc['End_number'])==0:
        return Request_results.code_1()
    
    #参数赋值
    time1=int(data_ditc['time1'])
    home_page=int(data_ditc['home_page'])
    trailer_page=int(data_ditc['trailer_page'])
    Starting_number=int(data_ditc['Starting_number'])
    End_number=int(data_ditc['End_number'])
    #到期时间 dt=
    Due_date=int(data_ditc['Due_date'])
    #交易模式 m=
    Trading_model=int(data_ditc['Trading_model'])
    #投标状态 bs=
    Tender_status=int(data_ditc['Tender_status'])
    #托管状态 s=
    Hosting_status=int(data_ditc['Hosting_status'])
    #原始url
    url_data1='https://task.zbj.com/t-rjkf/page{}.html?'
    
    #参数判断
    #判断交易模式参数
    if Trading_model==1111:#招标
        url_data1+='m=1111'
            #判断托管状态参数
        if Hosting_status==1:#已托管
            url_data1+='&s=1'
        elif Hosting_status==2:#未托管
            url_data1+='&s=2'
        else:
            pass
        if Tender_status==1:#0人投标
            url_data1+='&bs=1'
        elif Tender_status==2:#1-3人投标
            url_data1+='&bs=2'
        elif Tender_status==3:#4-6人投标
            url_data1+='&bs=3'
        elif Tender_status==4:#6人以上
            url_data1+='&bs=4'
        else:
            pass
    elif Trading_model==2:#比稿
        url_data1+='m=2'
    else:
        pass
    
    #判断托管状态参数
    if Hosting_status==3:#已托管
        url_data1+='&s=1'
    elif Hosting_status==4:#未托管
        url_data1+='&s=2'
    else:
        pass

    #判断到期时间参数
    if  Due_date==2:#1天内到期
        url_data1+='&dt=2'
    elif Due_date==3:#3天内到期
        url_data1+='&dt=3'
    elif Due_date==4:#7天内到期
        url_data1+='&dt=4'
    else:
        pass

    #倒计时设置
    time.sleep(int(time1))

    #变量设置
    dict1={}
    dict2={}
    client = MongoClient()
    Number=0
    ls=[]
    db=client['temporary_data']
    crawling_data_collection= db['crawling_data']
    client['sands']['start_end'].drop()
    
    #爬虫
    try:
        for i in range(int(home_page),int(trailer_page)+1):
            url=url_data1.format(i)
            req=r.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'})
            data=r.urlopen(req).read().decode('utf-8','ignore')
            selector=Selector(text=data)
            for k in range(int(Starting_number),int(End_number)+1):
                #暂停设置，根据数据库内容有无确定
                while True:
                    if int(client['sands']['start_end'].find().count())==0:
                        break
                    else:
                        continue
                task_title=selector.xpath('//*[@id="utopia_widget_8"]/div[1]/div[{}]/div[2]/div[1]/div/span[1]/a'.format(k)).xpath('string(.)').extract()[0]
                task_price_status=selector.xpath('//*[@id="utopia_widget_8"]/div[1]/div[{}]/div[2]/div[2]'.format(k)).xpath('string(.)').extract()[0].replace('\n','')
                task_release_time=selector.xpath('//*[@id="utopia_widget_8"]/div[1]/div[{}]/div[1]/span[1]'.format(k)).xpath('string(.)').extract()[0].replace('\n','')
                task_type=selector.xpath('//*[@id="utopia_widget_8"]/div[1]/div[{}]/div[2]/div[1]/div/span[3]/i'.format(k)).xpath('string(.)').extract()[0].replace('\n','')
                task_quota=selector.xpath('//*[@id="utopia_widget_8"]/div[1]/div[{}]/div[1]/span[2]'.format(k)).xpath('string(.)').extract()[0].replace('\n','')
                dict1[str(Number)]={'id':Number,"task_title":task_title,"task_price_status":task_price_status,"task_release_time":task_release_time,"task_type":task_type,"task_quota":task_quota}
                ls.append({'id':Number,"task_title":task_title,"task_price_status":task_price_status,"task_release_time":task_release_time,"task_type":task_type,"task_quota":task_quota})
                Number+=1
                if len(dict1)!=1:
                    dict1['length']=int(len(dict1)-1)
                else:
                    dict1['length']=int(len(dict1))
                dict2['data']=dict1
                dict2['Message']=("成功采集{}条数据".format(len(dict1)-1))
    except Exception as err:
        pass
    if len(dict1)==0:
        dict1[str(0)]={'id':0,'task_title':"未查询到",'task_price_status':"未查询到",'task_release_time':"未查询到",'task_type':"未查询到",'task_quota':"未查询到"}
        dict1['length']=int(len(dict1))
        dict2['data']=dict1
        dict2['Message']=("成功采集{}条数据".format(0))
        return dict2
    else: 
        pass
    
    #写入数据库，不能使用文件操作，会使网页刷新
    crawling_data_collection.insert_many(ls)
    return dict2


#设置删除临时数据接口
@app.route('/del_data')

#接口函数
def del_data():
    from pymongo import MongoClient
    client = MongoClient()#启动数据库
    db=client['temporary_data']
    crawling_data_collection= db['crawling_data']
    client['temporary_data']['crawling_data'].drop()
    return Request_results.code0()

#设置查询数据接口
@app.route('/indexdata/num=<num>')

#接口函数
def indexdata(num):
    if  len(re.compile('^\d{0,5}[0-9]$').findall(num))==1:#判断参数是否符合要求
        try:
            from pymongo import MongoClient
            client = MongoClient()#启动数据库
            db=client['temporary_data']
            crawling_data_collection= db['crawling_data']
            detailed_data=list(crawling_data_collection.find({"id":int(num)}))[0]
            del(detailed_data['_id'])
            return dict(detailed_data)
        except Exception as err:
            return {"code":"-1","message":"Data does not exist"}
    else:
        return Request_results.code_1()

if __name__ == '__main__':
    '''启动接口代码python demo.py runserver -h 127.16.23.34 -p 5000 -d
        启动路径为当前文件下，若端口5000被占用请修改
    '''
    #设置跨域
    CORS(app,supports_credentials=True)
    #ASCII设置不默认转换成ASCII码
    app.config['JSON_AS_ASCII'] = False
    #启动服务
    manager.run()
