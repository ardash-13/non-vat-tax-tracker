import tkinter as tk


class HelpTab(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Help – User Guide (Non-VAT)")
        self.geometry("1400x1000")
        self.resizable(True, True)

        self.update_idletasks()  # 🔑 VERY IMPORTANT
        # Make sure the dialog is centered
        self.after(10, lambda: self.center_window(parent))  # Pass parent here

        # Set background color of the window
        self.configure(bg="#040f21")

        # Make the dialog modal
        # self.transient(parent)
        # self.grab_set()

        # ================= SCROLLABLE AREA =================
        canvas = tk.Canvas(self, bg="#040f21", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        content = tk.Frame(canvas, bg="#040f21")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        # ================= MOUSE WHEEL SCROLL =================
        def _on_mousewheel(event, canvas=canvas):
            if canvas.winfo_exists():  # check if canvas still exists
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ================= TITLE =================
        tk.Label(
            content,
            text="📘 User Guide: Reports & Summary Module",
            font=("Segoe UI", 20, "bold"),
            bg="#040f21",
            fg="white"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        tk.Label(
            content,
            text=(
                "This module is designed to help non-VAT registered taxpayers in the Philippines"
                " (Freelancers, Professionals, and Sole Proprietors) visualize their tax liabilities for 2026."
                "\nIt automatically applies the complex rules of the TRAIN Law, including the specific treatment for mixed-income earners."
            ),
            font=("Segoe UI", 12),
            bg="#040f21",
            fg="#cbd5e1",
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 20))

        # ================= SECTION A: Navigation & Filters =================
        self.section(
            content,
            "1. Navigation & Filters",
            [
                "🟢 View (Quarter vs. Annual):",
                "➤ Quarterly: Shows data for the specific quarter selected. This is used for filing BIR Form 1701Q (Income Tax) and BIR Form 2551Q (Percentage Tax).",
                "➤ Annual: Consolidates all four quarters to show your total year-end standing for BIR Form 1701/1701A.\n",
                "🟣 Year & Quarter: Select the specific taxable period you wish to review.\n",
                "🟢 Prior Paid: Select which quarters you have already paid for. The app uses this to calculate the \"Tax Payable\" by subtracting what you’ve already remitted to the BIR.\n"
            ]
        )

        # ================= SECTION B: Understanding Your Profile =================
        self.section(
            content,
            "2. Understanding Your Profile",
            [
                "The Profile Row shows your current tax settings, which dictate how the math is performed:\n",
                "🟢 Income Earner Type:",
                "➤ Pure Business: You receive the full ₱250,000 tax-exempt threshold on your business income.",
                "➤ Mixed-Income: The app assumes your salary uses the ₱250,000 threshold, so your business income is taxed from the very first peso.\n",
                "🟢 Tax Type: Displays if you are on the 8% Flat Rate or Graduated Rates.\n",
                "🟢 Deduction Method: Shows OSD (40%) or Itemized, which determines how your \"Net Taxable Income\" is calculated.\n"
            ]
        )

        # ================= SECTION C: Key Financial Cards =================
        self.section(
            content,
            "3. Key Financial Cards",
            [
                "Total Gross Income: Your total sales or receipts before any deductions.\n",
                "🟢 Total Deductions:",
                "➤ If OSD, this is 40% of your Gross Income.",
                "➤ If Itemized, this is your total documented business expenses.\n",
                "🟢 Net Taxable Income: The amount left after deductions. This is the figure that gets \"plugged into\" the 2026 tax table.\n",
                "Income Tax Due: The total income tax for the period based on your tax regime.\n",
                "🟢 Percentage Tax (3%):",
                "➤ If you chose Graduated Rates, this card shows your business tax.",
                "➤ If you chose 8%, this card will show \"Exempted\".\n",
            ]
        )

        # ================= SECTION D: Final Tax Payable Calculation =================
        self.section(
            content,
            "4. Final Tax Payable Calculation",
            [
                "The app calculates your final \"out-of-pocket\" payment using this flow:\n",
                "① Income Tax Due",
                "② Minus CWT (Income): Taxes already withheld by your clients (from BIR Form 2307).",
                "③ Minus Prior Paid Quarters: Taxes you already paid in earlier quarters of the same year.",
                "④ Income Tax Payable: The final amount you need to pay to the BIR. If this is negative, it indicates a Refundable amount (overpayment).\n"
            ]
        )

        # ================= DISCLAIMER =================
        tk.Label(
            content,
            text=(
                "⚠ Important Notice:\n"
                "This application is designed to help Non-VAT taxpayers organize income, expenses, and tax-related data "
                "in accordance with Philippine BIR filing requirements.\n\n"
                "The reports and summaries generated by this app are intended to assist in tax preparation and record-keeping.\n"
                "Final tax filing and submission must still be completed using eBIRForms or other BIR-approved platforms.\n"
            ),
            font=("Segoe UI", 11),
            bg="#040f21",
            fg="#e5e7eb",
            justify="left",
            wraplength=820
        ).pack(anchor="w", padx=20, pady=(30, 20))

        self.lift()
        self.focus_force()

    # ================= HELPERS =================
    def section(self, parent, title, items):
        tk.Label(
            parent,
            text=title,
            font=("Segoe UI", 15, "bold"),
            bg="#040f21",
            fg="#60a5fa"
        ).pack(anchor="w", padx=20, pady=(20, 10))

        for item in items:
            tk.Label(
                parent,
                text=f"{item}",
                font=("Segoe UI", 12),
                bg="#040f21",
                fg="#d1d5db",
                justify="left",
                wraplength=820
            ).pack(anchor="w", padx=40, pady=2)

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

        # Add offset corrections here (example: shift left by 10px, up by 5px)
        offset_x = -10
        offset_y = -55

        x = parent_x + (parent_w // 2) - (w // 2) + offset_x
        y = parent_y + (parent_h // 2) - (h // 2) + offset_y

        self.geometry(f"{w}x{h}+{x}+{y}")
