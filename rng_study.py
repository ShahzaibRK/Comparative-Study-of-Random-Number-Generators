import tkinter as tk
from tkinter import ttk, messagebox
import random
import secrets
import os
import time
import numpy as np
from scipy.stats import chisquare, kstest, entropy
import matplotlib.pyplot as plt

# RNG Functions
def prng_mersenne_twister(size):
    return [random.getrandbits(8) for _ in range(size)]

def csprng_secrets(size):
    return [secrets.randbits(8) for _ in range(size)]

def trng_urandom(size):
    return list(os.urandom(size))

def trng_random(size):
    with open('/dev/random', 'rb') as f:
        return list(f.read(size))

# Statistical Analysis
def analyze(data):
    arr = np.array(data)
    start_time = time.time()

    counts, _ = np.histogram(arr, bins=256, range=(0, 255))
    chisq_stat, chisq_p = chisquare(counts)
    ks_stat, ks_p = kstest(arr/255.0, 'uniform')
    ent = entropy(counts + 1e-10, base=2) / 8

    duration = time.time() - start_time
    return duration, ent * 8, chisq_stat, chisq_p, ks_stat, ks_p

# GUI Application
class RNGApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧪 RNG Comparative Study")
        self.geometry("800x600")
        self.configure(bg="#F5F5F5")

        self.selected_rngs = tk.Variable(value=["PRNG", "CSPRNG", "TRNG (/dev/urandom)", "TRNG (/dev/random)"])

        # UI Layout
        title = tk.Label(self, text="🧪 Comparative Study of RNGs for Cryptographic Applications", font=("Helvetica", 16, "bold"), bg="#F5F5F5")
        title.pack(pady=10)

        frame = tk.Frame(self, bg="#F5F5F5")
        frame.pack(pady=10)

        tk.Label(frame, text="Select RNGs to Test:", bg="#F5F5F5").grid(row=0, column=0, sticky="w")

        self.check_vars = {}
        options = ["PRNG", "CSPRNG", "TRNG (/dev/urandom)", "TRNG (/dev/random)"]
        for i, opt in enumerate(options):
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(frame, text=opt, var=var, bg="#F5F5F5")
            cb.grid(row=i+1, column=0, sticky="w")
            self.check_vars[opt] = var

        run_btn = tk.Button(self, text="▶️ Run Analysis", command=self.run_analysis, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        run_btn.pack(pady=10)

        self.result_text = tk.Text(self, height=15, width=90)
        self.result_text.pack(pady=10)

        plot_btn = tk.Button(self, text="📊 Plot Results", command=self.plot_results, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        plot_btn.pack(pady=5)

        self.results = {}

    def run_analysis(self):
        self.result_text.delete(1.0, tk.END)
        self.results = {}
        size = 10000

        selections = [opt for opt, var in self.check_vars.items() if var.get()]
        if not selections:
            messagebox.showerror("Error", "Select at least one RNG!")
            return

        self.result_text.insert(tk.END, "Running tests...\n\n")

        for rng in selections:
            if rng == "PRNG":
                data = prng_mersenne_twister(size)
            elif rng == "CSPRNG":
                data = csprng_secrets(size)
            elif rng == "TRNG (/dev/urandom)":
                data = trng_urandom(size)
            elif rng == "TRNG (/dev/random)":
                try:
                    data = trng_random(size)
                except Exception as e:
                    self.result_text.insert(tk.END, f"Error accessing /dev/random: {e}\n")
                    continue

            duration, entropy_val, chisq_stat, chisq_p, ks_stat, ks_p = analyze(data)
            self.results[rng] = {
                'Time': duration,
                'Entropy': entropy_val,
                'ChiSqStat': chisq_stat,
                'ChiSqP': chisq_p,
                'KSStat': ks_stat,
                'KSP': ks_p
            }

            self.result_text.insert(tk.END, f"--- {rng} ---\n")
            self.result_text.insert(tk.END, f"⏱ Time taken: {duration:.4f} sec\n")
            self.result_text.insert(tk.END, f"🔐 Entropy: {entropy_val:.4f} bits\n")
            self.result_text.insert(tk.END, f"🎲 Chi-square: {chisq_stat:.2f}, p-value={chisq_p:.4f}\n")
            self.result_text.insert(tk.END, f"📊 K-S test: statistic={ks_stat:.4f}, p-value={ks_p:.4f}\n\n")

        self.result_text.insert(tk.END, "✅ Analysis Completed!\n")

    def plot_results(self):
        if not self.results:
            messagebox.showerror("Error", "Run analysis first!")
            return

        labels = list(self.results.keys())
        entropy_vals = [self.results[r]['Entropy'] for r in labels]
        chisq_pvals = [self.results[r]['ChiSqP'] for r in labels]
        ks_pvals = [self.results[r]['KSP'] for r in labels]

        x = np.arange(len(labels))

        fig, axs = plt.subplots(3, 1, figsize=(10, 10))

        axs[0].bar(x, entropy_vals, color='skyblue')
        axs[0].set_title('Entropy Comparison')
        axs[0].set_xticks(x)
        axs[0].set_xticklabels(labels, rotation=45)

        axs[1].bar(x, chisq_pvals, color='lightgreen')
        axs[1].set_title('Chi-Square P-Values')
        axs[1].set_xticks(x)
        axs[1].set_xticklabels(labels, rotation=45)

        axs[2].bar(x, ks_pvals, color='salmon')
        axs[2].set_title('K-S Test P-Values')
        axs[2].set_xticks(x)
        axs[2].set_xticklabels(labels, rotation=45)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = RNGApp()
    app.mainloop()
