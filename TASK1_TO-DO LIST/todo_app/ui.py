import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from logic import add_task, delete_task, toggle_complete

DARK = {
    "bg": "#1e1e2f",
    "card": "#2a2a40",
    "text": "#ffffff"
}

LIGHT = {
    "bg": "#f5f5f5",
    "card": "#ffffff",
    "text": "#000000"
}

ACCENT = "#6c63ff"
SUCCESS = "#00c896"
DANGER = "#ff5c5c"


class TodoUI:
    def __init__(self, root, tasks):
        self.root = root
        self.tasks = tasks
        self.theme = DARK

        root.title("To-Do List")
        root.geometry("420x550")

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.title = tk.Label(self.container, text="My Tasks", font=("Segoe UI", 18, "bold"))
        self.title.pack(anchor="w")

        self.entry = tk.Entry(self.container)
        self.entry.pack(fill="x", pady=5)

        self.date_entry = tk.Entry(self.container)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.pack(fill="x", pady=5)

        self.priority = tk.StringVar(value="Medium")
        tk.OptionMenu(self.container, self.priority, "High", "Medium", "Low").pack()

        tk.Button(self.container, text="Add Task", bg=ACCENT, fg="white",
                  command=self.add).pack(fill="x", pady=5)

        self.listbox = tk.Listbox(self.container)
        self.listbox.pack(fill="both", expand=True, pady=10)

        btn_frame = tk.Frame(self.container)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Delete", bg=DANGER, fg="white",
                  command=self.delete).pack(side="left", expand=True, fill="x", padx=5)

        tk.Button(btn_frame, text="Complete", bg=SUCCESS, fg="white",
                  command=self.complete).pack(side="left", expand=True, fill="x", padx=5)

        tk.Button(self.container, text="Toggle Theme",
                  command=self.toggle_theme).pack(pady=5)

        self.apply_theme()
        self.refresh()

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        self.container.configure(bg=self.theme["bg"])
        self.title.configure(bg=self.theme["bg"], fg=self.theme["text"])
        self.listbox.configure(bg=self.theme["card"], fg=self.theme["text"])

    def refresh(self):
        self.listbox.delete(0, tk.END)
        today = datetime.today().date()

        for i, task in enumerate(self.tasks):
            text = f"{task['title']} [{task['priority']}] (Due: {task['due_date']})"

            if task["completed"]:
                text += " ✔"

            self.listbox.insert(tk.END, text)

            # overdue
            try:
                due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                if due < today and not task["completed"]:
                    self.listbox.itemconfig(i, fg="red")
            except:
                pass

    def add(self):
        success, msg = add_task(
            self.tasks,
            self.entry.get(),
            self.priority.get(),
            self.date_entry.get()
        )

        if success:
            self.entry.delete(0, tk.END)
            self.refresh()
        else:
            messagebox.showwarning("Error", msg)

    def delete(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Error", "Select a task")
            return

        success, _ = delete_task(self.tasks, sel[0])
        if success:
            self.refresh()

    def complete(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Error", "Select a task")
            return

        success, _ = toggle_complete(self.tasks, sel[0])
        if success:
            self.refresh()

    def toggle_theme(self):
        self.theme = LIGHT if self.theme == DARK else DARK
        self.apply_theme()