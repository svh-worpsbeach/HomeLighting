from stupidArtnet import StupidArtnet

import logging.handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

class ArtnetConnector:

    TARGET_IP = '192.168.178.197'             # typically in 2.x or 10.x range
    UNIVERSE_TO_SEND = 0                      # see docs
    PACKET_SIZE = 512                         # it is not necessary to send whole universe

    def __init__(self):
        self.artnet = StupidArtnet(target_ip=self.TARGET_IP, universe=self.UNIVERSE_TO_SEND, packet_size=self.PACKET_SIZE, artsync=True)
        self.artnet.start()

    def setDataSlot(self, channel, value, update):
        logger.debug(f"Setting single slot for channel {channel}\t--> {value}")
        self.artnet.set_single_value(channel, value)
        if update:
            self.artnet.show()

    def update(self):
        self.artnet.show()

    def setBulkDataSlots(self, basechannel, values, update):
        self.artnet.set_simplified_values(basechannel, values)

    def flashAll(self, delay):
        self.artnet.flash_all(delay)

    def update_data_slots(self, baseChannel, data):
        logger.debug(f"setting artnet buffer at address {baseChannel}")

        index = 0
        for dataPoint in data:
            self.artnet.set_single_value(baseChannel+index, dataPoint)
            index += 1

