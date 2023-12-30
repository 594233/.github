import requests,json,os

# 推送开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
# sever = os.environ["SERVE"]
sever = "on"
# 填写pushplus的sckey,不开启推送则不用填
# sckey = os.environ["SCKEY"]
sckey = "SCT219134TSgRnarsTJ3v4yvljYHdLFXLL"
# 填入glados账号对应cookie
# COOKIES = os.environ["COOKIES"]
COOKIES ="koa:sess=eyJ1c2VySWQiOjM0MDUzNiwiX2V4cGlyZSI6MTcxNzkxNzc2MjQyMywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=EBNX0uDXw_zEfGuYHZIf1QPrzVM; _gid=GA1.2.1604353738.1703939652; _gat_gtag_UA_104464600_2=1; _ga=GA1.1.812250388.1691915772; _ga_CZFVKMNT9J=GS1.1.1703939652.14.1.1703939877.0.0.0"
#COOKIES = "&&"
print(COOKIES)
cookies=COOKIES.split('&&')



def start():
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56"
    payload={
        'token': 'glados.one'
    }
    for cookie in cookies:
        checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        email = state.json()['data']['email']
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            if sever == 'on':
                requests.get('http://www.pushplus.plus/send?token=' + sckey + '&title='+mess+'&content='+email+' 剩余'+time+'天')
        else:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content='+email+'更新cookie')
     #--------------------------------------------------------------------------------------------------------#


def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()
