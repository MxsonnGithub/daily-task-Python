import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(name):
    tasks = load_tasks()
    task = {"name": name, "start_time": time.time(), "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    messagebox.showinfo("Task Added", f"Task '{name}' added.")

def complete_task(name):
    tasks = load_tasks()
    for task in tasks:
        if task["name"] == name and not task["completed"]:
            task["completed"] = True
            task["end_time"] = time.time()
            save_tasks(tasks)
            messagebox.showinfo("Task Completed", f"Task '{name}' marked as completed!")
            return
    messagebox.showwarning("Task Not Found", f"Task '{name}' not found or already completed.")

def daily_report():
    tasks = load_tasks()
    completed_tasks = [t for t in tasks if t["completed"]]
    total_time = sum(t.get("end_time", 0) - t["start_time"] for t in completed_tasks)
    
    report = "Daily Report:\n" + "-" * 20 + "\n"
    report += f"Tasks Completed: {len(completed_tasks)}\n"
    report += f"Total Time Spent: {total_time / 60:.2f} minutes\n"
    for task in completed_tasks:
        report += f"✔ {task['name']}\n"
    
    messagebox.showinfo("Daily Report", report)

def add_task_gui():
    task_name = simpledialog.askstring("Add Task", "Enter task name:")
    if task_name:
        add_task(task_name)

def complete_task_gui():
    task_name = simpledialog.askstring("Complete Task", "Enter completed task name:")
    if task_name:
        complete_task(task_name)

def main():
    root = tk.Tk()
    root.title("Daily Productivity Tracker")
    root.geometry("300x200")
    
    tk.Button(root, text="Add Task", command=add_task_gui).pack(pady=5)
    tk.Button(root, text="Complete Task", command=complete_task_gui).pack(pady=5)
    tk.Button(root, text="Show Daily Report", command=daily_report).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
