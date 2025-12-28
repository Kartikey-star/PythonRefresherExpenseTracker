import json
import os
import hashlib

USERS_FILE = 'users.json'
TASKS_FILE = 'tasks.json'


def laodData(path, default):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default


def saveData(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def hashPassword(password: str) -> str:
    # Simple SHA-256 hashing for passwords
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# 1. User Authentication
def register():
    users = laodData(USERS_FILE, {})
    print("\n=== Registration ===")
    while True:
        username = input("Enter a username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if username in users:
            print("Username already exists. Try another.")
            continue
        break
    while True:
        password = input("Enter a password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        break
    users[username] = hashPassword(password)
    saveData(USERS_FILE, users)
    print("Registration successful! You can now log in.")


def login():
    users = laodData(USERS_FILE, {})
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username not in users:
        print("Invalid username or password.")
        return None
    if users[username] != hashPassword(password):
        print("Invalid username or password.")
        return None
    print(f"Welcome, {username}!")
    return username


# Tasks helpers
def loadTasks():
    return laodData(TASKS_FILE, {})


def saveTasks(tasks):
    saveData(TASKS_FILE, tasks)


def getNextTaskId(tasks, username):
    user_tasks = tasks.get(username, [])
    if not user_tasks:
        return 1
    return max(task["id"] for task in user_tasks) + 1

def addTask(username):
    tasks = loadTasks()
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return
    task_id = getNextTaskId(tasks, username)
    task = {
        "id": task_id,
        "description": description,
        "status": "Pending"
    }
    tasks.setdefault(username, []).append(task)
    saveTasks(tasks)
    print(f"Task added with ID {task_id}.")


# 3. View Tasks
def viewTasks(username):
    tasks = loadTasks()
    user_tasks = tasks.get(username, [])
    if not user_tasks:
        print("No tasks found.")
        return
    print("\nYour tasks:")
    print("-" * 40)
    for task in user_tasks:
        print(f"ID: {task['id']} | {task['description']} | Status: {task['status']}")
    print("-" * 40)


# 4. Mark Task as Completed
def updateTasks(username):
    tasks = loadTasks()
    user_tasks = tasks.get(username, [])
    if not user_tasks:
        print("No tasks to update.")
        return
    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("Invalid ID.")
        return
    for task in user_tasks:
        if task["id"] == task_id:
            task["status"] = "Completed"
            saveTasks(tasks)
            print("Task marked as completed.")
            return
    print("Task ID not found.")


# 5. Delete a Task
def deleteTasks(username):
    tasks = loadTasks()
    user_tasks = tasks.get(username, [])
    if not user_tasks:
        print("No tasks to delete.")
        return
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    new_tasks = [t for t in user_tasks if t["id"] != task_id]
    if len(new_tasks) == len(user_tasks):
        print("Task ID not found.")
        return
    tasks[username] = new_tasks
    saveTasks(tasks)
    print("Task deleted.")


def intercativeMenu(username):
    print("Please enter an option from the following")
    print("Menu")
    print("Input 1 for Add tasks")
    print("Input 2 for View tasks")
    print("Input 3 for Mark a task as completed")
    print("Input 4 for Delete a task")
    print("Input 5 for Logout")
    while True:
        choice=int(input("Enter your choice"))
        if choice == 1:
            addTask(username)
        elif choice == 2:
            viewTasks(username)
        elif choice == 3:
            updateTasks(username)
        elif choice == 4:
            deleteTasks(username)
        elif choice == 5:
            #exit
            break
        else:
            print("please enter a valid input")

def main():
    register()
    username=login()
    intercativeMenu(username)

if __name__ == "__main__":
    main()