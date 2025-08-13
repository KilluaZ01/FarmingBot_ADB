import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from parallel_runner import run_all_batches, get_persistent_path
import subprocess
import json
import os

BATCHES_FILE = get_persistent_path('batches.json')

class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Silver and Blood Bot")
        self.geometry("680x600")
        self.configure(bg="#1e1e2e")

        self.style = ttk.Style(self)
        self.configure_style()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_frame = ttk.Frame(self.notebook, style="Card.TFrame")
        self.instances_frame = ttk.Frame(self.notebook, style="Card.TFrame")

        self.notebook.add(self.main_frame, text="⚙ Main Bot")
        self.notebook.add(self.instances_frame, text="📋 Instance Status")

        self.create_main_tab()
        self.create_instances_tab()

        if self.check_task_exists():
            self.auto_claim_enabled = True
            self.btn_toggle_auto.config(text="🟢 Disable Daily Auto-Claim")
        else:
            self.auto_claim_enabled = False
            self.btn_toggle_auto.config(text="⚪ Enable Daily Auto-Claim")

    def configure_style(self):
        self.style.theme_use("clam")

        # Frame Style
        self.style.configure("Card.TFrame", background="#2e2e3e")

        # Labels & Entry
        self.style.configure("TLabel", background="#2e2e3e", foreground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="#3b3b4f", foreground="#ffffff", insertcolor="white")

        # Buttons
        self.style.configure("TButton",
                             background="#4a90e2",
                             foreground="white",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("TButton",
                       background=[("active", "#357ABD")],
                       foreground=[("active", "#ffffff")])

        # Treeview
        self.style.configure("Treeview",
                             background="#3b3b4f",
                             foreground="white",
                             fieldbackground="#3b3b4f",
                             bordercolor="#444",
                             rowheight=25)
        self.style.configure("Treeview.Heading",
                             background="#4a90e2",
                             foreground="white",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview.Heading",
                       background=[("active", "#357ABD")])

    # ---------------- MAIN TAB ----------------
    def create_main_tab(self):
        frame = self.main_frame

        ttk.Label(frame, text="SILVER AND BLOOD BOT", font=("Segoe UI", 16, "bold"), foreground="#4a90e2").grid(
            row=0, column=0, columnspan=2, pady=(10, 15)
        )

        fields = [
            ("Base Instance Name:", "SilverBlood"),
            ("Total Accounts:", "10"),
            ("Batch Size:", "2"),
            ("Guest Name:", "OP")
        ]

        self.entries = {}
        for i, (label_text, default) in enumerate(fields, start=1):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky='e', pady=5, padx=10)
            entry = ttk.Entry(frame, width=30)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[label_text] = entry

        ttk.Label(frame, text="Auto-Claim Time (HH:MM):").grid(row=6, column=0, sticky='e', pady=5, padx=10)
        self.claim_time_entry = ttk.Entry(frame, width=30)
        self.claim_time_entry.insert(0, "09:00")
        self.claim_time_entry.grid(row=6, column=1, sticky='w', pady=5)

        self.auto_claim_enabled = False
        self.btn_toggle_auto = ttk.Button(frame, text="⚪ Enable Daily Auto-Claim", command=self.toggle_auto_claim)
        self.btn_toggle_auto.grid(row=7, column=0, columnspan=2, pady=(8, 10), padx=(0, 10))

        self.btn_start = ttk.Button(frame, text="▶ Start Bot", command=self.start_bot_thread)
        self.btn_start.grid(row=7, column=1, columnspan=2, pady=(8, 10), padx=(10, 0))

        self.log_area = scrolledtext.ScrolledText(
            frame, width=90, height=18, font=("Consolas", 9),
            bg="#1e1e2e", fg="#cdd6f4", insertbackground="white", borderwidth=1, relief="solid"
        )
        self.log_area.configure(state='disabled')
        self.log_area.grid(row=9, column=0, columnspan=2, pady=10)

    # ---------------- INSTANCE STATUS TAB ----------------
    def create_instances_tab(self):
        frame = self.instances_frame

        columns = ("Instance Name", "Login Day", "Last Login", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)
        self.tree.pack(fill="both", expand=True, pady=10, padx=10)

        refresh_btn = ttk.Button(frame, text="🔄 Refresh", command=self.load_batches_data)
        refresh_btn.pack(pady=5)

        self.load_batches_data()

    def load_batches_data(self):
        self.tree.delete(*self.tree.get_children())
        if not os.path.exists(BATCHES_FILE):
            messagebox.showwarning("Warning", f"No {BATCHES_FILE} file found.")
            return

        try:
            with open(BATCHES_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = [data]
            for entry in data:
                instances = entry.get("instance_names", [])
                login_day = entry.get("login_day", "")
                last_login = entry.get("last_login", "")
                status = entry.get("status", "")
                for inst in zip(instances):
                    self.tree.insert("", tk.END, values=(inst, login_day, last_login, status))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load batch data:\n{e}")

    # ---------------- BOT CONTROL ----------------
    def check_task_exists(self, task_name="SilverBloodAutoClaim"):
        result = subprocess.run(f'schtasks /Query /TN {task_name}', shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0

    def toggle_auto_claim(self):
        time_str = self.claim_time_entry.get().strip()
        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM format.")
            return

        task_name = "SilverBloodAutoClaim"
        exe_path = "D:/Silver_Blood_Bot/daily_claim_runner.exe"
        if not self.auto_claim_enabled:
            command = (f'schtasks /Create /F /SC DAILY /TN {task_name} '
                       f'/TR "{exe_path}" /ST {time_str}')
            disable_conditions = disable_conditions = (
                f'powershell -Command "'
                f'$task = Get-ScheduledTask -TaskName \'{task_name}\'; '
                f'$task.Settings.DisallowStartIfOnBatteries = $false; '
                f'$task.Settings.StopIfGoingOnBatteries = $false; '
                f'Set-ScheduledTask -TaskName \'{task_name}\' -Settings $task.Settings"'
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            subprocess.run(disable_conditions, shell=True)
            if result.returncode == 0:
                self.log(f"✅ Scheduled daily claim at {time_str}")
                self.btn_toggle_auto.config(text="🟢 Disable Daily Auto-Claim")
                self.auto_claim_enabled = True
            else:
                self.log(f"❌ Failed to schedule task: {result.stderr}")
        else:
            command = f'schtasks /Delete /F /TN {task_name}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("🗑️ Auto-claim task removed.")
                self.btn_toggle_auto.config(text="⚪ Enable Daily Auto-Claim")
                self.auto_claim_enabled = False
            else:
                self.log(f"❌ Failed to remove task: {result.stderr}")

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def start_bot_thread(self):
        try:
            base_instance = self.entries["Base Instance Name:"].get()
            total_accounts = int(self.entries["Total Accounts:"].get())
            batch_size = int(self.entries["Batch Size:"].get())
            guest_name = self.entries["Guest Name:"].get()
            if total_accounts < 1 or batch_size < 1:
                raise ValueError("Values must be positive integers.")
            if batch_size > total_accounts:
                raise ValueError("Batch size cannot exceed total accounts.")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        self.btn_start.config(state='disabled')
        threading.Thread(
            target=self.run_bot,
            args=(base_instance, total_accounts, batch_size, guest_name),
            daemon=True
        ).start()

    def run_bot(self, base_instance, total_accounts, batch_size, guest_name):
        try:
            run_all_batches(base_instance, total_accounts, batch_size, guest_name, self.log)
            self.log("✅ Bot run completed successfully")
        except Exception as e:
            self.log(f"❌ Error during bot run: {e}")
        finally:
            self.btn_start.config(state='normal')


if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()