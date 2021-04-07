from google.cloud import datastore

import datetime
import hashlib
import os

class UserCredential:
    def __init__(self, user_email, password_hash, salt):
        self.user_email = user_email
        self.password_hash = password_hash
        self.salt = salt


def generate_credentials(user_email, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)
    return UserCredential(user_email, password_hash, salt)

def hash_password(password, salt):
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)


class UserStore:
    def __init__(self, datastore_client):
        self.ds = datastore_client

    def verify_pass(self, user_email, password, txn=None):
        user_key = self.ds.key("UserCredential", user_email)
        user = self.ds.get(user_key)
        if not user:
            return None
        hash_attempt = hash_password(password, user["salt"])
        if hash_attempt != user["password_hash"]:
            return None
        return UserCredential(user["user_email"], user["password_hash"], user["salt"])

    def store_new_credentials(self, creds, txn=None):
        user_key = self.ds.key("UserCredential", creds.user_email)
        user = datastore.Entity(key=user_key)
        user["user_email"] = creds.user_email
        user["password_hash"] = creds.password_hash
        user["salt"] = creds.salt
        self.ds.put(user)

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="UserCredential")
        users = query.fetch()
        return [u["user_email"] for u in users if "user_email" in u]

    def update_profile(self,user_email,name,bio,pro_pic):
        user_key = self.ds.key("UserCredential",user_email)
        user = datastore.Entity(key=user_key)
        user["name"] = name
        user["bio"] = bio
        user["pro_pic"] = pro_pic
        self.ds.put(user)
    def get_profile(self,user_email):
        print(user_email)
        query = self.ds.key("UserCredential", user_email)       
        found_user = self.ds.get(query)
        print(found_user)
        
        return found_user;

        #return {"name":found_user["name"],"bio":found_user["bio"],"pro_pic":found_user["pro_pic"]}

        