from kiwi.core.bio_periphery import InstrumPeriphery


class Pipettor(InstrumPeriphery):
    def __init__(self):
        super().__init__()

    def prepare(self):
        pass

    def start(self):
        pass

    def shutdown(self):
        pass

    def tip_on(self):
        """ add tip to the pipettor """
        pass

    def tip_off(self):
        """ remove tip from pipettor """
        pass

    def move(self, pos):
        """ move pipettor to position """
        pass

    def suck_liquid(self):
        """ suck liquid to pipettor """
        pass

    def drop_liquid(self):
        """ drop liquid to the container """
        pass




