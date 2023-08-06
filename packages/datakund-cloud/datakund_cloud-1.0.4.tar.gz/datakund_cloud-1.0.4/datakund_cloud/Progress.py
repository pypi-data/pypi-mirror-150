from tqdm import tqdm
import requests
import time
import json
global progress_dict
progress_dict={}
def fetch_progress(user,bot,indexnumber,api,i):
    global progress_dict
    data={"user":user,"bot":bot,"indexnumber":indexnumber,"api_name":"fetchbotprogress"}
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = api, data = json.dumps(data), headers=headers)
    res=res.text
    res=json.loads(res)
    progress_dict[user+bot+str(indexnumber)]=res
    prog=int(res["progress"])
    if(i==0 and str(prog)=="100"):
        prog=5
    return prog
def get_progress_dict(user,bot,indexnumber):
    try:
        prog_dict=progress_dict[user+bot+str(indexnumber)]
    except:
        prog_dict={}
    return prog_dict
def get_bot_response(user,bot,indexnumber,api):
    data={"user":user,"bot":bot,"indexnumber":indexnumber,"api_name":"getresponse"}
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = api, data = json.dumps(data), headers=headers)
    res=res.text
    res=json.loads(res)
    return res
def show_progress(user,bot,indexnumber,api,callback_func):
    prog=5
    last=5
    i=0
    with tqdm(total=200, desc="Progress") as progress:
        progress.update(10)
        while(prog!=100):
            last=prog
            prog=fetch_progress(user,bot,indexnumber,api,i)
            time.sleep(2)
            if(prog==0 or prog<=5):
                pass
            else:
                final=prog-last
                progress.update(final+final)
            if(prog==100):
                break
            i=i+1
    progress.close()
    if(callback_func!=None):
        time.sleep(2)
        response=get_bot_response(user,bot,indexnumber,api)
        callback_func(response)