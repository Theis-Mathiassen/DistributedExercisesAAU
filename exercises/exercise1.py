import random
from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here   
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._index = index
        self._number_of_devices = number_of_devices
        self._secrets = set([index])

    def run(self):
        #if (device != self.index()):
        x = 0
        while(True):
            if (x % 2 == 0):
                message = GossipMessage(self.index(), (self.index() + 1) % self.number_of_devices(), self._secrets)
            else:
                message = GossipMessage(self.index(), (self.index() - 1) % self.number_of_devices(), self._secrets)

            if message.destination != message.source:
                self.medium().send(message)
                
            
            while True:
                ingoing = self.medium().receive()
                if ingoing is None:
                    break
                self._secrets.update(ingoing.secrets)
            
            # this call is only used for synchronous networks
            self.medium().wait_for_next_round()
            
            
            # the following is your termination condition, but where should it be placed?
            if len(self._secrets) == self.number_of_devices():
                return
            x += 1

    def print_result(self):
        x = 0
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
