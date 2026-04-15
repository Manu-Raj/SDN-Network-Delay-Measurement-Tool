# 📡 Network Delay Measurement and Analysis using Mininet & Ryu

## 🧾 Overview
This project implements a Software-Defined Networking (SDN)-based Network Delay Measurement Tool using **Mininet** and the **Ryu controller**. The system measures, analyzes, and compares latency across different hosts in a simulated network topology.

It integrates both:
- **Data Plane Measurement** using ICMP (ping)
- **Control Plane Measurement** using OpenFlow Echo messages

---

## 🎯 Objectives
- Measure Round Trip Time (RTT) between hosts
- Analyze latency variations across network paths
- Implement SDN-based flow control using Ryu
- Simulate realistic network conditions using Mininet

---

## 🏗️ Project Structure
```
network-delay-measurement/
│── src/
│   ├── controller.py      # Ryu SDN Controller
│   ├── measure.py         # RTT Measurement Script
│   └── topology.py        # Mininet Topology
│── README.md
│── requirements.txt
```

---

## ⚙️ Technologies Used
- Python 3
- Mininet
- Ryu SDN Controller
- OpenFlow 1.3
- Linux Networking Tools (ping)

---

## 🌐 Network Topology
- **2 OpenFlow switches** (s1, s2)
- **4 hosts** (h1–h4)
- Controlled delay and bandwidth links:
  - Host ↔ Switch: 5 ms
  - Switch ↔ Switch: 10 ms

This allows comparison between intra-switch and inter-switch delays.

---

## 🧠 System Design

### 1. SDN Controller (Ryu)
- Implements a **learning switch**
- Installs flow rules dynamically
- Handles packet forwarding
- Measures **controller-to-switch latency** using OpenFlow Echo

### 2. Delay Measurement Module
- Uses ICMP ping to compute:
  - Minimum RTT
  - Average RTT
  - Maximum RTT
  - Packet loss
- Parses and displays results in tabular format

### 3. Metrics Collected
- RTT (min/avg/max)
- Packet loss
- Delay variation (mdev)

---

## 🚀 How to Run

### 1. Start Ryu Controller
```
ryu-manager src/controller.py
```

### 2. Run Mininet Topology
```
sudo python3 src/topology.py
```

### 3. Run Measurements (inside Mininet CLI)
```
python3 src/measure.py
```

---

## 📊 Sample Output
```
=== RTT Measurement ===
Pair            Min     Avg     Max   Loss
--------------------------------------------------
h1->10.0.0.2   5.12    5.30    5.60    0%
h1->10.0.0.3  15.20   15.45   15.80    0%
```

---

## 📈 Key Observations
- Hosts on the same switch show lower latency
- Inter-switch communication introduces additional delay
- Network delay reflects configured link parameters accurately
- Controller echo RTT represents control-plane latency

---

## 🧪 Features
- Dynamic flow installation
- Real-time RTT measurement
- Multi-path latency comparison
- Structured output reporting
- Configurable network parameters

---

## ⚠️ Limitations
- No graphical visualization of results
- No adaptive routing based on delay
- Echo requests are not periodic (single measurement per connection)

---

## 🔮 Future Improvements
- Implement delay-aware routing
- Add real-time monitoring dashboard
- Integrate matplotlib for visualization
- Extend topology with multiple paths

---

## 📚 References
- Mininet Documentation: http://mininet.org/
- Ryu Documentation: https://osrg.github.io/ryu/
- OpenFlow Specification

"# SDN-Network-Delay-Measurement-Tool" 
