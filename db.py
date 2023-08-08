from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Includes database operations
class DB:


    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']


    # checks if an account with the username exists
    def is_account_exist(self, username):

        if len(list(self.db.accounts.find({'username': username}))) > 0:
            return True
        else:
            return False
    

    # registers a user
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)


    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(self, username):
        if len(list(self.db.online_peers.find({"username": username}))) > 0:
            return True
        else:
            return False

    
    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)
    

    # logs out the user 
    def user_logout(self, username):
        self.db.online_peers.delete_one({"username": username})
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    # Assuming you have imported the necessary exceptions


    def register_room(self, room_id, peers = []):
        # Check if the room_id already exists in the database
        if self.db.rooms.find_one({"room_id": room_id}):
            raise ValueError(f"Room with id {room_id} already exists.")
        
        room = {
            "room_id": room_id,
            "peers": peers
        }

        # Store the room information in the database
        self.db.rooms.insert_one(room)

    # checks if an room with the id exists
    def is_room_exist(self, room_id):
        if len(list(self.db.rooms.find({'room_id': room_id}))) > 0:
            return True
        else:
            return False
        
    #Needed when we flood a message
    def get_room_peers(self, room_id):
        res = self.db.rooms.find_one({"room_id": room_id})
        return (res["_id"] ,res["peers"])
    
    def update_room(self, id, peers):
        filter_criteria = {"_id": id}
        update_data = {
            "$set": {"peers": peers}
        }
        self.db.rooms.update_one(filter_criteria, update_data)
