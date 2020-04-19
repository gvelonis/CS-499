##!/usr/bin/python3

from pymongo import MongoClient
from urllib.parse import quote_plus


class MongoIfc:
    # declare global variables
    __connection = None
    __db = None
    __collection = None

    # initialize with connection to provided host and port
    # host can be a hostname or IP address, defaults to 'localhost' if not provided
    # port should be an integer, defaults to 27017 if not provided
    # db is a string, the name of the database to use
    # collection is a string, the name of the collection to use
    def __init__(self,
                 db,
                 collection,
                 host='localhost',
                 port=None,
                 username=None,
                 password=None,
                 auth_db=None):
        # build the connection URI
        uri = "mongodb://"

        # authentication
        if username is not None:
            uri += "%s:%s@" % (quote_plus(username), quote_plus(password))

        # server
        uri += host  # only required piece for the URI
        if port is not None:
            uri += ":%s" % port

        # options
        if auth_db is not None:
            uri += "/%s" % auth_db

        self.__connection = MongoClient(uri)
        self.__db = self.__connection[db]
        self.__collection = self.__db[collection]

    # close MongoClient connection when object is deleted
    def __del__(self):
        self.__connection.close()

    # function to create a document
    # argument is a document (dictionary with full set of key/value pairs)\
    # returns True if success, False if failure
    def create_doc(self, document):
        try:
            self.__collection.save(document)
        except Exception as e:
            print(e)
            return False
        return True

    # function to read a document
    # argument is a key/value lookup pair (dictionary with 1 key/value pair)
    # returns list of documents matching the query
    def read_doc(self, query, fields=None):
        try:
            if fields is None:
                result = self.__collection.find(query)
            else:
                result = self.__collection.find(query, fields)
        except Exception as e:
            return e
        return result

    # function to update a document
    # first argument is key/value pair to select the document
    # second argument is key/value pair to update
    # returns True if Success, False if fail
    def update_doc(self, query, new_value):
        try:
            self.__collection.update_many(query, {'$set': new_value})
        except Exception as e:
            print(e)
            return False
        return True

    # function to delete a document
    # argument is a key/value lookup pair
    # returns True if success, false if failure
    def delete_doc(self, query):
        result = self.__collection.delete_many(query)
        if result.deleted_count == 0:
            return False
        return True

    # function to return aggregation results
    # argument is the pipeline string
    # returns results of db query
    def aggregate(self, pipeline):
        return self.__collection.aggregate(pipeline)
