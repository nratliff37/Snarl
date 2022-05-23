from abc import ABC, abstractmethod

#
# Represents a User
#
class UserClient(ABC):

    @abstractmethod
    def begin_turn(self, message):
        pass
     

    @abstractmethod
    def send_message(self):
        pass
       
    @abstractmethod
    def receive_update(self, update):
        pass

    @abstractmethod
    def render(self):
        pass

    

    