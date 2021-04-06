# ejemplo de un timer en python con la libreria threading

import time
import threading 

INTRV = 1 # en segundos

class timerbot:
    def __init__(self):
        self.timeouts_on = []
        self.timeouts_count = []
        self.timeouts_end = []
        self.timeouts_message = []
        self.timeouts_name = []
        self.timeouts_args = []

        self.intervals_on = []
        self.intervals_count = []
        self.intervals_end = []
        self.intervals_message = []
        self.intervals_name = []
        self.intervals_args = []
        
        self.stm = 0
        self.t1 = 0
        self.t2 = 0
    
    def steamON (self,):
        self.stm = 1
        self.steam()
    def steamOFF (self):
        self.stm = 0
    def steamTOGGLE (self):
        self.stm = self.stm ^ 1
        if (self.stm == 1):
            self.steam()

    def timeout(self):
        for i in range(0,len(self.timeouts_name)):
            if(self.timeouts_on[i] == 1):
                if(self.timeouts_count[i] < self.timeouts_end[i]):
                    self.timeouts_count[i] = self.timeouts_count[i]+1
                elif (self.timeouts_count[i] == self.timeouts_end[i]):
                    self.timeouts_message[i](self.timeouts_args[i])
                    self.timeouts_count[i] = 0
                    self.timeouts_on[i] = 0
                else:
                    self.timeouts_count[i] = 0
                    self.timeouts_on[i] = 0
                    print("errno 2304 >> fallo con el timeout " + str(i))
        self.t2.cancel()
        self.t2 = threading.Timer(INTRV,self.timeout)
        self.t2.start()

    def interval(self):
        for i in range(0,len(self.intervals_name)):
            if(self.intervals_on[i] == 1):
                if(self.intervals_count[i] < self.intervals_end[i]):
                    self.intervals_count[i] = self.intervals_count[i]+1
                elif (self.intervals_count[i] == self.intervals_end[i]):
                    self.intervals_message[i](self.intervals_args[i])
                    self.intervals_count[i] = 0
                else:
                    self.intervals_count[i] = 0
                    self.intervals_on[i] = 0
                    print("errno 2305 >> fallo con el interval " + str(i))
        self.t1.cancel()
        self.t1 = threading.Timer(INTRV,self.interval)
        self.t1.start()

    def steam(self):
        self.t1 = threading.Timer(INTRV, self.interval)
        self.t2 = threading.Timer(INTRV, self.timeout)
        self.t1.start()
        self.t2.start()

    # add and remove timeouts or intervals
    def add_interval(self,time:int,functionInt,Args,name:str):
        self.intervals_message.append(functionInt)
        self.intervals_args.append(Args)
        self.intervals_name.append(name)
        self.intervals_count.append(0)
        self.intervals_end.append(time)
        self.intervals_on.append(0)

    def rem_interval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_message.pop(i)
        self.intervals_count.pop(i)
        self.intervals_name.pop(i)
        self.intervals_end.pop(i)

    def add_timeout (self,time:int,functionInt,Args,name:str):
        self.timeouts_message.append(functionInt)
        self.timeouts_args.append(Args)
        self.timeouts_count.append(0)
        self.timeouts_name.append(name)
        self.timeouts_end.append(time)
        self.timeouts_on.append(0)

    def rem_timeout (self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_message.pop(i)
        self.timeouts_count.pop(i)
        self.timeouts_name.pop(i)
        self.timeouts_end.pop(i)

    # enables, dissables and toggle count
    def enableTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_on[i] = 1

    def enableAllTimeout(self):
        for i in range(0,len(self.timeouts_on)):
            self.timeouts_on[i] = 1
    def dissableTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_on[i] = 0
    def dissableAllTimeout(self):
        for i in range(0,len(self.timeouts_on)):
            self.timeouts_on[i] = 0
    def toggleTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_on[i] = self.getTimeTimeout(name) ^ 1
    def enableInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_on[i] = 1
    def enableAllInterval(self):
        for i in range(0,len(self.timeouts_on)):
            self.intervals_on[i] = 1
    def dissableAllInterval(self):
        for i in range(0,len(self.timeouts_on)):
            self.timeouts_on[i] = 0
    def dissableInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_on[i] = 0
    def toggleInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.timeouts_on[i] = getTimeInterval(name) ^ 1

    # counts

    def clearIntervalCount(self,name):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_count[i] = 0
    def clearAllIntervalCount(self):
        for i in range(0,len(self.intervals_count)):
            self.intervals_count[i] = 0
    def clearTimeoutCount(self,name):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_count[i] = 0
    def clearAllTimeoutCount(self):
        for i in range(0,len(self.timeouts_count)):
            self.timeouts_count[i] = 0


    # getters
    def getFuncInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        return self.intervals_message[i]
    def getArgsInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        return self.intervals_args[i]
    def getCountInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        return self.intervals_count[i]
    def getTimeInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        return self.intervals_end[i]
    def getNameInterval(self,name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        return self.intervals_name[i]
    
    def getFuncTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        return self.timeouts_message[i]
    def getArgsTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        return self.timeouts_args[i]
    def getCountTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        return self.timeouts_count[i]
    def getTimeTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        return self.timeouts_end[i]
    def getNameTimeout(self,name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        return self.timeouts_name[i]

    # setters
    def setFuncInterval(self,name:str,function):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_message[i] = function

    def setArgsInterval(self,name:str,args):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_args[i] = args

    def setCountInterval(self,name:str,count:int):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_count[i] = count
    def setTimeInterval(self,name:str,end:int):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_end[i] = end
    def setNameInterval(self,name:str,new_name:str):
        try:
            i = self.intervals_name.index(name)
        except:
            return -1
        self.intervals_name[i] = new_name
    
    def setFuncTimeout(self,name:str,function):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_message[i] = function
    def setArgsTimeout(self,name:str,args):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_args[i] = args
    def setCountTimeout(self,name:str,count:int):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_count[i] = count
    def setTimeTimeout(self,name:str,end:int):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_end[i] = end
    def setNameTimeout(self,name:str,new_name:str):
        try:
            i = self.timeouts_name.index(name)
        except:
            return -1
        self.timeouts_name[i] = new_name