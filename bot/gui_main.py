import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from parallel_runner import run_all_batches  # Import your main bot logic


class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mirren Star Legends Bot GUI")

        # Row 0 - Base Instance Name
        tk.Label(self, text="Base Instance Name:").grid(row=0, column=0, sticky='e')
        self.entry_base_instance = tk.Entry(self)
        self.entry_base_instance.insert(0, "LDPlayer")  # Default
        self.entry_base_instance.grid(row=0, column=1)

        # Row 1 - Proxy API Key
        tk.Label(self, text="Proxy API Key:").grid(row=1, column=0, sticky='e')
        self.entry_proxy_api = tk.Entry(self)
        self.entry_proxy_api.insert(0, "your_proxy_proxy_api")  # Empty by default
        self.entry_proxy_api.grid(row=1, column=1)

        # Row 2 - Total Accounts
        tk.Label(self, text="Total Accounts:").grid(row=2, column=0, sticky='e')
        self.entry_total_accounts = tk.Entry(self)
        self.entry_total_accounts.insert(0, "2")
        self.entry_total_accounts.grid(row=2, column=1)

        # Row 3 - Batch Size
        tk.Label(self, text="Batch Size:").grid(row=3, column=0, sticky='e')
        self.entry_batch_size = tk.Entry(self)
        self.entry_batch_size.insert(0, "1")
        self.entry_batch_size.grid(row=3, column=1)

        # Start Button
        self.btn_start = tk.Button(self, text="Start Bot", command=self.start_bot_thread)
        self.btn_start.grid(row=4, column=0, columnspan=2, pady=10)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self, width=60, height=20, state='disabled')
        self.log_area.grid(row=5, column=0, columnspan=2)

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def start_bot_thread(self):
        try:
            base_instance = self.entry_base_instance.get()
            proxy_api = self.entry_proxy_api.get()
            total_accounts = int(self.entry_total_accounts.get())
            batch_size = int(self.entry_batch_size.get())

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
            args=(base_instance, proxy_api, total_accounts, batch_size),
            daemon=True
        ).start()

    def run_bot(self, base_instance, proxy_api, total_accounts, batch_size):
        try:
            run_all_batches(base_instance, proxy_api, total_accounts, batch_size, self.log)
            self.log("✅ Bot run completed successfully")
        except Exception as e:
            self.log(f"❌ Error during bot run: {e}")
        finally:
            self.btn_start.config(state='normal')


if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
