import json 
import time
import sys

import logging.handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ShowRunner:

    def __init__(self, config_file, show):
        logger.debug(f"Initialize {__name__}")

    def play_steps_once(self, identifier, delay):
        logger.debug(f"playing {identifier} steps once")

        steps = self.show.get_steps(identifier)

        for s in steps:
             comment = s.get_comment()
             light = s.get_light()
             fixture = self.get_fixture(light)
             base = fixture.get_base_channel()
             
             for set in s.get_settings():
                chName = set.get_name()
                chValue = set.get_value()
                ch = fixture.get_channel_by_name(chName)
                chType = ch.get_type()

                if type(chValue) == 'str':
                    chValue = ch.get_value_by_name(chValue)

                offset = ch.get_offset()

                chValue = ch.verify_function_value(chType, chName, chValue)

                logger.debug(f"setting ch {chName}\t (ch-addr: {base} + {offset})\t --> {chValue}")
                self.ac.setDataSlot(base + offset, chValue)
                time.sleep(delay/1000)

    def play_steps_loop(self, identifier, delay):
        logger.debug(f"starting loop for {identifier} with playLoop set to {self.playLoop}")
        cnt = 0

        if self.show.showType == "loop":
            self.playLoop = True

        while self.playLoop:
            self.play_steps_once(identifier, delay)
            time.sleep(delay/1000)

            if self.loopCount != None:
                cnt += 1
                logger.debug(f"loop count: {cnt}")

                if cnt >= self.loopCount:
                    logger.debug(f"stopping loop at count: {cnt}")
                    self.playLoop = False
             
    def play_steps(self, identifier, delay):
        logger.debug(f"playng steps from {identifier}") 

        if delay > 0:
            delay = self.show.get_Parameter("defaultDelay")
            if self.show.showType == "sequence":
                self.play_steps_once(identifier, delay)
            elif self.show.showType == "loop":
                self.loopCount = self.show.get_Parameter("loopCount")
                self.play_steps_loop(identifier, delay)
        else:
            delay = 0
            self.play_steps_once(identifier, delay)