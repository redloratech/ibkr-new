from ast import arg
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import logging
from threading import Thread

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
    
class ApiWrapper(EClient,EWrapper,metaclass=Singleton):
    response = None
    def enter_exit_info(func):
        def wrapper(self, *arg, **kw):
            if not self.isConnected():
                logger.warning("Not connected")
                logger.warning("Connecting...")
                self.start_client()
                res = func(self, *arg, **kw)
            else:
                logger.warning("session connected...")
                res = func(self, *arg, **kw)
                self.disconnect()
                
                
            
            
            return res

        return wrapper
    
    
    def start_client(self):
        self.connect(port=4002,host="127.0.0.1",clientId=233)
        self.runner = Thread(target=self.run,daemon=True)
        self.runner.start()
        
    def stop_client(self):
        self.disconnect()
        self.runner.join()
        
    def __init__(self,queue):
        self.queue = queue
        EClient.__init__(self,self)
        
    @enter_exit_info
    def reqAccountSummary(self, reqId, groupName, tags):
        super().reqAccountSummary(reqId, groupName, tags)
        
    @enter_exit_info
    def accountSummary(self, *args):
        # print(f"reqId:{reqId} \n account:{account} \n tag:{tag} \n value:{value} \n currency:{currency}")
        # self.response['message'] = f"reqId:{reqId} \n account:{account} \n tag:{tag} \n value:{value} \n currency:{currency}"
        self.response = args
        print(args)
        # logger.warning("session Exit...")
        
        
        
        


    
        