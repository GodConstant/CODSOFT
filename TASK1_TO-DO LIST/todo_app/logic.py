from storage import save_tasks

def add_task(tasks, title, priority, due_date):
    if not title.strip():
        return False, "Task cannot be empty"

    tasks.append({
        "title": title.strip(),
        "priority": priority,
        "completed": False,
        "due_date": due_date
    })

    save_tasks(tasks)
    return True, "Task added"


def delete_task(tasks, index):
    if index < 0 or index >= len(tasks):
        return False, "Invalid selection"

    tasks.pop(index)
    save_tasks(tasks)
    return True, "Task deleted"


def toggle_complete(tasks, index):
    if index < 0 or index >= len(tasks):
        return False, "Invalid selection"

    tasks[index]["completed"] = not tasks[index]["completed"]
    save_tasks(tasks)
    return True, "Updated"