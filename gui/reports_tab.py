import tkinter as tk
import customtkinter as ctk
from core.storage import StorageManager
from datetime import datetime

TAX_EXEMPTION = 250_000


class ReportsTab(ctk.CTkFrame):
    def __init__(self, parent, storage: StorageManager, app_state):
        super().__init__(parent, fg_color="#040f21", corner_radius=0)

        self.storage = storage
        self.app_state = app_state

        BG_COLOR = "#2b3545"
        HOVER_COLOR = "#246ae3"
        TEXT_COLOR = "#ffffff"
        DISABLED_TEXT = "#9CA3AF"

        # ================= SCROLLABLE CONTENT =================
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True)
        self.bind("<Map>", lambda e: self.refresh_scroll())
        self.bind("<Visibility>", lambda e: self.refresh_scroll())

        # ================= HEADER =================
        header = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(20, 10))

        ctk.CTkLabel(header, text="Reports & Summary",
                     font=("Segoe UI", 26, "bold"),
                     text_color="#ffffff").pack(anchor="w")

        ctk.CTkLabel(header, text="Income, expenses, and tax overview",
                     font=("Segoe UI", 15),
                     text_color="#A0AEC0").pack(anchor="w")

        # ================= VARIABLES =================
        self.report_mode = tk.StringVar(value="Annual")
        self.selected_year = tk.StringVar(value=str(datetime.now().year))
        self.selected_quarter = tk.StringVar(value=self.get_current_quarter())
        self.prior_paid_quarters = tk.StringVar(value=self.get_prior_paid_quarters())
        self.report_mode.trace_add("write", self.update_mode_dependent_controls)



        # ================= CONTROLS =================
        controls = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        controls.pack(fill="x", padx=10, pady=(10, 10))

        ctk.CTkLabel(controls, text="View", text_color="#fff").grid(row=0, column=0, padx=6)
        self.view_dropdown = ctk.CTkOptionMenu(
            controls, values=["Quarter", "Annual"],
            variable=self.report_mode,
            command=lambda _: self.update_mode_dependent_controls(),
            width=120
        )
        self.view_dropdown.configure(
            fg_color=BG_COLOR,
            button_color=BG_COLOR,
            button_hover_color=HOVER_COLOR,
            dropdown_fg_color=BG_COLOR,
            dropdown_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR,
            text_color_disabled=DISABLED_TEXT
        )

        self.view_dropdown.grid(row=0, column=1, padx=6)

        ctk.CTkLabel(controls, text="Year", text_color="#fff").grid(row=0, column=2, padx=6)
        self.year_dropdown = ctk.CTkOptionMenu(
            controls, values=[],
            variable=self.selected_year,
            command=lambda _: self.update_mode_dependent_controls(),
            width=90
        )
        self.year_dropdown.configure(
            fg_color=BG_COLOR,
            button_color=BG_COLOR,
            button_hover_color=HOVER_COLOR,
            dropdown_fg_color=BG_COLOR,
            dropdown_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR,
            text_color_disabled=DISABLED_TEXT
        )

        self.year_dropdown.grid(row=0, column=3, padx=6)

        ctk.CTkLabel(controls, text="Quarter", text_color="#fff").grid(row=0, column=4, padx=6)
        self.quarter_dropdown = ctk.CTkOptionMenu(
            controls, values=["Q1", "Q2", "Q3", "Q4"],
            variable=self.selected_quarter,
            command=lambda _: self.refresh(),
            width=90
        )
        self.quarter_dropdown.configure(
            fg_color=BG_COLOR,
            button_color=BG_COLOR,
            button_hover_color=HOVER_COLOR,
            dropdown_fg_color=BG_COLOR,
            dropdown_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR,
            text_color_disabled=DISABLED_TEXT
        )

        self.quarter_dropdown.grid(row=0, column=5, padx=6)

        ctk.CTkLabel(controls, text="Prior Paid", text_color="#fff").grid(row=0, column=6, padx=6)
        self.prior_dropdown = ctk.CTkOptionMenu(
            controls,
            values=["None", "Q1", "Q1-Q2", "Q1-Q3"],  # options for what’s already paid
            variable=self.prior_paid_quarters,
            command=lambda _: self.refresh(),  # refresh totals when changed
            width=100
        )
        self.prior_dropdown.configure(
            fg_color=BG_COLOR,
            button_color=BG_COLOR,
            button_hover_color=HOVER_COLOR,
            dropdown_fg_color=BG_COLOR,
            dropdown_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR,
            text_color_disabled=DISABLED_TEXT
        )
        self.prior_dropdown.grid(row=0, column=7, padx=6)

        self.load_report_years()

        # ================= PROFILE ROW =================
        self.profile_row = ctk.CTkFrame(self.scroll_container, fg_color="#0f172a")
        self.profile_row.pack(fill="x", padx=20, pady=(20, 20))  # Increased padding to create more space

        self.profile_labels = {}

        def profile_item(label):
            frame = ctk.CTkFrame(self.profile_row, fg_color="transparent")
            frame.pack(side="left", padx=0, pady=(20,20), expand=True)
            # Add the label
            ctk.CTkLabel(frame, text=label, text_color="#94a3b8", font=("Segoe UI", 13)).pack(anchor="w")

            # Add the value field
            value = ctk.CTkLabel(frame, text="-", text_color="#fff", font=("Segoe UI", 19, "bold"))
            value.pack(anchor="w")

            # Store the value label for future reference
            self.profile_labels[label] = value

        # Create the profile items
        profile_item("Income Earner Type")
        profile_item("Tax Type")
        profile_item("Deduction Method")

        # ================= CARDS =================
        self.cards = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.cards.pack(fill="x", padx=20, pady=(0, 40))

        self.card_values = {}

        def card_row():
            row = ctk.CTkFrame(self.cards, fg_color="transparent")
            row.pack(fill="x", pady=6)
            return row

        def create_card(parent, title):
            card = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=12)
            card.pack(side="left", expand=True, fill="both", padx=6, pady=(0,10))

            ctk.CTkLabel(card, text=title, text_color="#9CA3AF").pack(
                anchor="w", padx=20, pady=(10, 0)
            )

            value = ctk.CTkLabel(
                card, text="₱0.00",
                font=("Segoe UI", 22, "bold"),
                text_color="#ffffff"
            )
            value.pack(anchor="w", padx=20, pady=(5, 25))

            self.card_values[title] = value

        # ROW 1 – MAIN
        row_main = card_row()
        for title in [
            "Total Gross Income",
            "Total Gross Expense",
            "Total Deductions",
            "Net Taxable Income",
            "Income Tax Due"
        ]:
            create_card(row_main, title)

        # ROW 2 – PERCENTAGE TAX
        row_pct = card_row()
        create_card(row_pct, "Percentage Tax (3%)")

        # ROW 3 – PAYABLE
        row_pay = card_row()
        create_card(row_pay, "Less: CWT (Income)")
        create_card(row_pay, "Less: Prior Paid Quarters")
        create_card(row_pay, "Income Tax Payable / (Refundable)")

        # ROW 4 - WT
        row_wt = card_row()
        create_card(row_wt, "WT (Expenses)")

        # ================= AUTO LOAD REPORT ON OPEN =================
        # Wait until UI is fully drawn, then refresh once
        self.after(100, self.refresh)

        # After UI setup
        self.update_mode_dependent_controls()

    # ================= HELPERS =================
    def load_report_years(self):
        rows = self.storage.cursor.execute("""
            SELECT DISTINCT strftime('%Y', date) as year
            FROM (SELECT date FROM income UNION ALL SELECT date FROM expense)
            ORDER BY year DESC
        """).fetchall()

        years = [r["year"] for r in rows]
        current_year = str(datetime.now().year)
        if current_year not in years:
            years.insert(0, current_year)

        self.year_dropdown.configure(values=years)
        self.selected_year.set(current_year)

    def get_current_quarter(self):
        m = datetime.now().month
        return "Q1" if m <= 3 else "Q2" if m <= 6 else "Q3" if m <= 9 else "Q4"

    def get_prior_paid_quarters(self):
        """Return default prior paid dropdown value based on mode."""
        if self.report_mode.get() == "Annual":
            return "Q1-Q3"  # default prior paid for annual filing
        else:
            # Quarter mode: dropdown is disabled anyway, so any default works
            return "None"

    def update_mode_dependent_controls(self, *args):
        # Quarter dropdown
        self.quarter_dropdown.configure(state="disabled" if self.report_mode.get() == "Annual" else "normal")
        # Prior paid dropdown
        self.prior_dropdown.configure(state="disabled" if self.report_mode.get() == "Quarter" else "normal")
        # Refresh after both states updated
        self.refresh()

    def calculate_graduated_tax(self, taxable_income):
        if taxable_income <= 250_000:
            return 0.0
        elif taxable_income <= 400_000:
            return (taxable_income - 250_000) * 0.15
        elif taxable_income <= 800_000:
            return 22_500 + (taxable_income - 400_000) * 0.20
        elif taxable_income <= 2_000_000:
            return 102_500 + (taxable_income - 800_000) * 0.25
        elif taxable_income <= 8_000_000:
            return 402_500 + (taxable_income - 2_000_000) * 0.30
        else:
            return 2_202_500 + (taxable_income - 8_000_000) * 0.35

    # ================= REFRESH =================
    def refresh_scroll(self):
        self.scroll_container.update_idletasks()

        canvas = self.scroll_container.winfo_children()[0]
        canvas.configure()

    def refresh(self):
        try:
            year = int(self.selected_year.get())
            quarter = self.selected_quarter.get()
            # paid = self.prior_paid_quarters.get()
            mode = self.report_mode.get()
        except Exception:
            return

        self.refresh_scroll()

        earner_type = self.app_state.earner_type
        tax_type = self.app_state.tax_type
        deduction_type = self.app_state.deduction_type

        # PROFILE
        self.profile_labels["Income Earner Type"].configure(
            text="Mixed Income Earner" if earner_type == "mixed" else "Sole Proprietor"
        )
        self.profile_labels["Tax Type"].configure(
            text="8% Flat Tax" if tax_type == "8_percent" else "Graduated Tax"
        )
        if tax_type == "8_percent":
            self.profile_labels["Deduction Method"].configure(text="Not Applicable")
        else:
            self.profile_labels["Deduction Method"].configure(
                text="OSD (40%)" if deduction_type == "osd" else "Itemized"
            )

        annual = self.storage.get_annual_summary(year)
        quarter_data = self.storage.get_quarter_summary(year, quarter)

        if mode == "Quarter":
            gross_income = quarter_data["gross_income"]
            gross_expense = quarter_data["gross_expense"]
            cwt = quarter_data["cwt_current_quarter"]
            wt = quarter_data["wt"]
        else:
            gross_income = annual["gross_income"]
            gross_expense = annual["gross_expense"]
            cwt = annual["cwt"]
            wt = annual["wt"]

        # DEDUCTIONS
        if tax_type == "8_percent":
            deductions = 0
        else:
            if deduction_type == "osd":
                deductions = gross_income * 0.40
            else:
                deductions = min(gross_expense, gross_income)  # 🔒 CAP itemized deductions

        # TAXABLE & TAX
        if tax_type == "8_percent":
            taxable = gross_income if earner_type == "mixed" else max(0, gross_income - TAX_EXEMPTION)
            income_tax = taxable * 0.08
            percentage_tax = "Status: Exempted"

        else:
            taxable = max(0, gross_income - deductions)
            income_tax = self.calculate_graduated_tax(
                (taxable + TAX_EXEMPTION) if earner_type == "mixed" else taxable
            )
            percentage_tax = (
                f"₱{gross_income * 0.03:,.2f}" if mode == "Quarter" else f"Filed Quarterly (Q1-Q4)"
            )

        # Helper to compute tax for a given quarter
        def calc_quarter_tax(qdata):
            if tax_type == "8_percent":
                return (qdata["gross_income"] if earner_type == "mixed" else max(0, qdata[
                    "gross_income"] - TAX_EXEMPTION)) * 0.08
            else:
                if deduction_type == "osd":
                    deductions = qdata["gross_income"] * 0.40
                else:
                    deductions = min(qdata["gross_expense"], qdata["gross_income"])

                taxable = max(0, qdata["gross_income"] - deductions)
                return self.calculate_graduated_tax(taxable + TAX_EXEMPTION if earner_type == "mixed" else taxable)

        if mode == "Annual":
            # Get quarter data
            q1 = self.storage.get_quarter_summary(year, "Q1")
            q2 = self.storage.get_quarter_summary(year, "Q2")
            q3 = self.storage.get_quarter_summary(year, "Q3")

            # Compute tax per quarter
            q1_tax_due = calc_quarter_tax(q1)
            q2_tax_due = calc_quarter_tax(q2)
            q3_tax_due = calc_quarter_tax(q3)

            # Map dropdown selection to prior paid total
            prior_mapping = {
                "None": 0,
                "Q1": q1_tax_due,
                "Q1-Q2": q1_tax_due + q2_tax_due,
                "Q1-Q3": q1_tax_due + q2_tax_due + q3_tax_due,
            }

            prior_paid = prior_mapping.get(self.prior_paid_quarters.get(), 0)
        else:
            prior_paid = 0  # quarter mode ignores prior paid

        # Compute Income Tax Payable
        payable = income_tax - cwt - prior_paid

        # UPDATE CARDS
        self.card_values["Total Gross Income"].configure(text=f"₱{gross_income:,.2f}")
        self.card_values["Total Gross Expense"].configure(text=f"₱{gross_expense:,.2f}")
        self.card_values["Total Deductions"].configure(
            text="--------" if tax_type == "8_percent" else f"₱{deductions:,.2f}"
        )
        self.card_values["Net Taxable Income"].configure(text=f"₱{taxable:,.2f}")
        self.card_values["Income Tax Due"].configure(text=f"₱{income_tax:,.2f}")
        self.card_values["Percentage Tax (3%)"].configure(text=percentage_tax)
        self.card_values["Less: CWT (Income)"].configure(text=f"₱{cwt:,.2f}")
        self.card_values["Less: Prior Paid Quarters"].configure(text=f"₱{prior_paid:,.2f}")
        self.card_values["WT (Expenses)"].configure(text=f"₱{wt:,.2f}")
        self.card_values["Income Tax Payable / (Refundable)"].configure(text=f"₱{payable:,.2f}")
