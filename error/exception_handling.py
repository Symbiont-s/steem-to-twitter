# Standar library
from datetime           import datetime, timezone
import traceback
# Third party library
from tinydb             import TinyDB

error = TinyDB("error/exceptions.json")

def exception_handling(e,funcion,dict_exceptions):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if e is not None:
        if str(e) in dict_exceptions.keys():
            if dict_exceptions[str(e)] !="":
                print(dict_exceptions[str(e)])
        else:
            print("Error: %s"%(str(e)))
            error.insert({'name':funcion, 'date':str(now) ,'error':str(e),'traceback':str(traceback.format_exc())})
    else:
        print("Error")
        error.insert({'name':funcion, 'date':str(now) ,'error':"empty",'traceback':str(traceback.format_exc())})
