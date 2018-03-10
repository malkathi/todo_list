import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from bottle import get, post, run, debug, default_app, request, template, static_file 

import mock_task_list as task_list
#import mongo_task_list as task_list

show_completed = True

@get('/')
@get('/task-list')
def get_task_list():
    global show_completed
    if (show_completed):
        tasks = task_list.get_tasks()
    else:
        tasks = task_list.get_tasks_by_status("0")
    output = template('task_list.tpl', tasks=tasks, show_completed = show_completed)
    return output

@post('/new-task')
def post_new_task():
    description = request.POST.new_task_description.strip()
    print(description)
    task={
        'description':description,
        'status':"0" # active, not completed
    }
    task_list.save_task(task)
    return get_task_list()

@get('/mark-as-completed/<id>')
def get_mark_as_completed(id):
    task_list.update_task(id, status="1")
    return get_task_list()

@get('/mark-as-active/<id>')
def get_mark_as_active(id):
    task_list.update_task(id, status="0")
    return get_task_list()

@get('/discard-task/<id>')
def get_discard_task(id):
    task_list.delete_task(id)
    return get_task_list()

@get('/hide-completed')
def get_hide_completed():
    global show_completed
    show_completed = False
    return get_task_list()
    
@get('/show-completed')
def get_show_completed():
    global show_completed
    show_completed = True
    return get_task_list()

@get('/static/<filepath:path>')
def server_static(filepath):
    print(filepath)
    return static_file(filepath, root='./static')

def setup():
    task_list.save_task({'description' : "This is a test task.", 'status' : "0"})
    task_list.save_task({'description' : "This is another test task.", 'status' : "0"})
    task_list.save_task({'description' : "This is a completed task.", 'status' : "1"})
    task_list.save_task({'description' : "This is an active task.", 'status' : "0"})

setup()
#application = default_app()
debug(True)
run(host='0.0.0.0', port=8080)

