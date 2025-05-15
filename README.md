🧪 RNG Comparative Study GUI
A Python-based GUI tool to evaluate and compare different Random Number Generators (RNGs) for cryptographic applications. This application provides statistical analysis and visualization to assess the randomness quality of various RNG types.

📌 Features
✅ Graphical User Interface (Tkinter)

🔢 Supports:

PRNG (Mersenne Twister)

CSPRNG (secrets)

TRNG via /dev/urandom

TRNG via /dev/random

📈 Statistical analysis:

Entropy estimation

Chi-Square Test

Kolmogorov–Smirnov (K-S) Test

📊 Graphical visualization using Matplotlib

⚙️ Fast execution with clearly formatted results

🚀 Getting Started:
📦 Prerequisites
Make sure you have the following installed:
Python 3.7+
Required libraries:
pip install numpy scipy matplotlib

📁 Clone the Repository
git clone https://github.com/yourusername/rng-comparative-study.git
cd rng-comparative-study

▶️ Run the Application
python rng_gui.py
Note: Access to /dev/random may block if system entropy is low. You can deselect that option if needed.

