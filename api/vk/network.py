from .netType import *
import requests

class Server():
    def __init__(self, fake=True, respond=False, log = True):
        self.log = log
        self.number = -1
        self.respond = respond
        self.fake = fake
    def Answer(self, url, data):
        resp = requests.Response()
        if self.respond == False:
            return resp
        resp.encoding = "utf-8"
        resp._content = r"{error:1}".encode("utf-8")
        resp.status_code = 200
        return resp
    def Send(self, url, data):
        self.number += 1
        if self.log == True:
            print(f"POST \n\tnumber: {self.number}\n\turl: {url} \n\twith: {data}")
        answer = None
        if self.fake == True:
            answer = self.Answer(url, data)
        else:
            pass    #TODO: implement
        if self.log == True:
            print(f"RESULT \n\tstatus_code:{answer.status_code} \n\ttext: {answer.text}")
        return answer
    

class Network():
    def __init__(self, _type = NetType.dry):
        self._type = _type
        self.Post = None
        self.SetType(_type)
    def SetType(self, _type):
        self._type = _type
        if _type == NetType.dry:
            server = Server(respond=False,log=True)
            self.Post = server.Send
        elif _type == NetType.emulate:
            server = Server(respond=True,log=True,fake=True)
            self.Post = server.Send
