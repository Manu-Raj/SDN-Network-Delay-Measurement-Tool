#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from measure import measure_all, measure_iperf

import time


def create_topology():
    # Create Mininet instance with:
    # - Remote controller (Ryu)
    # - OVS switches
    # - Traffic-controlled links (delay, bandwidth)
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True  # auto assign MACs
    )

    info("*** Adding Controller\n")
    net.addController('c0', ip='127.0.0.1', port=6653)

    info("*** Adding Switches\n")
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')

    info("*** Adding Hosts\n")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    info("*** Creating Links\n")

    # Host ↔ Switch links (low delay, high bandwidth)
    net.addLink(h1, s1, delay='5ms', bw=100)
    net.addLink(h2, s1, delay='5ms', bw=100)
    net.addLink(h3, s2, delay='5ms', bw=100)
    net.addLink(h4, s2, delay='5ms', bw=100)

    # Inter-switch link (higher delay, lower bandwidth)
    net.addLink(s1, s2, delay='10ms', bw=50)

    # Start network
    net.start()
    net.waitConnected()

    # Print host info
    info("*** Hosts:\n")
    for h in net.hosts:
        info(f"{h.name}: {h.IP()} {h.MAC()}\n")

    time.sleep(2)

    # Run RTT measurements
    info("*** Running RTT Measurement...\n")
    measure_all(net)

    # Run throughput test (blocking enabled)
    info("*** Running Throughput Measurement...\n")
    measure_iperf(net, block_enabled=True)

    info("*** Ready 🚀\n")

    # Start Mininet CLI
    CLI(net)

    # Stop network after CLI exit
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    create_topology()