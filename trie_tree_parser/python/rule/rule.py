class Rule:
    def __init__(self,protocol, srcIp, srcPort, dstIp, dstPort, rule):
        self.protocol = protocol
        self.srcIp = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.rule = rule