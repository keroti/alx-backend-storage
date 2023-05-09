#!/usr/bin/env python3
'''
Function that returns the list of school having a specific topic
'''


def schools_by_topic(mongo_collection, topic):
    '''Returns the list of school
    '''
    topic_search = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [school for school in mongo_collection.find(topic_searchl)]