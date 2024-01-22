import threading
import socket
client_nicknames = {}#dict of clients socket and their nicknames
rooms_passwords={}# room and passwords dict
client_rooms={}#clients sockets and room dict
id_counter=0
class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket tcp
        self.server_socket.bind(('0.0.0.0',55555))
        self.server_socket.listen()

    def Get_Direct(self,client): #gets message from the client
        mess=client.recv(1024)
        return mess.decode()

    def Send_Direct(self, client, mess): #sending message to the client
        client.send(mess.encode())

    def run(self):
        global client_sockets
        while(True): #start a thread
            conn, addr = self.server_socket.accept()
            q=GetMessage(conn,self)
            q.start()

class GetMessage(threading.Thread):
    def __init__(self, client,server):
        threading.Thread.__init__(self)
        self.server=server
        self.client=client
    def menu(self,nickname): #returns flase if the or disconected unexpectedly, return true when creates a room or enters one
        global client_nicknames
        global rooms_passwords
        global client_rooms
        global id_counter
        self.server.Send_Direct(self.client,'Please choose one of the following options by entering option number: \n 1. Connect To group chat. \n 2. Create a group chat. \n 3. Exit the server.')
        while(True):
            try:
                option = self.server.Get_Direct(self.client)
                option = int(option)
                if (option > 3 or option < 1):
                    self.server.Send_Direct(self.client,'invalid option, option must be a number between 1-3  \n Please choose one of the following options by entering option number: \n 1. Connect To group chat. \n 2. Create a group chat. \n 3. Exit the server. ')
                    continue
                if (option == 1):#enter an exsisting room
                    self.server.Send_Direct(self.client, 'Enter group id')
                    id = self.server.Get_Direct(self.client)
                    id = int(id)
                    if (id in rooms_passwords.keys()):
                        self.server.Send_Direct(self.client, 'Enter password')
                        password = self.server.Get_Direct(self.client)
                        if (password == rooms_passwords[id]):
                            if(id in client_rooms.keys()):
                                client_rooms[id].append(nickname)
                            else:
                                client_rooms[id]=[]
                                client_rooms[id].append(nickname)
                            self.server.Send_Direct(self.client, 'welcome to room #'+ str(id))
                            return True, id
                        else:
                            self.server.Send_Direct(self.client,
                                                    'invalid password  \n Please choose one of the following options by entering option number: \n 1. Connect To group chat. \n 2. Create a group chat. \n 3. Exit the server. ')
                            continue
                    else:
                        self.server.Send_Direct(self.client,  'invalid id  \n Please choose one of the following options by entering option number: \n 1. Connect To group chat. \n 2. Create a group chat. \n 3. Exit the server. ')
                        continue
                else:
                    if (option == 2):#create a room
                        self.server.Send_Direct(self.client, 'Please enter your room password:')
                        password = self.server.Get_Direct(self.client)
                        rooms_passwords[id_counter] = password
                        if (id_counter in client_rooms.keys()):
                            client_rooms[id_counter].append(nickname)
                        else:
                            client_rooms[id_counter] = []
                            client_rooms[id_counter].append(nickname)
                        self.server.Send_Direct(self.client, 'you created the room #'+ str(id_counter))
                        id_counter = id_counter + 1
                        return True, id_counter - 1
                    else:#disconnect
                        self.server.Send_Direct(self.client, 'you disconected')
                        del client_nicknames[nickname]
                        return False, -1
            except:
                print("client disconnected")
                del client_nicknames[nickname]
                return False,-1

    def run(self): #main loop of the game in a thread
        global client_nicknames
        global rooms_passwords
        global client_rooms
        nickname_found=False
        in_chat=False
        my_room_id=0
        #getting a nickname
        self.server.Send_Direct(self.client,'Enter your nickname: \n')
        while(True):
            try:
                nickname = self.server.Get_Direct(self.client)
                if(nickname in client_nicknames.keys()):
                    self.server.Send_Direct(self.client,'this nickname is already in use, please pick another one.')
                    continue
                client_nicknames[nickname]= self.client
                nickname_found=True
                break
            except:
                print("client disconnected")
                break
        #entering the char room
        if(nickname_found):
            in_chat,my_room_id=self.menu(nickname)
            while(in_chat):
                try:
                    mess=self.server.Get_Direct(self.client)
                    my_groups_clients = client_rooms[my_room_id]
                    for i in range(len(my_groups_clients)):
                        if (my_groups_clients[i] != nickname):
                            self.server.Send_Direct(client_nicknames[my_groups_clients[i]],nickname+": \n"+mess)#sending to all the clients in the room
                except:
                    my_groups_clients=client_rooms[my_room_id]
                    for i in range(len(my_groups_clients)):
                        if(my_groups_clients[i]!=nickname):
                            self.server.Send_Direct(client_nicknames[my_groups_clients[i]],nickname+" has disconnected")
                        else:
                            disconected_client=i
                    del client_nicknames[my_groups_clients[disconected_client]]
                    client_rooms[my_room_id].pop(disconected_client)
                    if(client_rooms[my_room_id]==[]):
                        del rooms_passwords[my_room_id] #if room is empty delete it from dict
                    break




server=Server()
server.start()

