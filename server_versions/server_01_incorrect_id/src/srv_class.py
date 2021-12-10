from uuid import uuid4
from dataclasses import dataclass


class SrvClass(object):
    def __init__(self):
        self.users = {}

    def new_user(self, username, email_address):
        user_data = UserData(str(uuid4()), username, email_address)
        self.users[user_data.username] = user_data
        # self.users[user_data.uid] = user_data

    def get_user_email_address(self, username):
        for user_data in self.users.values():
            if user_data.username == username:
                return {"email_address": user_data.email_address}
        return {"email_address": None}

    def delete_user(self, username):
        found_user_uid = None
        for uid, user_data in self.users.items():
            if user_data.username == username:
                found_user_uid = user_data.uid
        if found_user_uid:
            self.users.pop(found_user_uid)

    def clear(self):
        self.users.clear()


@dataclass
class UserData:
    uid: str
    username: str
    email_address: str
