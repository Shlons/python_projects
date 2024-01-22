import threading
import socket
HOST = "127.0.0.1"
PORT = 55555
quit_from_server=False
class Client_player(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket tcp
        self.client.connect((HOST,PORT))  #connecting to the server


    def Get_message(self): #getting a message from server
        mess=self.client.recv(1024)
        return mess.decode()

    def Send_message(self, mess): #sending a message to server
        self.client.send(mess.encode())

    def run(self):
        q1 = Get_Message(self)
        q1.start()
        q2 = Send_Message(self)
        q2.start()


class Get_Message(threading.Thread): #thread of getting a message from server
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client=client
    def run(self):
        global quit_from_server
        while (True):
            try:
                response = self.client.Get_message()
                print(response)
                if(response=="you disconected"):
                    quit_from_server=True
                    print("please enter another message to fully exit the program")
                    break
            except:
                print("server disconnected")
                break
class Send_Message(threading.Thread): #thread of sending a message from server
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client=client
    def run(self):
        global quit_from_server
        while(True):
            try:
                if(quit_from_server):
                    break
                else:
                    mess = input()
                    self.client.Send_message(mess)
            except:
                break
client=Client_player()
client.start()




