# mock task list module

current_tasks = [
    ]

current_id = 0

def get_tasks():
    return current_tasks

def get_tasks_by_status(status):
    return [ task for task in current_tasks if task['status'] == status ]

def get_task(task_id):
    for task in current_tasks:
        if  task['_id'] == task_id:
            return task
    return None

def save_task(task):
    global current_id
    current_id += 1
    task_id = str(current_id)
    task['_id'] = task_id
    current_tasks.append(task)
    return task_id

def delete_task(task_id):
    global current_tasks
    current_tasks = [ task for task in current_tasks if task['_id'] != task_id ]

def update_task(task_id, description=None, status=None):
    for task in current_tasks:
        if  task['_id'] == task_id:
            if description:
                task['description'] = description
            if status:
                task['status'] = status
