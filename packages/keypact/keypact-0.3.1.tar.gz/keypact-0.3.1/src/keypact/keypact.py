#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from hashlib import sha256
import pickle

import fire

import time
from shutil import move, copy

class KeyPact:

    def __init__(self, name):
        self.name = name
        self.hashed_name = sha256(name.encode()).hexdigest()
        self.location = os.path.join(os.getcwd(), "kp-" + self.hashed_name)

        self.initialize()

    def initialize(self):
        try: 
            os.makedirs(self.location)
        except OSError:
            if not os.path.isdir(self.location):
                raise

    def set(self, key: str, value, type_of_value="str"):

        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        key_location = os.path.join(self.location, sha256(key.encode()).hexdigest())
        key_location_loading = os.path.join(self.location, key_location+".l")
        with open(key_location_loading, "wb") as f:
            pickle.dump({"key":key,"value":value, "type":type}, f)

        move(key_location_loading, key_location)


    def set_file(self, key: str, file, dont_remove: bool = False):

        self.set(key, file, type_of_value="file")
        key_name = self.get_file(key)
        if not dont_remove:
            move(file, os.path.join(self.location, key_name))
        else:
            copy(file, os.path.join(self.location, key_name))

    def get_file(self, key: str, custom_key_location: str = None):
        the_key = self.get(key,custom_key_location)
        return the_key+the_key.split("/")[-1]




    def get(self, key: str, custom_key_location: str = None):
        key_location = os.path.join(self.location, sha256(key.encode()).hexdigest()) if custom_key_location == None else custom_key_location

        if not os.path.isfile(os.path.join(self.location, key_location)):
            return None

        total_result = None

        try:
            with open(os.path.join(self.location, key_location), "rb") as f:
                result = pickle.load(f)
                try:
                    total_result = result["value"]
                except TypeError:
                    total_result = result
        except EOFError or FileNotFoundError:
            pass

        return total_result

    def get_key(self, key_location: str):
       

        if not os.path.isfile(os.path.join(self.location, key_location)):
            return None
        total_result = None

        try:
            with open(os.path.join(self.location, key_location), "rb") as f:
                result = pickle.load(f)
                if not "type" in result:
                    result["type"] = "str"
                try:
                    total_result = result["key"]
                except TypeError:
                    total_result = False
        except EOFError or FileNotFoundError:
            pass            
        return total_result

    def delete(self, key: str):
        key_location = os.path.join(self.location, sha256(key.encode()).hexdigest())

        try:
            os.remove(os.path.join(self.location, key_location))
        except OSError:
            pass

    def delete_file(self, key: str):
        

        try:
            os.remove(os.path.join(self.location, self.get_file(key)))
        except OSError:
            pass

        self.delete(key)
        

    def dict(self):
        result ={}
        for key in os.listdir(self.location):
            the_key = self.get_key(key)
            if not the_key is None:
                if the_key != False:
                    result_of_key = self.get(the_key)
                    if not result_of_key is None:
                        result[the_key] = result_of_key
        return result

def main():
    fire.Fire(KeyPact)    