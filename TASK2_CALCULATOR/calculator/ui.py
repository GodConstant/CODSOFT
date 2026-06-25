import tkinter as tk
from logic import evaluate, load_history

DARK = {"bg": "#1e1e2f", "btn": "#2a2a40", "text": "white"}
LIGHT = {"bg": "#f5f5f5", "btn": "#dddddd", "text": "black"}


class Calculator:
    def __init__(self, root):
        self.root = root
        self.theme = DARK
        self.memory = 0

        self.build_ui()
        self.bind_keys()
        self.refresh_history()
        self.apply_theme()

    # ----------------------------
    # UI
    # ----------------------------
    def build_ui(self):
        self.root.title("Advanced Calculator")
        self.root.geometry("450x650")

        tk.Label(self.root, text="Output", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10)

        self.entry = tk.Entry(self.root, font=("Segoe UI", 20), justify="right")
        self.entry.pack(fill="x", padx=10, pady=5)

        self.preview = tk.Label(self.root, fg="gray")
        self.preview.pack(anchor="e", padx=10)

        self.entry.bind("<KeyRelease>", self.live_preview)

        frame = tk.Frame(self.root)
        frame.pack()

        buttons = [
            "7","8","9","/","sqrt",
            "4","5","6","*","pow",
            "1","2","3","-","log",
            "0",".","(",")","+",
            "sin","cos","=","C",
            "backspace"
        ]

        row = col = 0
        for text in buttons:
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                command=lambda t=text: self.click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col > 4:
                col = 0
                row += 1

        # Memory
        mem_frame = tk.Frame(self.root)
        mem_frame.pack(pady=5)

        for m in ["M+", "M-", "MR", "MC"]:
            tk.Button(mem_frame, text=m, width=6,
                      command=lambda x=m: self.memory_action(x)).pack(side="left", padx=5)

        tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme).pack(pady=5)

        # History
        tk.Label(self.root, text="History", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10)

        self.history = tk.Listbox(self.root, height=6)
        self.history.pack(fill="both", padx=10, pady=5)
        self.history.bind("<<ListboxSelect>>", self.use_history)

    # ----------------------------
    # ACTIONS
    # ----------------------------
    def click(self, value):
        if value == "=":
            result = evaluate(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
            self.preview.config(text="")
            self.refresh_history()

        elif value == "C":
            self.clear()

        elif value == "backspace":
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])

        elif value in ["sin","cos","log","sqrt","pow"]:
            self.entry.insert(tk.END, f"{value}(")

        else:
            self.entry.insert(tk.END, value)

    def clear(self):
        self.entry.delete(0, tk.END)
        self.preview.config(text="")

    def live_preview(self, event=None):
        exp = self.entry.get()
        result = evaluate(exp)
        if result != "Error":
            self.preview.config(text=f"= {result}")
        else:
            self.preview.config(text="")

    # ----------------------------
    # HISTORY
    # ----------------------------
    def refresh_history(self):
        self.history.delete(0, tk.END)
        for item in load_history():
            self.history.insert(tk.END, item)

    def use_history(self, event):
        sel = self.history.curselection()
        if sel:
            text = self.history.get(sel[0])
            exp = text.split("=")[0].strip()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, exp)

    # ----------------------------
    # MEMORY
    # ----------------------------
    def memory_action(self, op):
        try:
            val = float(self.entry.get())
        except:
            return

        if op == "M+":
            self.memory += val
        elif op == "M-":
            self.memory -= val
        elif op == "MR":
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(self.memory))
        elif op == "MC":
            self.memory = 0

    # ----------------------------
    # THEME
    # ----------------------------
    def toggle_theme(self):
        self.theme = LIGHT if self.theme == DARK else DARK
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        self.entry.configure(bg=self.theme["btn"], fg=self.theme["text"])
        self.history.configure(bg=self.theme["btn"], fg=self.theme["text"])

    # ----------------------------
    # KEYBOARD
    # ----------------------------
    def bind_keys(self):
        self.root.bind("<Return>", lambda e: self.click("="))
        self.root.bind("<Escape>", lambda e: self.clear())