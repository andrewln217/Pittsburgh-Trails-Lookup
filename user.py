from google.cloud import datastore
from flask import Flask, url_for

import datetime
import hashlib
import os

class UserCredential:
    def __init__(self, user_email, password_hash, salt, name, bio, pro_pic,likedTrails):
        self.user_email = user_email
        self.password_hash = password_hash
        self.salt = salt
        self.name = name
        self.bio = bio
        self.pro_pic = pro_pic
        self.likedTrails = likedTrails

def generate_credentials(user_email, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)
    return UserCredential(user_email, password_hash, salt, '', '', url_for('static', filename='blank.jpg'),'')

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
        return UserCredential(user["user_email"], user["password_hash"], user["salt"], user["name"], user["bio"], user["pro_pic"], user["likedTrails"])

    def store_new_credentials(self, creds, txn=None):
        user_key = self.ds.key("UserCredential", creds.user_email)
        user = datastore.Entity(key=user_key)
        user["user_email"] = creds.user_email
        user["password_hash"] = creds.password_hash
        user["salt"] = creds.salt
        user["name"] = creds.name
        user["bio"] = creds.bio
        user["pro_pic"] = creds.pro_pic
        user["likedTrails"] = creds.likedTrails
        self.ds.put(user)

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="UserCredential")
        users = query.fetch()
        return [u["user_email"] for u in users if "user_email" in u]

    def update_profile(self, user_email, name, bio, pro_pic, txn=None):
        user_key = self.ds.key("UserCredential",user_email)
        user = self.ds.get(user_key)
        user_email = user["user_email"]
        password_hash = user["password_hash"]
        salt = user["salt"]
        likedTrails = user["likedTrails"]
        user_key = self.ds.key("UserCredential", user_email)
        new_user = datastore.Entity(key=user_key)
        new_user["user_email"] = user_email
        new_user["password_hash"] = password_hash
        new_user["salt"] = salt
        new_user["name"] = name
        new_user["bio"] = bio
        new_user["pro_pic"] = pro_pic
        new_user["likedTrails"] = likedTrails
        self.ds.put(new_user)

    def get_profile(self,user_email, txn=None):
        query = self.ds.key("UserCredential", user_email)       
        found_user = self.ds.get(query)
        return found_user;

    def get_name(self, user_email, txn=None):
        user_key = self.ds.key("UserCredential", user_email)
        user = datastore.Entity(key=user_key)
        if not user:
            return None
        name = user["name"]
        return name

    def get_bio(self, user_email, txn=None):
        user_key = self.ds.key("UserCredential", user_email)
        user = datastore.Entity(key=user_key)
        if not user:
            return None
        bio = user["bio"]
        return bio

    def get_pro_pic(self, user_email, txn=None):
        user_key = self.ds.key("UserCredential", user_email)
        user = datastore.Entity(key=user_key)
        if not user:
            return None
        pro_pic = user["pro_pic"]
        return pro_pic

    def set_likedTrails(self,user_email,liked,txn=None):
        user_key = self.ds.key("UserCredential",user_email)
        user = self.ds.get(user_key)
        user_email = user["user_email"]
        password_hash = user["password_hash"]
        salt = user["salt"]
        name = user["name"]
        bio = user["bio"]
        pro_pic = user["pro_pic"]
        likedTrails = liked
        likedTrails += user["likedTrails"]
        user_key = self.ds.key("UserCredential", user_email)
        new_user = datastore.Entity(key=user_key)
        new_user["user_email"] = user_email
        new_user["password_hash"] = password_hash
        new_user["salt"] = salt
        new_user["name"] = name
        new_user["bio"] = bio
        new_user["pro_pic"] = pro_pic
        new_user["likedTrails"] = likedTrails
        self.ds.put(new_user)
        

    
    def get_likedTrails(self, user_email, txn=None):
        user_key = self.ds.key("UserCredential", user_email)
        user = datastore.Entity(key=user_key);
        if not user:
            return None
        likedTrails = user["likedTrails"]
        return likedTrails
