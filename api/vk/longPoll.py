import requests
from queue import Queue
import random

class LongPoll:
    def __init__(self,basicToken,groupId,debug=False,verbouse=False,network="requests"):
        self.basicAddress = 'https://api.vk.com/method/'
        self.longpollApi = 'https://api.vk.com/method/groups.getLongPollServer'
        self.messageApi = 'https://api.vk.com/method/messages.send'
        self.participiantApi = 'messages.getConversationMembers'
        self.usersApi = 'users.get'
        self.groupId = groupId
        self.basicToken = basicToken
        self.LongpollServer = None
        self.longPollToken = None
        self.debug = debug
        self.verbouse = verbouse
        self.ts = None
        self.waitDefalt = 25
        self.initialized = False
        self.longpoolRes = Queue()
        self.longpoolResMax = 10
    def updateInner(self):
        for _ in range (0,4):
            if (self.initialized != True) or (self.needToReconnect == True):
                self.getLongPoll()
            else:
                return
        raise Exception("Attempt to init failed!")
    def getLongPoll(self):
        try:
            print(self.basicToken)
            answer = requests.post(\
                self.longpollApi,\
                data = {'group_id':self.groupId ,\
                        'access_token':self.basicToken,\
                        'v':'5.110'})
        except requests.ConnectionError:
            if (self.debug == True):
                print("Connection Error" + "\n")
            return
        if (answer.status_code == 200):
            if (self.debug == True):
                print("Longpoll: 200, answer:" + answer.text + "\n")
            ansJson = answer.json()
            self.LongpollServer = ansJson["response"]["server"]
            self.longPollToken = ansJson["response"]["key"]
            self.logPollToken = ansJson["response"]["ts"]
            self.initialized = True
            self.needToReconnect = False
        else:                
            if (self.debug == True):
                print("Longpoll status: " + str(anwer.status_code) + "\n" )
            raise Exception("Status code is incorrect ")
    def longPoll(self):
        if (self.longpoolRes.qsize() < self.longpoolResMax):
            res = requests.post(self.LongpollServer, data = {\
                    'act':'a_check','key':self.longPollToken,\
                    'ts':self.ts,'wait':self.waitDefalt})
            if (res.status_code == 200):
                failedSafe = False
                json = res.json()  
                try:
                    self.ts = json['ts']
                except:                    
                    if self.debug:
                        print(json)
                    failedSafe = True
                try: 
                    if (json['failed'] == 1):
                        failedSafe = True
                    if (json['failed'] == 2):
                        self.needToReconnect = True
                except:
                    pass
                if (failedSafe == False):
                    self.longpoolRes.put(json['updates'])
            else:
                raise Exception("Status code is incorrect")
    def sendMessage(self,dialog,text):
        resMsgRes = requests.post(self.messageApi, data = {\
            'peer_id':dialog, 'group_id':self.groupId, 'message':text,\
            'random_id':random.randint(1, 1000), 'access_token':self.basicToken, 'v':'5.123'})
        if self.debug == True:
            print(resMsgRes.text)
    def getMembers(self,dialog):
        resMembers = requests.post(self.basicAddress + self.participiantApi, data = {\
            'peer_id':dialog, 'group_id':self.groupId, 'access_token':self.basicToken, 'v':'5.123'})
        if self.debug == True:
            print(resMembers.text)
        json = resMembers.json()
        return json
    def getUserName(self,userId):
        resUser = requests.post(self.basicAddress + self.usersApi, data = {\
            'user_ids':userId, 'name_case':"Nom", 'access_token':self.basicToken, 'v':'5.120'})
        if self.debug == True:
            print(resUser.text)
        body = resUser.json()["response"][0]
        return body["first_name"] , body["last_name"]
