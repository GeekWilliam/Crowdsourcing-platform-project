# Reptiles_API&Statr_end_API说明  

##### 参数说明  

------
  ##### 一品威客爬取  

  ​1.time1:倒计时参数，倒计时结束自动调用API

​  2.home_page:起始页数，从多少页开始爬取

​  3.trailer_page:结束页数，从多少页结束爬取

​  4.Starting_number:起始条数，从多少条开始爬取

​  5.End_number:结束条数，从多少条结束爬取  

  6.Bidding_task:招标任务为0不添加指定字段，为1添加指定字段

  7.Employment_task:雇佣任务为0不添加指定字段，为1添加指定字段

  8.Bounty_trust:赏金是否托管,1为未托管,2为已托管

  9.Mission_time:任务时间,为1是一周到期,为2是三天到期,为3是两天到期

  10.Mission_time&Bounty_trust:任务时间参数为4、5、6赏金是否托管参数为3,爬取的数据分别为:
  一周到期，赏金未托管、三天到期，赏金未托管、两天到期，赏金未托管
  任务时间参数为4、5、6赏金是否托管参数为4,爬取的数据分别为:
  一周到期，赏金已托管、三天到期，赏金已托管、两天到期，赏金已托管

  用法:使用POST请求
      {"time1":"1",
    "home_page":"1",
    "trailer_page":"10",
    "Starting_number":"1",
    "End_number":"10",
    "Bidding_task":"0",
    "Employment_task":"0",
    "Bounty_trust":"0",
    "Mission_time":"0"}
  
  ##### 猪八戒爬取
  ​1.time1:倒计时参数，倒计时结束自动调用API

​  2.home_page:起始页数，从多少页开始爬取

​  3.trailer_page:结束页数，从多少页结束爬取

​  4.Starting_number:起始条数，从多少条开始爬取

  5.Trading_model:交易模式，为1111时是招标，为2时是比稿，为0是默认参数
  
  6.Hosting_status:托管状态，为1时是已托管，为2时是未托管，为0是默认参数

  7.Tender_status:投标状态，是交易模式子选项，为1时是0投标，为2时是1-3投标，为3时是4-6投标，为4时是6人以上，为0是默认参数

  8.Due_date:到期时间，为2时是1天内到期，为3时是3天内到期，为4时是7天内到期，为0是默认参数

  用法:使用POST请求
      {"time1":"0",
    "home_page":"1",
    "trailer_page":"1",
    "Starting_number":"1",
    "End_number":"10",
    "Trading_model":"0",
    "Hosting_status":"0",
    "Tender_status":"0",
    "Due_date":"0"}

  ##### Statr_end_API
  1.num参数,为0时暂停采集,为1时继续采集,若临时数据库没有数据,则不能暂停

  用法:http://127.16.23.35:5006/statr_end/SE=x x为0或1