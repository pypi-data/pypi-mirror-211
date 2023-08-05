from abc import ABC, abstractmethod
import datetime
from ClientSocketControl.SocketClient import SocketClient
from ClientSocketControl.DataStructure import DataStructure
from TradeControl.OrderActionConstants.Action import Action
from TradeControl.TradeController import TradeController

import json

class MainController(ABC):
    
    dataStreaming = None
    dataStreamingRequest = None
    tradeController = None
    
    def login(self, loginname, password):
        try:
            self.dataStreaming = SocketClient(loginname, password)
        except:
            self.dataStreaming = None
            raise Exception("Login fail")
    
    def createDataStreamingRequest(self, activity:str, market:str, index:str, startdate:datetime, enddate:datetime, starttime:datetime, endtime:datetime, interval:int):
        if(self.dataStreaming is None):
            raise Exception("Please login first");
        else:
            try:
                datetime.datetime(int(startdate.strftime('%Y')),int(startdate.strftime('%m')),int(startdate.strftime('%d')))
            except ValueError:
                raise Exception("startdate invaild")
            try:
                datetime.datetime(int(enddate.strftime('%Y')),int(enddate.strftime('%m')),int(enddate.strftime('%d')))
            except ValueError:
                raise Exception("enddate invaild")
            try:
                datetime.datetime(int(starttime.strftime('%H')),int(starttime.strftime('%M')),int(starttime.strftime('%S')))
            except ValueError:
                raise Exception("starttime invaild")
            try:
                datetime.datetime(int(endtime.strftime('%H')),int(endtime.strftime('%M')),int(endtime.strftime('%S')))
            except ValueError:
                raise Exception("endtime invaild")
            dataStreamingRequest = {
                "activity":activity,
                "market":market,
                "index":index,
                "startdate":startdate.strftime('%Y%m%d'),
                "enddate":enddate.strftime('%Y%m%d'),
                "starttime":starttime.strftime('%H%M%S'),
                "endtime":endtime.strftime('%H%M%S'),
                "interval":int(interval),
            }
            self.dataStreaming.request(dataStreamingRequest)
            
    def projectBTradeController(slippageRangeInPercentage):
        tradeController = TradeController()
        tradeController.setSlippage(0.0005)
    
    @abstractmethod
    def logicHandler(datastructure:DataStructure):
        pass
        
    def run(self):
        while True:
            #get the response
            response = self.dataStreaming.getResponse()
            if response:
                #Convert response JSON message to Python dictionary
                dataStructure_dict = json.loads(response)
                dataStructure = DataStructure(**dataStructure_dict)
                
                #Check response finished or not
                if dataStructure.done:
                    break
                
                #Check error caused or not
                if dataStructure.error:
                    print(dataStructure.error)
                    break
                
                #check the order allow to trade or not
                self.tradeController.tradeCheckingAndBalanceUpdate(dataStructure)
                
                '''
                You may write your back test program below within the while loop
                >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                '''
                
                self.logicHandler(dataStructure);
                
                '''
                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                '''
    
