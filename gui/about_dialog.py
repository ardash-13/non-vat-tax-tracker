import tkinter as tk

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("800x550")
        self.resizable(False, False)

        self.update_idletasks()  # 🔑 VERY IMPORTANT
        # Make sure the dialog is centered
        self.after(10, lambda: self.center_window(parent))  # Pass parent here

        # Set background color of the window
        self.configure(bg="#040f21")

        # Make the dialog modal
        # self.transient(parent)
        # self.grab_set()

        # ================= TITLE =================
        tk.Label(
            self,
            text="Non-VAT Income, Expense Tracker & Tax Assistant",
            font=("Segoe UI", 20, "bold"),
            bg="#040f21",
            fg="#ffffff"
        ).pack(pady=(15, 30))

        # ================= DESCRIPTION =================
        description = (
            "🧾 Disclaimer:\n"
            "This application is designed exclusively for Non-VAT businesses and professionals.\n\n"
            "It tracks business income and expenses and provides estimated tax summaries "
            "based on Philippine BIR rules.\n\n\n"
            
            "⚠ Legal Reminder:\n"
            "This app only helps you with computing your taxes. Remember to manually summarize these totals into your BIR Books of Accounts at the end of each month.\n\n"
            "Tax computations are for reference only. Consult a licensed accountant or BIR officer for official filing and compliance.\n\n\n"
            
            "💬 Contact / License Support:\n"
            "Email: argiepiamonte0@gmail.com\n"
            "Facebook/Messenger: Argie Piamonte"
        )

        tk.Label(
            self,
            text=description,
            font=("Segoe UI", 11),
            wraplength=520,
            justify="left",
            bg="#040f21",
            fg="#ffffff"
        ).pack(padx=20, pady=10)

        # Bring dialog to front safely
        self.lift()
        self.focus_force()
        self.attributes("-topmost", True)  # Keep window on top

    def center_window(self, parent):
        self.update_idletasks()

        # Dialog size
        w = self.winfo_width()
        h = self.winfo_height()

        # Parent position and size (absolute screen coords)
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        # Center over parent
        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 3) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")

    def close_dialog(self):
        """Method to destroy the AboutDialog window."""
        self.destroy()
