# -*- coding: utf-8 -*-
__author__ = 'jiangzhx'
__weibo__ = "@核桃过敏患者"
import httplib,urlparse,hashlib,json,datetime,types


class getui(object):
    def __init__(self,appkey,mastersecret,appid,api="http://sdk.open.api.igexin.com/service"):
        pr = urlparse.urlparse(api)
        self.domain = pr.netloc
        self.endpoint = pr.path
        self.appkey=appkey
        self.mastersecret=mastersecret
        self.appid=appid

    def pushMessage(self,data,clientid,expire=3600):

        ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args = {
            'action': 'pushmessage',
            'appid':self.appid,
            'appkey': self.appkey,
            'clientid': clientid,
            'data': data,
            'time':ctime,
            'expire':expire,
            'appid':self.appid
        }
        args['sign']=self.sign(args)

        return self.post(args)

    def pushSpecifyMessage(self,appname,title,content,clientid,offline=True,offlineTime=72,priority=1, \
                           notifyMsgIcon="icon.png",notifyMsgNoRing=False,notifyMsgNoVibrate=False,\
                            pushType='NotifyMsg',transmissionType=1,transmissionContent=""):
        if type(clientid)!=types.ListType:
            clientid=[clientid,]

        notifyMsg = {
            'notifyMsgIcon':notifyMsgIcon,
            'notifyMsgTitle':title,
            'notifyMsgContent':content,
            'transmissionContent':transmissionContent,
            'transmissionType':transmissionType,
            'notifyMsgNoRing':notifyMsgNoRing,
            'notifyMsgNoVibrate':notifyMsgNoVibrate,
            }

        args = {
            'action': "pushSpecifyMessage",
            'appkey': self.appkey ,
            'type': 2 ,
            'pushTitle':appname,
            'pushType': pushType,
            'offline': offline,
            'offlineTime':offlineTime,
            'priority': priority,
            'tokenMD5List': clientid,
            'msg':notifyMsg,
            }
        args['sign']=self.sign(args)

        return self.post(args)

    #####尚未完成全局发送#######
    '''
    def pushGroupMessage(self,appname,title,content,clientid,offline=True,offlineTime=72,priority=1,\
                           notifyMsgIcon="",notifyMsgNoRing=False,notifyMsgNoVibrate=False,\
                           pushType='NotifyMsg',transmissionType=1,transmissionContent=""):
        if type(clientid)!=types.ListType:
            clientid=[clientid,]

        notifyMsg = {
            'notifyMsgIcon':"icon.png",
            'notifyMsgTitle':title,
            'notifyMsgContent':content,
            'transmissionContent':transmissionContent,
            'transmissionType':transmissionType,
            'notifyMsgNoRing':notifyMsgNoRing,
            'notifyMsgNoVibrate':notifyMsgNoVibrate,
            }

        args = {
            'action': "pushGroupMessage",
            'appkey': self.appkey ,
            'type': 2 ,
            'pushTitle':appname,
            'pushType': pushType,
            'offline': offline,
            'offlineTime':offlineTime,
            'priority': priority,

            'isDirected':True,
            'appIdList':[],
            'phoneTypeList':['ANDROID','SYMBIAN'],
            'provinceList':[],
            'msg':notifyMsg,
            }
        args['sign']=self.sign(args)

        return self.post(args)
    '''

    def sign(self,args):
        keys = args.keys()
        keys.sort()
        sign = ""

        for k in keys:
            if type(args[k]) in (types.UnicodeType,types.StringType,types.IntType,types.LongType):
                sign+=k+str(args[k])
        sign=self.mastersecret+sign
        sign = hashlib.md5(sign).hexdigest()
        return sign

    def post(self,args):
        conn = httplib.HTTPConnection(self.domain)
        conn.request("POST", self.endpoint, json.dumps(args))
        response = conn.getresponse()
        return response.read()



if __name__ == '__main__':
    #test config
    api="http://sdk.open.api.igexin.com/service"
    appkey="110000"
    mastersecret= "a02a76119b20d4e31620d7597a3b4f35";
    appid="b03c5cfef65ed30108f0a3fd82c3f6b4"

    #test clientid
    clientid = "ab3ca688d7c0cfe2c78f28da31c0a6ca"
    pusher = getui(appkey,mastersecret,appid)
    print pusher.pushMessage("今天天气不错啊",clientid)

    print pusher.pushSpecifyMessage("测试","哈哈","今天天气不错啊",clientid)
