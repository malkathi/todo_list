# sqlite task list module
import sqlite3

connection = sqlite3.connect('todo.db')

def get_tasks():
    cursor = connection.cursor()
    cursor.execute("SELECT id, task, status FROM todo")
    items = [ {'_id':str(i), 'description':d, 'status':s} for (i, d, s) in cursor.fetchall() ]
    for item in items:
        item['status'] = str(item['status'])
    return items

def get_tasks_by_status(status):
    cursor = connection.cursor()
    cursor.execute("SELECT id, task, status FROM todo where status = ?", (int(status),))
    items = [ {'_id':str(i), 'description':d, 'status':s} for (i, d, s) in cursor.fetchall() ]
    for item in items:
        item['status'] = str(item['status'])
    return items

def get_task(task_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id, task, status FROM todo WHERE id = " + task_id)
    items = [ {'_id':str(i), 'description':d, 'status':s} for (i, d, s) in cursor.fetchall() ]
    if len(items) == 1:
        item = items[0]
        item['status'] = str(item['status'])
        return item
    return None

def save_task(task):
    cursor = connection.cursor()
    save_task = (task['description'], int(task['status']))
    x = cursor.execute('INSERT INTO todo("task", "status") VALUES(?,?)', save_task)
    lastrowid = cursor.lastrowid
    connection.commit()
    return str(lastrowid)

def delete_task(task_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM todo WHERE id = " + task_id)
    connection.commit()

def update_task(task_id, description=None, status=None):
    cursor = connection.cursor()
    if description:
        cursor.execute("UPDATE todo SET task = ? WHERE id = " + task_id, (description,))
    if status=='1':
        cursor.execute("UPDATE todo SET status = 1 WHERE id = " + task_id)
    else:
        cursor.execute("UPDATE todo SET status = 0 WHERE id = " + task_id)