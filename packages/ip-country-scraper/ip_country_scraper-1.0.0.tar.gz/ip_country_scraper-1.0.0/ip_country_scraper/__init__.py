from datakund_cloud import *
def getargs(argss,kwargs):
    args={}
    i=0
    for a in argss:
        args[str(i)]=a
        i=i+1
    args.update(kwargs)
    if("apiKey" not in args):
        if(len(argss)>0):
            args["apiKey"]=argss[0]
    return args
def set_api_key(*argss,**kwargs):
    args=getargs(argss,kwargs)
    if("apiKey" not in args):
        print("Please set a valid API Key")
        return None
    key=args["apiKey"]
    dk=datakund_cloud.set_api_key(apiKey=key)
    return dk