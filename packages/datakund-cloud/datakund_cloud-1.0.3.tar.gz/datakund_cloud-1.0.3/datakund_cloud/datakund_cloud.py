import requests
import json
import os
import inspect
from .RunBot import run_the_bot
global global_user,serverurl
global_user=""
serverurl="https://un8qsuz159.execute-api.us-east-2.amazonaws.com/default/run_bot_on_cloud"
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
    callback_func=None
    if("callback" in kwargs):
        callback_func=kwargs["callback"]
        del kwargs["callback"]
    args.update(kwargs)
    if("apiKey"==api and "apiKey" not in args):
        if(len(argss)>0):
            args["apiKey"]=argss[0]
    return args,callback_func

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
def check_valid_user(key):
    is_user=False
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = serverurl, data = json.dumps({"api_name":"verifyuser","user":key}), headers=headers)
    try:
        res=json.loads(res.text)
    except:
        res=res.text
    if(res["status"]==True):
        is_user=True
    return is_user
class datakund_cloud():
    def __init__(self):
        global global_user
    def __getattr__(self, name):
        def method(*argss,**kwargs):
            args,cb=getargs(argss,kwargs,"")
            def callthefunction(self,index,name,args,bot):
                global serverurl
                headers = {'Content-type': 'application/json'}
                args['indexnumber']=index
                args['bot']=bot
                args['user']=self.user
                args["tech_type"]="PIP"
                args["api_name"]=name
                res=requests.post(url = serverurl, data = json.dumps(args), headers=headers)
                try:
                    res=json.loads(res.text)
                except:
                    res=res.text
                return res
            def set_api_key_user(self,key):
                global global_user
                is_user=check_valid_user(key)
                if(is_user==True):
                    self.user=key
                    global_user=key
            def set_browser_index(self,*argss,**kwargs):
                global global_user
                argums,cb=getargs(argss,kwargs,"apiKey")
                self.index=0
                self.domain=name
                self.user=global_user
                self.private_bot=False
                if(name=="set_api_key"):
                    if("apiKey" not in argums):
                        print("Please set API Key first")
                    else:
                        set_api_key_user(self,argums["apiKey"])
            def stop_the_bot():
                global global_user
                headers = {'Content-type': 'application/json'}
                send_data={}
                send_data['user']=global_user
                send_data["tech_type"]="PIP"
                send_data["api_name"]="stop"
                res=requests.post(url = serverurl, data = json.dumps(send_data), headers=headers)
                try:
                    res=json.loads(res.text)
                except:
                    res=res.text
                return res
            def __getattrr__(self, name):
                indexname=self.index
                def method(*argss,**kwargs):
                    if(name in ["end","get_snapshot","get_page_title","get_page_source","get_current_url","reload","keypress","open","scroll","getresponse","send_feedback","quit","refresh"]):
                        args,callback_func=getargs(argss,kwargs,"")
                        method=callthefunction(self,indexname,name,args,'')
                    elif(name in ["click","find_element","find_elements","send_keys","wait_for_element"]):
                        args,callback_func=getargs(argss,kwargs,"")
                        method=call_element_functions(self,indexname,name,args)
                    elif(name in ["stop"]):
                        if(global_user==""):
                            print("Please set a valid api key first")
                            return None
                        method=stop_the_bot()
                    else:
                        if(global_user==""):
                            print("Please set a valid api key first")
                            return None
                        args,callback_func=getargs(argss,kwargs,"datakund")
                        domainname=self.domain
                        bot=name
                        if(domainname=="" or domainname=="new" or domainname=="set_api_key"):
                            bot=bot
                        else:
                            bot=domainname+"_"+bot
                        if("apiKey" in args or self.private_bot==True):
                            pass
                        else:
                            bot=bot+"~D75HsPTUIeOmN0bLp5ulrwB7F1f2"
                        def runbot(bot,outputdata,callback_func):
                            global global_user ,serverurl
                            current_user=global_user
                            url1=serverurl
                            try:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"fields":outputdata["fields"],"tech_type":"PIPCLOUD","api_name":"run"}
                            except:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"tech_type":"PIPCLOUD","api_name":"run"}
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
                            api_data["publicbot"]=True
                            api_data["run_type"]="simple"
                            run_the_bot(api_data,url1,current_user,bot,self.index,callback_func)
                        method=runbot(bot,args,callback_func)
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