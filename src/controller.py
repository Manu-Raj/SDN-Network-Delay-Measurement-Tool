from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import time


class DelayController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DelayController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.echo_sent = {}
        self.delay = {}

        # 🔥 FLAG: change this for demo
        self.block_enabled = True  # True = block h1 -> h4

    # ── Switch connects ─────────────────────────────
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        dpid = datapath.id

        self.mac_to_port[dpid] = {}

        # ✅ Table-miss flow
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(
            ofproto.OFPP_CONTROLLER,
            ofproto.OFPCML_NO_BUFFER
        )]
        self.add_flow(datapath, 0, match, actions)

        self.logger.info("Switch connected: %s", dpid)

        if self.block_enabled:
            self.logger.info("🔴 MODE: BLOCKING ENABLED")
        else:
            self.logger.info("🟢 MODE: NORMAL")

        # Send echo request
        self.send_echo(datapath)

    # ── Echo (delay measurement) ────────────────────
    def send_echo(self, datapath):
        parser = datapath.ofproto_parser
        now = time.time()
        self.echo_sent[datapath.id] = now

        req = parser.OFPEchoRequest(datapath, data=b'ping')
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPEchoReply, MAIN_DISPATCHER)
    def echo_reply_handler(self, ev):
        now = time.time()
        dpid = ev.msg.datapath.id

        if dpid in self.echo_sent:
            rtt = now - self.echo_sent[dpid]
            self.delay[dpid] = rtt
            self.logger.info("RTT to switch %s: %.6f sec", dpid, rtt)

    # ── PacketIn handler ────────────────────────────
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth is None:
            return

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        # 🚫 BLOCKING LOGIC (SAFE LOCATION)
        if self.block_enabled:
            if src == "00:00:00:00:00:01" and dst == "00:00:00:00:00:04":
                self.logger.info("🚫 Dropping packet: h1 -> h4")
                return  # DROP packet

        self.mac_to_port.setdefault(dpid, {})

        # Learn source MAC
        self.mac_to_port[dpid][src] = in_port

        # Decide output port
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install flow if destination known
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(
                in_port=in_port,
                eth_src=src,
                eth_dst=dst
            )
            self.add_flow(datapath, 10, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)

    # ── Add flow ────────────────────────────────────
    def add_flow(self, datapath, priority, match, actions):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions
        )]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst,
            idle_timeout=30,
            hard_timeout=120
        )
        datapath.send_msg(mod)