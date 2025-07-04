import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter Dashboard")
        self.root.geometry("1200x700")
        
        # Currency data (exchange rates relative to USD as base)
        self.currency_data = {
            "USD": {"name": "US `Dollar", "rate": 1.0, "country": "United States", "symbol": "$"},
            "EUR": {"name": "Euro", "rate": 0.93, "country": "European Union", "symbol": "€"},
            "GBP": {"name": "British Pound", "rate": 0.79, "country": "United Kingdom", "symbol": "£"},
            "JPY": {"name": "Japanese Yen", "rate": 156.5, "country": "Japan", "symbol": "¥"},
            "AUD": {"name": "Australian Dollar", "rate": 1.51, "country": "Australia", "symbol": "A$"},
            "CAD": {"name": "Canadian Dollar", "rate": 1.36, "country": "Canada", "symbol": "C$"},
            "CHF": {"name": "Swiss Franc", "rate": 0.89, "country": "Switzerland", "symbol": "Fr"},
            "CNY": {"name": "Chinese Yuan", "rate": 7.25, "country": "China", "symbol": "¥"},
            "INR": {"name": "Indian Rupee", "rate": 83.45, "country": "India", "symbol": "₹"},
            "MXN": {"name": "Mexican Peso", "rate": 18.20, "country": "Mexico", "symbol": "$"}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frames
        control_frame = tk.Frame(self.root, padx=10, pady=10, bd=1, relief=tk.RIDGE)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        
        dashboard_frame = tk.Frame(self.root, padx=10, pady=10, bd=1, relief=tk.RIDGE)
        dashboard_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        # Conversion controls
        tk.Label(control_frame, text="Currency Converter", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(control_frame, text="Amount:").grid(row=1, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(control_frame, width=15)
        self.amount_entry.grid(row=1, column=1, pady=5)
        self.amount_entry.insert(0, "1.00")
        
        tk.Label(control_frame, text="From Currency:").grid(row=2, column=0, sticky="w", pady=5)
        self.from_currency = ttk.Combobox(control_frame, values=list(self.currency_data.keys()), width=12)
        self.from_currency.grid(row=2, column=1, pady=5)
        self.from_currency.set("USD")
        
        tk.Label(control_frame, text="To Currency:").grid(row=3, column=0, sticky="w", pady=5)
        self.to_currency = ttk.Combobox(control_frame, values=list(self.currency_data.keys()), width=12)
        self.to_currency.grid(row=3, column=1, pady=5)
        self.to_currency.set("EUR")
        
        convert_btn = tk.Button(control_frame, text="Convert", command=self.convert_currency, bg="#4CAF50", fg="white")
        convert_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.result_var = tk.StringVar()
        tk.Label(control_frame, textvariable=self.result_var, font=("Arial", 12), wraplength=200).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Comparison controls
        separator = ttk.Separator(control_frame, orient='horizontal')
        separator.grid(row=6, column=0, columnspan=2, sticky='ew', pady=15)
        
        tk.Label(control_frame, text="Currency Comparison", font=("Arial", 12, "bold")).grid(row=7, column=0, columnspan=2, pady=5)
        
        tk.Label(control_frame, text="Currency 1:").grid(row=8, column=0, sticky="w", pady=5)
        self.comp_currency1 = ttk.Combobox(control_frame, values=list(self.currency_data.keys()), width=12)
        self.comp_currency1.grid(row=8, column=1, pady=5)
        self.comp_currency1.set("USD")
        
        tk.Label(control_frame, text="Currency 2:").grid(row=9, column=0, sticky="w", pady=5)
        self.comp_currency2 = ttk.Combobox(control_frame, values=list(self.currency_data.keys()), width=12)
        self.comp_currency2.grid(row=9, column=1, pady=5)
        self.comp_currency2.set("EUR")
        
        compare_btn = tk.Button(control_frame, text="Compare", command=self.compare_currencies, bg="#2196F3", fg="white")
        compare_btn.grid(row=10, column=0, columnspan=2, pady=10)
        
        self.comparison_var = tk.StringVar()
        tk.Label(control_frame, textvariable=self.comparison_var, font=("Arial", 10), wraplength=200).grid(row=11, column=0, columnspan=2, pady=10)
        
        # Dashboard setup
        self.setup_dashboard(dashboard_frame)
        
    def setup_dashboard(self, parent):
        # Create dashboard with 3 visualization panels
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create initial empty plots
        self.update_dashboard("USD", "EUR")
        
    def update_dashboard(self, currency1, currency2):
        self.fig.clear()
        
        # Get currency data
        c1 = self.currency_data[currency1]
        c2 = self.currency_data[currency2]
        currencies = list(self.currency_data.keys())
        values = [1 / self.currency_data[c]['rate'] for c in currencies]  # Value in USD
        
        # 1. Currency Strength Comparison
        ax1 = self.fig.add_subplot(221)
        bars = ax1.bar([currency1, currency2], [1/c1['rate'], 1/c2['rate']], color=['#1f77b4', '#ff7f0e'])
        ax1.set_title(f'Currency Strength Comparison ({currency1} vs {currency2})')
        ax1.set_ylabel('Value in USD')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.4f}',
                     ha='center', va='bottom')
        
        # 2. All Currencies Value Chart
        ax2 = self.fig.add_subplot(222)
        colors = ['#1f77b4' if c != currency1 and c != currency2 else 
                 ('#d62728' if c == currency1 else '#2ca02c') for c in currencies]
        ax2.bar(currencies, values, color=colors)
        ax2.set_title('All Currencies Value (USD Equivalent)')
        ax2.set_ylabel('Value of 1 Unit in USD')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # 3. Percentage Difference Radial Chart
        ax3 = self.fig.add_subplot(223, polar=True)
        strength_ratio = (1/c1['rate']) / (1/c2['rate'])
        if strength_ratio < 1:
            strength_ratio = 1 / strength_ratio
            stronger, weaker = currency2, currency1
        else:
            stronger, weaker = currency1, currency2
            
        percentage = (strength_ratio - 1) * 100
        
        # Create radial chart
        theta = np.linspace(0, 2 * np.pi, 100)
        r = np.linspace(0, 1, 100)
        ax3.plot(theta, np.ones_like(theta), 'k--')
        ax3.fill_between(theta, 0, strength_ratio/10, alpha=0.3, color='green')
        ax3.set_yticklabels([])
        ax3.set_title(f'{stronger} is {percentage:.1f}% stronger than {weaker}', pad=20)
        
        # 4. Country Information
        ax4 = self.fig.add_subplot(224)
        ax4.axis('off')
        info_text = (f"{c1['country']} ({currency1}):\n"
                    f"1 {currency1} = {1/c1['rate']:.4f} USD\n\n"
                    f"{c2['country']} ({currency2}):\n"
                    f"1 {currency2} = {1/c2['rate']:.4f} USD\n\n"
                    f"Conversion Rate:\n"
                    f"1 {currency1} = {c2['rate']/c1['rate']:.4f} {currency2}\n"
                    f"1 {currency2} = {c1['rate']/c2['rate']:.4f} {currency1}")
        ax4.text(0.5, 0.5, info_text, ha='center', va='center', 
                fontsize=12, bbox=dict(facecolor='#f0f0f0', alpha=0.5))
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_cur = self.from_currency.get()
            to_cur = self.to_currency.get()
            
            if from_cur not in self.currency_data or to_cur not in self.currency_data:
                messagebox.showerror("Error", "Invalid currency selection")
                return
                
            # Convert via USD as base
            usd_amount = amount / self.currency_data[from_cur]['rate']
            converted = usd_amount * self.currency_data[to_cur]['rate']
            
            self.result_var.set(
                f"{amount:.2f} {from_cur} = {converted:.2f} {to_cur}\n"
                f"({self.currency_data[from_cur]['symbol']}{amount:.2f} → "
                f"{self.currency_data[to_cur]['symbol']}{converted:.2f})"
            )
            
            # Update dashboard with conversion pair
            self.update_dashboard(from_cur, to_cur)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered")
    
    def compare_currencies(self):
        currency1 = self.comp_currency1.get()
        currency2 = self.comp_currency2.get()
        
        if currency1 not in self.currency_data or currency2 not in self.currency_data:
            messagebox.showerror("Error", "Invalid currency selection")
            return
            
        # Calculate strength comparison
        strength1 = 1 / self.currency_data[currency1]['rate']
        strength2 = 1 / self.currency_data[currency2]['rate']
        
        if strength1 > strength2:
            stronger = currency1
            weaker = currency2
            percentage = (strength1 - strength2) / strength2 * 100
        else:
            stronger = currency2
            weaker = currency1
            percentage = (strength2 - strength1) / strength1 * 100
            
        self.comparison_var.set(
            f"{stronger} is {percentage:.2f}% stronger than {weaker}\n"
            f"1 {stronger} = {strength1/strength2 if stronger==currency1 else strength2/strength1:.4f} {weaker}\n"
            f"Country: {self.currency_data[stronger]['country']} vs {self.currency_data[weaker]['country']}"
        )
        
        # Update dashboard with comparison pair
        self.update_dashboard(currency1, currency2)

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop() 