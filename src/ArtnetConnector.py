from stupidArtnet import StupidArtnet

class ArtnetConnector:

    TARGET_IP = '192.168.178.165'             # typically in 2.x or 10.x range
    UNIVERSE_TO_SEND = 0                      # see docs
    PACKET_SIZE = 512                         # it is not necessary to send whole universe

    def __init__(self):
        self.artnet = StupidArtnet(target_ip=self.TARGET_IP, universe=self.UNIVERSE_TO_SEND, packet_size=self.PACKET_SIZE, artsync=True)
        self.artnet.start()

    def setDataSlot(self, channel, value):
        self.artnet.set_single_value(channel, value)
        self.artnet.show()

    def flashAll(self, delay):
        self.artnet.flash_all(delay)