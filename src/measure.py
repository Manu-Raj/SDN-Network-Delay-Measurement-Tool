def measure_all(net):
    import re
    import time

    HOST_PAIRS = [
        ("h1", "10.0.0.2"),
        ("h1", "10.0.0.3"),
        ("h2", "10.0.0.4"),
        ("h3", "10.0.0.4"),
    ]

    PING_COUNT = 10

    def parse_rtt(output):
        match = re.search(
            r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)", output
        )
        loss = re.search(r"(\d+)% packet loss", output)

        if match:
            return {
                "min": float(match.group(1)),
                "avg": float(match.group(2)),
                "max": float(match.group(3)),
                "mdev": float(match.group(4)),
                "loss": int(loss.group(1)) if loss else 0,
            }
        return None

    print("\n=== RTT Measurement ===")
    print(f"{'Pair':<15} {'Min':>7} {'Avg':>7} {'Max':>7} {'Loss':>6}")
    print("-" * 50)

    for src, dst in HOST_PAIRS:
        host = net.get(src)
        output = host.cmd(f"ping -c {PING_COUNT} {dst}")

        rtt = parse_rtt(output)
        label = f"{src}->{dst}"

        if rtt:
            print(
                f"{label:<15} {rtt['min']:>6.2f} {rtt['avg']:>6.2f} "
                f"{rtt['max']:>6.2f} {rtt['loss']:>5}%"
            )
        else:
            print(f"{label:<15} FAILED")

        time.sleep(1)




def measure_iperf(net):
    import time
    import re

    print("\n=== Throughput Measurement (iperf) ===")
    print(f"{'Pair':<15} {'Bandwidth':>10}")
    print("-" * 30)

    tests = [
        ("h1", "h2"),
        ("h1", "h4"),
    ]

    for src, dst in tests:
        server = net.get(dst)
        client = net.get(src)

        server.cmd("iperf -s -p 5001 &")
        time.sleep(1)

        result = client.cmd(f"iperf -c {server.IP()} -p 5001 -t 5")

        # Extract bandwidth
        match = re.search(r"([\d.]+)\s+Mbits/sec", result)

        if match:
            bw = float(match.group(1))
            print(f"{src+'->'+dst:<15} {bw:>8.2f} Mbps")
        else:
            print(f"{src+'->'+dst:<15} FAILED")

        server.cmd("pkill -f iperf")
        time.sleep(1)