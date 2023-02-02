class Rule:
    def __init__(self,protocol, srcIp, srcPort, dstIp, dstPort, rule):
        self.protocol = protocol
        self.srcIp = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.rule = rule
    def __eq__(self, other):
        if not isinstance(other, Rule):
            return NotImplemented
        return (self.protocol == other.protocol and 
                self.srcIp == other.srcIp and 
                self.srcPort == other.srcPort and 
                self.dstIp == other.dstIp and 
                self.dstPort == other.dstPort and 
                self.rule == other.rule)