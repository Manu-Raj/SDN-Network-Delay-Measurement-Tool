from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import time


class DelayController(app_manager.RyuApp):
    # Use OpenFlow 1.3 protocol
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DelayController, self).__init__(*args, **kwargs)

        # MAC learning table: {dpid: {mac: port}}
        self.mac_to_port = {}

        # Stores timestamp when echo request was sent
        self.echo_sent = {}

        # Stores measured RTT per switch
        self.delay = {}

        # 🔥 FLAG: toggle blocking behavior
        self.block_enabled = True  # True = block h1 -> h4

    # ── Triggered when switch connects ─────────────────────────────
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        dpid = datapath.id

        # Initialize MAC table for this switch
        self.mac_to_port[dpid] = {}

        # ✅ Table-miss flow: send unknown packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]
        self.add_flow(datapath, 0, match, actions)

        self.logger.info("Switch connected: %s", dpid)

        # Log mode
        if self.block_enabled:
            self.logger.info("🔴 MODE: BLOCKING ENABLED")
        else:
            self.logger.info("🟢 MODE: NORMAL")

        # Send echo request to measure RTT
        self.send_echo(datapath)

    # ── Send Echo Request to switch (for RTT measurement) ──────────
    def send_echo(self, datapath):
        parser = datapath.ofproto_parser

        # Record current time
        now = time.time()
        self.echo_sent[datapath.id] = now

        # Send OpenFlow echo request
        req = parser.OFPEchoRequest(datapath, data=b'ping')
        datapath.send_msg(req)

    # ── Handle Echo Reply from switch ──────────────────────────────
    @set_ev_cls(ofp_event.EventOFPEchoReply, MAIN_DISPATCHER)
    def echo_reply_handler(self, ev):
        now = time.time()
        dpid = ev.msg.datapath.id

        # Calculate RTT if request was sent earlier
        if dpid in self.echo_sent:
            rtt = now - self.echo_sent[dpid]
            self.delay[dpid] = rtt
            self.logger.info("RTT to switch %s: %.6f sec", dpid, rtt)

    # ── Handle incoming packets (PacketIn event) ───────────────────
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Incoming port
        in_port = msg.match['in_port']

        # Parse packet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Ignore non-Ethernet packets
        if eth is None:
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        # 🚫 BLOCKING LOGIC: drop traffic from h1 → h4
        if self.block_enabled:
            if src == "00:00:00:00:00:01" and dst == "00:00:00:00:00:04":
                self.logger.info("🚫 Dropping packet: h1 -> h4")
                return  # DROP packet (no forwarding)

        # Ensure switch entry exists
        self.mac_to_port.setdefault(dpid, {})

        # Learn source MAC → port mapping
        self.mac_to_port[dpid][src] = in_port

        # Determine output port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]  # Known destination
        else:
            out_port = ofproto.OFPP_FLOOD  # Unknown → flood

        actions = [parser.OFPActionOutput(out_port)]

        # Install flow rule if destination is known (avoid future PacketIn)
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(
                in_port=in_port,
                eth_src=src,
                eth_dst=dst
            )
            self.add_flow(datapath, 10, match, actions)

        # Prepare packet data
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        # Send packet out
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)

    # ── Helper function to install flow rules ──────────────────────
    def add_flow(self, datapath, priority, match, actions):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Define instruction (apply actions)
        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions
        )]

        # Create flow mod message
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=30,   # removed if idle
            hard_timeout=120   # removed after fixed time
        )
        datapath.send_msg(mod)