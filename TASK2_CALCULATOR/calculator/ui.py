import tkinter as tk
from logic import evaluate, load_history

DARK = {"bg": "#1e1e2f", "btn": "#2a2a40", "text": "white"}
LIGHT = {"bg": "#f5f5f5", "btn": "#dddddd", "text": "black"}


# 🔹 Tooltip
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tip = tk.Toplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")

        label = tk.Label(self.tip, text=self.text, bg="black", fg="white")
        label.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()


class Calculator:
    def __init__(self, root):
        self.root = root
        self.theme = DARK
        self.memory = 0

        root.title("Advanced Calculator")
        root.geometry("450x650")

        # Entry
        tk.Label(
            root,
            text="Output",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=10)

        self.entry = tk.Entry(root, font=("Segoe UI", 20), justify="right")
        self.entry.pack(fill="x", padx=10, pady=5)

        # Live preview
        self.preview = tk.Label(root, fg="gray")
        self.preview.pack(anchor="e", padx=10)

        self.entry.bind("<KeyRelease>", self.live_preview)

        # Buttons
        frame = tk.Frame(root)
        frame.pack()

        buttons = [
            ("7","7"),("8","8"),("9","9"),("/","divide"),("sqrt","sqrt"),
            ("4","4"),("5","5"),("6","6"),("*","multiply"),("pow","power"),
            ("1","1"),("2","2"),("3","3"),("-","subtract"),("log","log"),
            ("0","0"),(".","dot"),("(","open"),(")","close"),("+","add"),
            ("sin","sin"),("cos","cos"),("=","equals"),("C","clear")
        ]

        row = col = 0
        for text, tip in buttons:
            btn = tk.Button(frame, text=text, width=6, height=2,
                            command=lambda t=text: self.click(t))
            btn.grid(row=row, column=col, padx=5, pady=5)
            ToolTip(btn, tip)

            col += 1
            if col > 4:
                col = 0
                row += 1

        # Memory buttons
        mem_frame = tk.Frame(root)
        mem_frame.pack(pady=5)

        for m in ["M+", "M-", "MR", "MC"]:
            btn = tk.Button(mem_frame, text=m, width=6,
                            command=lambda x=m: self.memory_action(x))
            btn.pack(side="left", padx=5)
            ToolTip(btn, f"Memory {m}")

        # Theme toggle
        tk.Button(root, text="Toggle Theme",
                  command=self.toggle_theme).pack(pady=5)

        # 📜 History
        tk.Label(
            root,
            text="History",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.history = tk.Listbox(root, height=6)
        self.history.pack(fill="both", padx=10, pady=5)
        

        self.history.bind("<<ListboxSelect>>", self.use_history)

        # ⌨️ Keyboard support
        root.bind("<Key>", self.key_input)

        self.refresh_history()
        self.apply_theme()

    # 🔘 Button click
    def click(self, value):
        if value == "=":
            result = evaluate(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, result)
            self.preview.config(text="")
            self.refresh_history()

        elif value == "C":
            self.entry.delete(0, tk.END)
            self.preview.config(text="")

        elif value in ["sin","cos","log","sqrt"]:
            self.entry.insert(tk.END, f"{value}(")

        elif value == "pow":
            self.entry.insert(tk.END, "pow(")

        else:
            self.entry.insert(tk.END, value)

    # 👀 Live preview
    def live_preview(self, event=None):
        exp = self.entry.get()
        result = evaluate(exp)
        if result != "Error":
            self.preview.config(text=f"= {result}")
        else:
            self.preview.config(text="")

    # 🧾 History
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

    # 🧠 Memory
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
            self.entry.insert(tk.END, str(self.memory))
        elif op == "MC":
            self.memory = 0

    # 🌙 Theme
    def toggle_theme(self):
        self.theme = LIGHT if self.theme == DARK else DARK
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.theme["bg"])
        self.entry.configure(bg=self.theme["btn"], fg=self.theme["text"])
        self.history.configure(bg=self.theme["btn"], fg=self.theme["text"])

    # ⌨️ Keyboard
    def key_input(self, event):
        if event.char in "0123456789+-*/().":
            self.entry.insert(tk.END, event.char)

        elif event.keysym == "Return":
            self.click("=")

        elif event.keysym == "BackSpace":
            self.entry.delete(len(self.entry.get())-1, tk.END)

        elif event.keysym == "Escape":
            self.entry.delete(0, tk.END)