from abc import ABC, abstractmethod
from datetime import datetime
from ProjectB_clientside_template_package.ClientSocketControl.SocketClient import SocketClient
from ProjectB_clientside_template_package.ClientSocketControl.DataStructure import DataStructure
from ProjectB_clientside_template_package.TradeControl.OrderActionConstants.Action import Action
from ProjectB_clientside_template_package.TradeControl.TradeController import TradeController

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
    
    def createDataStreamingRequest(self, activity:str, market:str, index:str, startdate:str, enddate:str, starttime:str, endtime:str, interval:int):
        if(self.dataStreaming is None):
            raise Exception("Please login first")
        else:
            try:
                date_format = '%Y%m%d'
                datetime.strptime(startdate, date_format)
            except ValueError:
                raise Exception("startdate invaild")
            try:
                date_format = '%Y%m%d'
                datetime.strptime(enddate, date_format)
            except ValueError:
                raise Exception("enddate invaild")
            try:
                date_format = '%H%M%S'
                datetime.strptime(starttime, date_format)
            except ValueError:
                raise Exception("starttime invaild")
            try:
                date_format = '%H%M%S'
                datetime.strptime(endtime, date_format)
            except ValueError:
                raise Exception("endtime invaild")
            dataStreamingRequest = {
                "activity":activity,
                "market":market,
                "index":index,
                "startdate":startdate,
                "enddate":enddate,
                "starttime":starttime,
                "endtime":endtime,
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
                
                self.logicHandler(dataStructure)
                
                '''
                <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                '''
    
