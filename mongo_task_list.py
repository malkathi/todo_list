import pymongo

import private

from pymongo import MongoClient
from bson.objectid import ObjectId

connection_string = "mongodb://{u}:{p}@ds221258.mlab.com:21258/cloudapps"

client = MongoClient(connection_string.format(u=private.mongo_user,
                                              p=private.mongo_password))

db = client.cloudapps
current_tasks = db.current_tasks

def get_tasks():
    tasks = list(current_tasks.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return tasks

def get_tasks_by_status(status):
    tasks = list(current_tasks.find({"status":status}))
    for task in tasks:
        task['_id'] = str(task['_id'])
    return tasks

def get_task(task_id):
    # Convert from string to ObjectId:
    object_id = ObjectId(task_id)
    task = current_tasks.find_one({'_id': object_id})
    task['_id'] = str(task['_id'])
    return task

def save_task(task):
    task_id = current_tasks.insert_one(task).inserted_id
    return str(task_id)

def delete_task(task_id):
    object_id = ObjectId(task_id)
    task = current_tasks.delete_one({'_id': object_id})    

def update_task(task_id, description=None, status=None):
    if description:
        update = {'$set':{'description':description}}
        object_id = ObjectId(task_id)
        current_tasks.update_one({'_id': object_id}, update)    
    if status:
        update = {'$set':{'status':status}}
        object_id = ObjectId(task_id)
        current_tasks.update_one({'_id': object_id}, update)    


