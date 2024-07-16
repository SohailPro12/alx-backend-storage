#!/usr/bin/env python3
"""
inserts a new document in a collection
based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    insert_school function
    """
    if not mongo_collection:
        return []
    return mongo_collection.insert_one(kwargs).inserted_id
