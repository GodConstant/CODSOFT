import tkinter as tk
from storage import load_tasks
from ui import TodoUI

root = tk.Tk()
tasks = load_tasks()

TodoUI(root, tasks)

root.mainloop()