from stupidArtnet import StupidArtnet

class ArtnetConnector:

    artnet = None

    TARGET_IP = '192.168.178.165'             # typically in 2.x or 10.x range
    UNIVERSE_TO_SEND = 0                      # see docs
    PACKET_SIZE = 512                         # it is not necessary to send whole universe

    def __init__(self):
        global artnet
        artnet = StupidArtnet(target_ip=self.TARGET_IP, universe=self.UNIVERSE_TO_SEND, packet_size=self.PACKET_SIZE, artsync=True)
        artnet.start()

    def setDataSlot(self, channel, value):
        artnet.set_single_value(channel, value)
        artnet.show()

    def flashAll(self, delay):
        artnet.flash_all(delay)
