import requests
import json
import threading
from threading import Thread
from .Progress import show_progress
def run_bot(api_data,url1):
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = url1, data = json.dumps(api_data), headers=headers,timeout=5)
    res=json.loads(res.text)
    return res
def run_the_bot(api_data,url1,user,bot,indexnumber,callback_func):
    print("Starting...")
    already_runing=False
    try:
        res=run_bot(api_data,url1)
        try:
            if("Already Runing" in res["errors"]):
                already_runing=True
        except:
            pass
    except:
        pass
    if(already_runing==False):
        Thread(target = show_progress,args=(user,bot,indexnumber,url1,callback_func,)).start()
    else:
        callback_func({"status":False,"errors":["Already Runing"],"body":{}})