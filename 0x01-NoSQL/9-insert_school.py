#!/usr/bin/env python3
""" Writes a function that inserts a new document in collection """


def insert_school(mongo_collection, **kwargs):
    """
        inserts a new document in collection

        :param mongo_collection
        :param kwargs
    """
    new_inserts = mongo_collection.insert_one(kwargs)

    return new_inserts.inserted_id
