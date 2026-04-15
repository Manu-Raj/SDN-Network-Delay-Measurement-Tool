#  SDN-Based Network Delay & Performance Measurement Tool

## 📌 Problem Statement

In computer networks, measuring **latency (delay)** and **throughput (bandwidth)** is essential for analyzing performance and ensuring efficient communication.

This project implements an **SDN-based network monitoring tool** using:

- Ryu Controller
- Mininet Emulator

The system is designed to:

- Measure **Round Trip Time (RTT)** using ICMP (ping)
- Measure **throughput** using iperf
- Analyze **delay variations across different paths**
- Demonstrate **SDN-based traffic control (blocking policy)**

---

## ⚠️ System Requirements (IMPORTANT)

This project is designed to run **preferably on Linux**.

### 🐧 Recommended Environment

* Ubuntu / Debian-based Linux system
* Python **3.9 (recommended for compatibility with Ryu & Mininet)**

### ❗ Why Linux?

* Mininet relies on Linux kernel features (network namespaces, tc, etc.)
* Running on Windows/macOS may cause failures or require virtualization

---

## 🎯 Objectives

* Implement a **learning switch** using OpenFlow 1.3
* Measure **RTT using ICMP (ping)**
* Measure **throughput using iperf**
* Demonstrate **SDN policy enforcement (traffic blocking)**
* Analyze performance differences across network paths

---

## 🏗️ Network Topology

```
h1 ---\
       \
        s1 -------- s2
       /             \
h2 ---/               \--- h3
                       \
                        \--- h4
```

### 🔗 Link Configuration

| Link  | Bandwidth | Delay |
| ----- | --------- | ----- |
| h1–s1 | 100 Mbps  | 5 ms  |
| h2–s1 | 100 Mbps  | 5 ms  |
| h3–s2 | 100 Mbps  | 5 ms  |
| h4–s2 | 100 Mbps  | 5 ms  |
| s1–s2 | 50 Mbps   | 10 ms |

---

## ⚙️ System Requirements

- OS: Ubuntu / Linux (Recommended)
- Python: 3.9
- Tools:
  - Mininet
  - Ryu Controller
  - iperf

---

## 📂 Project Structure

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

## 🚀 How to Run

### 🔧 Step 1: Install Dependencies

```
sudo apt update
sudo apt install mininet iperf
pip install -r requirements.txt

```

---

### ▶️ Step 2: Start Controller (Terminnal 1)

```
ryu-manager src/controller.py
```

---

### ▶️ Step 3: Run Topology  (Terminnal 2)

```
sudo python3 src/topology.py
```

---

## 🧪 Execution Modes (IMPORTANT)

The project supports **two modes**:

---

### 🟢 1. Normal Mode (Default)

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

### 🔴 2. Blocking Mode (SDN Policy Demonstration)

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

### ⚠️ Important Notes

* Blocking is **directional** (only h1 → h4)
* iperf test for blocked path is skipped to prevent hanging
* Controller dynamically drops packets matching rule

---

## 📊 Performance Measurement

---

### 📡 RTT Measurement

* Uses ICMP (`ping`)
* Extracts min / avg / max / packet loss

---

### 🚀 Throughput Measurement

* Uses `iperf`
* Shows bandwidth differences based on topology

---

## 🧠 Key Observations

* RTT increases with number of hops
* Throughput is limited by bottleneck link (50 Mbps)
* SDN enables dynamic traffic control
* Policy enforcement is achieved via OpenFlow rules

---

## ⚠️ Common Notes

* `sch_htb quantum` warnings can be ignored
* Always start controller before topology
* Ensure Python 3.9 environment

---

## 🎤 Viva Highlights

* OpenFlow match-action model
* Flow priority and rule overriding
* RTT vs throughput difference
* SDN control plane vs data plane

---

## 📸 Screenshots

Include:

* Topology running
* RTT output
* iperf output
* Blocking demonstration

---

## 🏁 Conclusion

This project demonstrates how SDN enables:

* Programmable networks
* Performance monitoring
* Dynamic policy enforcement

---

## 👨‍💻 Author

Manu

---
