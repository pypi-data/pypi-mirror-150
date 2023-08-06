import requests
import json
import os
import inspect
from .Progress import show_progress
from .GetAttributes import make_a_empty_class
import threading
global global_user,serverurl
global_user=""
serverurl="http://44.204.51.55:5350"
def changebotname(bot):
    prev=''
    newname=''
    for char in bot:
        if(prev=='_'):
            newname=newname+char.upper()
        else:
            newname=newname+char
        prev=char
    first=newname[0].upper()
    newname=newname[1:]
    newname=first+newname
    return newname
def getargs(argss,kwargs,api):
    if(api=="datakund" and len(argss)>0):
        args=list(argss)
        return args
    args={}
    i=0
    for a in argss:
        args[str(i)]=a
        i=i+1
    args.update(kwargs)
    return args
def fetch_the_response(name,res,user,bot,indexnumber,serverurl):
    res=make_a_empty_class(name,res,user,bot,indexnumber,serverurl)
    return res
def modify_res(res,bot_name):
    resume_dict={}
    res_copy=res.copy()
    for bot in res_copy:
        if(bot not in ["body","errors","success_score"]):
            try:
                resume_dict[bot]=res[bot]["resume_variable"]
                del res[bot]["resume_variable"]
            except:
                pass
        elif(bot=="resume_variable"):
            resume_dict[bot_name]=res[bot]
            del res[bot]
    res["resume_dict"]=resume_dict
    return res
class datakund_cloud():
    def __init__(self):
        global global_user
    def set_api_key(key):
        global global_user
        self.user=key
        global_user=key
    def __getattr__(self, name):
        def startbrowser(self,browseroptions):
            return 0
        def method(*argss,**kwargs):
            args=getargs(argss,kwargs,"")
            def callthefunction(self,index,name,args,bot):
                global serverurl
                if(name=="quit"):
                    try:
                        requests.get(serverurl+"quitdatakund")
                    except:
                        pass
                    os._exit(0)
                    return None
                url=serverurl+name
                headers = {'Content-type': 'application/json'}
                args['indexnumber']=index
                args['bot']=bot
                args['user']=self.user
                args["tech_type"]="PIP"
                res=requests.post(url = url, data = json.dumps(args), headers=headers)
                try:
                    res=json.loads(res.text)
                except:
                    res=res.text
                return res
            def set_browser_index(self,*argss,**kwargs):
                return 
            def __getattrr__(self, name):
                indexname=self.index
                print("here")
                def method(*argss,**kwargs):
                    if(name in ["end","get_snapshot","get_page_title","get_page_source","get_current_url","reload","keypress","open","scroll","getresponse","send_feedback","quit","refresh"]):
                        args=getargs(argss,kwargs,"")
                        method=callthefunction(self,indexname,name,args,'')
                    else:
                        args=getargs(argss,kwargs,"datakund")
                        domainname=self.domain
                        bot=bot
                        if("apiKey" in args or self.private_bot==True):
                            pass
                        else:
                            bot=bot+"~D75HsPTUIeOmN0bLp5ulrwB7F1f2"
                        def runbot(bot,outputdata):
                            global global_user ,serverurl
                            current_user=self.user
                            url1=serverurl+"run"
                            headers = {'Content-type': 'application/json'}
                            try:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"fields":outputdata["fields"],"tech_type":"PIP"}
                            except:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"tech_type":"PIP"}
                            if("apiKey" in outputdata):
                                current_user=outputdata["apiKey"]
                                api_data["user"]=outputdata["apiKey"]
                                api_data["privatebot"]=True
                            if(self.private_bot==True):
                                api_data["privatebot"]=True
                            if("data_format" in outputdata):
                                api_data["data_format"]=outputdata["data_format"]
                            if("resume_dict" in outputdata):
                                api_data["resume_dict"]=outputdata["resume_dict"]
                            #start_time = threading.Timer(3,show_progress, args=(current_user,bot,self.index,serverurl+"fetchbotprogress",))
                            #start_time.start()
                            res=requests.post(url = url1, data = json.dumps(api_data), headers=headers)
                            res=json.loads(res.text)
                            self.bot=bot
                            try:
                                self.body=res['body']
                            except:
                                self.body={}
                            try:
                                self.score=res['score']
                            except:
                                self.score=bot
                            try:
                                self.errors=res['errors']
                            except:
                                self.errors=[]
                            res=modify_res(res,bot)
                            return res
                        method=runbot(bot,args)
                    return method
                return method
            dynamicclass = type(name, 
              (), 
              { 
               "__init__": set_browser_index,
               "__getattr__":__getattrr__})
            obj1=dynamicclass(*argss,**kwargs)
            return obj1
        return method