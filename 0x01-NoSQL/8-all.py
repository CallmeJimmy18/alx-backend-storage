#!/usr/bin/env python3
""" Writes a function that lists all documents """
from pymongo import MongoClient


def list_all(mongo_collection):
    """
        lists all documents in a collection

        :param mongo_collection
    """
    return mongo_collection.find()
