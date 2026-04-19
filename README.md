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

###  Step 2: Start Controller 

```
ryu-manager src/controller.py
```

---

###  Step 3: Run Topology

```
sudo python3 src/topology.py
```

---

##  Execution Modes (IMPORTANT)

The project supports **two modes**:

---

# 🟢 1. Normal Mode (Default)

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

* Uses ICMP (`ping`)
* Extracts min / avg / max / packet loss

---

###  Throughput Measurement

* Uses `iperf`
* Shows bandwidth differences based on topology

---

##  Key Observations

* RTT increases with number of hops
* Throughput is limited by bottleneck link (50 Mbps)
* SDN enables dynamic traffic control
* Policy enforcement is achieved via OpenFlow rules

---
