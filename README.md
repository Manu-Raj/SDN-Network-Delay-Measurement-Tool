#  SDN-Based Network Delay & Performance Measurement Tool

##  Overview

This project implements a **Software Defined Networking (SDN)** application using the **Ryu controller** and **Mininet emulator** to:

* Measure **network delay (RTT)**
* Measure **throughput (bandwidth using iperf)**
* Demonstrate **SDN-based traffic control (blocking policy)**

---

##  System Requirements (IMPORTANT)

This project is designed to run **preferably on Linux**.

###  Recommended Environment

* Ubuntu / Debian-based Linux system
* Python **3.9 (recommended for compatibility with Ryu & Mininet)**

###  Why Linux?

* Mininet relies on Linux kernel features (network namespaces, tc, etc.)
* Running on Windows/macOS may cause failures or require virtualization

---

##  Objectives

* Implement a **learning switch** using OpenFlow 1.3
* Measure **RTT using ICMP (ping)**
* Measure **throughput using iperf**
* Demonstrate **SDN policy enforcement (traffic blocking)**
* Analyze performance differences across network paths

---

##  Network Topology

```
h1 ---\
       \
        s1 -------- s2
       /             \
h2 ---/               \--- h3
                       \
                        \--- h4
```

###  Link Configuration

| Link  | Bandwidth | Delay |
| ----- | --------- | ----- |
| h1–s1 | 100 Mbps  | 5 ms  |
| h2–s1 | 100 Mbps  | 5 ms  |
| h3–s2 | 100 Mbps  | 5 ms  |
| h4–s2 | 100 Mbps  | 5 ms  |
| s1–s2 | 50 Mbps   | 10 ms |

---

##  Technologies Used

*  Python 3.9
*  Ryu SDN Controller
*  Mininet Network Emulator
*  OpenFlow 1.3
*  iperf

---

##  Project Structure

```
SDN-Network-Delay-Measurement-Tool/
│── src/
│   ├── controller.py      # Ryu controller (SDN logic)
│   ├── measure.py         # RTT + iperf measurement scripts
│   └── topology.py        # Mininet Topology
│── .gitignore
│── requirements.txt
└── README.md
```

---

##  How to Run

###  Step 1: Install Dependencies

```
sudo apt update
sudo apt install mininet iperf
pip install -r requirements.txt

```

---

###  Step 2: Start Controller (Terminal 1)

<img width="1273" height="332" alt="image" src="https://github.com/user-attachments/assets/69826f93-7ecc-48b0-adc8-dd7901f40000" />


```
ryu-manager src/controller.py
```

---

###  Step 3: Run Topology (Terminal 2)

<img width="1264" height="379" alt="image" src="https://github.com/user-attachments/assets/d88f1a6a-0f46-477b-b113-5fdd6e18f2a7" />


```
sudo python3 src/topology.py
```

---

##  Execution Modes (IMPORTANT)

The project supports **two modes**:

---

# 🟢 1. Normal Mode (Default)

<img width="1266" height="270" alt="image" src="https://github.com/user-attachments/assets/e3a3c061-b203-4c4e-b7fb-06b6015e80b0" />


All traffic is allowed.

### ✔ Configure:

In `controller.py`:

```python id="mg7i6h"
self.block_enabled = False
```

In `topology.py`:

```python id="2q91rc"
measure_iperf(net, block_enabled=False)
```

---

### ✔ Behavior

* All hosts communicate successfully
* `pingall` → 0% packet loss
* iperf runs for all test pairs

---

# 🔴 2. Blocking Mode (SDN Policy Demonstration)

<img width="1264" height="288" alt="image" src="https://github.com/user-attachments/assets/48c050d2-c762-446a-825a-132ce91a9606" />


The controller blocks:

```id="vx7q41"
h1 → h4 ❌
```

---

### ✔ Configure:

In `controller.py`:

```python id="shp6u8"
self.block_enabled = True
```

In `topology.py`:

```python id="iq3q3x"
measure_iperf(net, block_enabled=True)
```

---

### ✔ Behavior

| Communication | Result    |
| ------------- | --------- |
| h1 → h4       | ❌ Blocked |
| h4 → h1       | ✅ Allowed |
| Others        | ✅ Allowed |

---

###  Important Notes

* Blocking is **directional** (only h1 → h4)
* iperf test for blocked path is skipped to prevent hanging
* Controller dynamically drops packets matching rule

---

##  Performance Measurement

---

### 📡 RTT Measurement
Sample Output
<img width="592" height="206" alt="image" src="https://github.com/user-attachments/assets/ff4645ab-50bb-40b4-9fd4-229ec5249682" />


* Uses ICMP (`ping`)
* Extracts min / avg / max / packet loss

---

###  Throughput Measurement
Sample Output
<img width="588" height="158" alt="image" src="https://github.com/user-attachments/assets/6c3f3429-5338-4bf6-93c4-ecf1cca99286" />



* Uses `iperf`
* Shows bandwidth differences based on topology

---

##  Key Observations

* RTT increases with number of hops
* Throughput is limited by bottleneck link (50 Mbps)
* SDN enables dynamic traffic control
* Policy enforcement is achieved via OpenFlow rules

---
