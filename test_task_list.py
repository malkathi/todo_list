#import mock_task_list as task_list
#import mongo_task_list as task_list

import sqlite_task_list as task_list
import pytest

def setup_module():
    for task_id in [t['_id'] for t in task_list.get_tasks()]:
        task_list.delete_task(task_id)

def test_dummy():
    pass

def test_get_tasks():
    task_list.save_task({'description' : "This is a test task.", 'status' : "1"})
    task_list.save_task({'description' : "This is another test task.", 'status' : "1"})
    tasks = task_list.get_tasks()
    assert type(tasks) is list
    for task in tasks:
        for item in ['_id','description','status']:
            assert type(task[item]) is str
        assert task['status'] == '1'

def test_get_tasks_by_status():
    task_list.save_task({'description' : "This is an inactive task.", 'status' : "0"})
    task_list.save_task({'description' : "This is an active task.", 'status' : "1"})
    tasks = task_list.get_tasks_by_status("0")
    for task in tasks:
        assert task['status'] == "0"
    tasks = task_list.get_tasks_by_status("1")
    for task in tasks:
        assert task['status'] == "1"

def test_get_task():
    tasks = task_list.get_tasks()
    task_id = task_list.get_tasks()[0]['_id']
    assert type(task_id) is str
    task = task_list.get_task(task_id)
    assert(task['description'] == "This is a test task.")
    assert(task['status'] == "1")

def test_save_task():
    task_list.save_task({'description' : "Do something worth saving", 'status' : "1"})
    tasks = task_list.get_tasks()
    assert type(tasks) is list
    found = False
    for task in tasks:
        assert 'description' in task
        if task['description'] == "Do something worth saving":
            found = True
    assert found

def test_delete_task():
    task_id = task_list.save_task({'description' : "This is a deletable task.", 'status' : "1"})
    tasks = task_list.get_tasks()
    found = False
    for task in tasks:
        if "deletable" in task['description']:
            found = True 
    assert found
    task_list.delete_task(task_id)
    tasks = task_list.get_tasks()
    found = False
    for task in tasks:
        if "deletable" in task['description']:
            found = True 
    assert not found

def test_update_task():
    task_id = task_list.save_task({'description' : "Do something worth updating", 'status' : "1"})
    task_list.update_task(task_id, description="This has been updated")
    task = task_list.get_task(task_id)
    assert "updated" in task['description']
    task_list.update_task(task_id, status="0")
    task = task_list.get_task(task_id)
    assert "0" in task['status']

def teardown_module():
    tasks = task_list.get_tasks()
    for task_id in [t['_id'] for t in tasks]:
        task_list.delete_task(task_id)

