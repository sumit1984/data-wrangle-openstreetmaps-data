#!/usr/bin/env python
'''
This program is used to generate the results given in the report
For most of the results an aggregation pipeline is created and then the aggregation 
is run by using the .aggregate method
The results are then displayed
'''

# To get an instance of db
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

# Pipeline for getting the user who contributed most
def make_pipeline_number1_user():
    # complete the aggregation pipeline
    pipeline = [{"$group":{"_id":"$created.user",
                           "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":1}]
    return pipeline
  
# Pipeline for getting the number of users who have contributed only once
def make_pipeline_user_only_once():
    pipeline = [{"$group":{"_id":"$created.user",
                           "count":{"$sum":1}}},
                {"$group":{"_id":"$count", 
                           "user_number":{"$sum":1}}},
                {"$sort":{"_id":1}},
                {"$limit":1}]
    return pipeline

# Pipeline for getting top 10 amenities
def make_pipeline_top10_amenities():
    pipeline = [{"$match":{"amenity":{"$exists":1}}},
                {"$group":{"_id":"$amenity", 
                           "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":10}]
    return pipeline
   
# Pipeline for getting the religion which has maximum number of places of worship
def make_pipeline_biggest_religion():
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
                {"$group":{"_id":"$religion", 
                           "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":1}]
    return pipeline

# Pipeline for getting number of places of worship for different religion    
def make_pipeline_different_places_of_worship():
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"place_of_worship"}},
                {"$group":{"_id":"$religion", 
                           "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
               ]
    return pipeline
  
# Pipeline for getting the top 5 cuisines in restaurants  
def make_pipeline_different_cuisines():
    pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}},
                {"$group":{"_id":"$cuisine", 
                           "count":{"$sum":1}}},
                {"$sort":{"count":-1}},
                {"$limit":5}]
    return pipeline
 
# Function for running the aggregator method on given db and pipeline
def aggregate(db, pipeline):
    result = db.new_delhi.aggregate(pipeline)
    return result
    
if __name__ == '__main__':

    db = get_db('examples')
    
    
    print "number of documents is ", db.new_delhi.find().count()
    print "number of ways is ", db.new_delhi.find({"type":"way"}).count()
    print "number of node is ", db.new_delhi.find({"type":"node"}).count()
    
    
    
    # to get number of ways and nodes
    result = db.new_delhi.aggregate([{"$group":{"_id":"$type", "count":{"$sum":1}}}])    
    for doc in result:
        print "number of ", doc['_id'], " is ", doc['count']
    
    
    
    
    # To get the distinct users
    disctinct_users = db.new_delhi.distinct("created.user")
    print "Number of distinct user is ", len(disctinct_users)
    
    
    
    # To get number 1  user
    pipeline = make_pipeline_number1_user()
    result = aggregate(db, pipeline)
    print "User who has contributed the most"
    for doc in result:
        print doc
    
    
    
    # To get number of users who have contributed only once
    pipeline = make_pipeline_user_only_once()
    result = aggregate(db, pipeline)
    print "Number of users who have made only 1 post"
    for doc in result:
        print doc
    

    
    # To get the top 10 amenities
    pipeline = make_pipeline_top10_amenities()
    result = aggregate(db, pipeline)
    print "Top 10 amenities"
    for doc in result:
        print doc
    
    
    
    # To get religion having maximum number of places of worship
    pipeline = make_pipeline_biggest_religion()
    result = aggregate(db, pipeline)
    print "religion having maximum number of places of worship"
    for doc in result:
        print doc
    
    
    
    # to get the number of places of worship for different religion
    pipeline = make_pipeline_different_places_of_worship()
    result = aggregate(db, pipeline)
    print "places of worship for different religion"
    for doc in result:
        print doc
    
    
    
    # to get different cuisines in resturant
    pipeline = make_pipeline_different_cuisines()
    result = aggregate(db, pipeline)
    print "top 5 cuisines"
    for doc in result:
        print doc
    
