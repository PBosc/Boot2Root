# Boot2Root

Boot2Root is a Capture The Flag (CTF) challenge focused on **privilege escalation**.  
The goal is simple: **gain root access on a target server** — but do it in as many ways as possible.  

This repository contains detailed writeups for **six distinct exploitation paths**, covering both common and creative privilege escalation techniques.

---

## 📂 Repository Structure

```
.
├── writeup1.md       # First root method
├── writeup2.md       # Second root method
├── scripts/          # Helper scripts used in the exploits
└── bonus/
    ├── writeup3.md   # Third root method
    ├── writeup4.md   # Fourth root method
    ├── writeup5.md   # Fifth root method
    └── writeup6.md   # Sixth root method
```

---

## 🏹 Objective

The challenge is inspired by **Boot2Root-style VMs** commonly found in platforms like VulnHub or HackTheBox.  
Starting with **limited access** to a simulated server, the task is to:

1. Enumerate the system.
2. Identify vulnerabilities or misconfigurations.
3. Exploit them to escalate privileges.
4. Repeat using different techniques.

---

## ✨ Features

- **6 full exploitation paths** with step-by-step explanations.
- Includes **commands, payloads, and reasoning** behind each step.
- Practical examples of:
  - SUID abuse
  - Kernel exploits
  - Misconfigured services
  - Weak permissions
  - Password reuse
- **Helper scripts** to automate certain steps.

---

## 🔧 Requirements

- A Linux machine or VM to replicate the challenge.
- Basic pentesting tools (e.g., `netcat`, `nmap`, `python`, `gcc`).
- A vulnerable Boot2Root server (the one used in the challenge).

> **Note:** The target server is **not** included in this repository. You will need to set it up separately.

---

## 🚀 Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/PBosc/Boot2Root.git
   cd Boot2Root
   ```

2. **Read a writeup**  
   Start from `writeup1.md` or pick any method you want to try.

3. **Reproduce the attack**  
   Use the described commands and scripts to replicate the escalation.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**.  
Do **not** attempt these techniques on systems you do not own or have explicit permission to test.

