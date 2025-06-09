# SecureChat - Encrypted Client-Server Messaging 

![Chat App Interface](image.png)


A lightweight yet powerful chat application that prioritizes **security without sacrificing usability**. Built with **Python** and **SQLite**, SecureChat enables real-time communication with **end-to-end encryption** to keep your conversations private.

---

## Key Features

- **Military-Grade Encryption**  
  Messages are secured with **AES-256** encryption before leaving your device.

- **Zero Knowledge Architecture**  
  Even the server can’t read your messages—**only the intended recipient** can.

- **Encrypted Message History**  
  Stores conversations locally in an **encrypted SQLite database**.

- **Cross-Platform**  
  Runs on **Windows, macOS, and Linux** – anywhere Python does.

- **Lightweight**  
  Minimal dependencies and **no bloated frameworks**.

---

## Installation

Getting started takes less than 2 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/Dinesh230806/OIBSIP.git
cd OIBSIP

# 2. Set up a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate your encryption keys
python generate_key.py
