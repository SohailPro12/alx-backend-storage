#!/usr/bin/env python3
"""
11-schools_by_topic.py
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    return mongo_collection.find({"topics": topic})

