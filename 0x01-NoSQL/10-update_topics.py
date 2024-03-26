#!/usr/bin/env python3
""" Writes a function that changes all topics of a school """


def update_topics(mongo_collection, name, topics):
    """
        changes all topics of a school document based on the name

        :param mongo_collection
        :param name
        :param topics
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
