import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from parallel_runner import run_all_batches
import subprocess

class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Silver and Blood Bot")
        self.configure(bg="#121821", padx=20, pady=20)

        self.style = ttk.Style(self)
        self.configure_style()
        self.create_widgets()

        # Check if task exists on startup
        if self.check_task_exists():
            self.auto_claim_enabled = True
            self.btn_toggle_auto.config(text="🟢 Disable Daily Auto-Claim")
        else:
            self.auto_claim_enabled = False
            self.btn_toggle_auto.config(text="⚪ Enable Daily Auto-Claim")

    def configure_style(self):
        self.style.theme_use("default")

        # Label and Entry Style
        self.style.configure("TLabel", background="#121821", foreground="#cdd6f4", font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="#1f2933", foreground="#f5f5f5", insertcolor="white")

        # Button Style
        self.style.configure("TButton",
                             background="#2d3b55",
                             foreground="#f8faff",
                             font=("Segoe UI", 10, "bold"),
                             padding=6)
        self.style.map("TButton", background=[("active", "#3e4d6a")])

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
        # exe_path = "C:/Users/Killua/Desktop/Silver/bot/dist/daily_claim_runner.exe"
        exe_path = "D:/Silver_Blood_Bot/daily_claim_runner.exe"
        if not self.auto_claim_enabled:
            # Register Task
            command = (
                f'schtasks /Create /F /SC DAILY /TN {task_name} '
                f'/TR "{exe_path}" /ST {time_str}'
            )

            # Then run PowerShell to modify the task and remove the AC-only condition
            disable_conditions = (
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
            # Remove Task
            command = f'schtasks /Delete /F /TN {task_name}'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log("🗑️ Auto-claim task removed.")
                self.btn_toggle_auto.config(text="⚪ Enable Daily Auto-Claim")
                self.auto_claim_enabled = False
            else:
                self.log(f"❌ Failed to remove task: {result.stderr}")

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="SILVER AND BLOOD BOT", font=("Segoe UI", 16, "bold"), foreground="#154c79")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Input Fields
        fields = [
            ("Base Instance Name:", "Base_Instance"),
            ("Total Accounts:", "2"),
            ("Batch Size:", "1"),
            ("Guest Name:", "Meow")
        ]

        self.entries = {}
        for i, (label_text, default) in enumerate(fields, start=1):
            ttk.Label(self, text=label_text).grid(row=i, column=0, sticky='e', pady=5)
            entry = ttk.Entry(self, width=30)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[label_text] = entry

        # Daily Claim Time
        ttk.Label(self, text="Auto-Claim Time (HH:MM):").grid(row=5, column=0, sticky='e', pady=5)
        self.claim_time_entry = ttk.Entry(self, width=30)
        self.claim_time_entry.insert(0, "09:00")  # default time
        self.claim_time_entry.grid(row=5, column=1, sticky='w', pady=5)

        # Enable Auto Claim Button
        self.auto_claim_enabled = False
        self.btn_toggle_auto = ttk.Button(self, text="⚪ Enable Daily Auto-Claim", command=self.toggle_auto_claim)
        self.btn_toggle_auto.grid(row=6, column=0, columnspan=2, pady=(8, 10))

        # Start Button
        self.btn_start = ttk.Button(self, text=" ▶   Start Bot ", command=self.start_bot_thread)
        self.btn_start.grid(row=7, column=0, columnspan=2, pady=(12, 10))

        # Log Area
        self.log_area = scrolledtext.ScrolledText(
            self,
            width=60,
            height=20,
            font=("Consolas", 9),
            bg="#1e293b",
            fg="#cdd6f4",
            insertbackground="white",
            borderwidth=1,
            relief="solid"
        )
        self.log_area.configure(state='disabled')
        self.log_area.grid(row=8, column=0, columnspan=2, pady=10)

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
