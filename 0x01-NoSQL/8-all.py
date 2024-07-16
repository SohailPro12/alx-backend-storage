#!/usr/bin/env python3
"""
list_all function
"""


def list_all(mongo_collection):
    """
    list all documents in Python
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
