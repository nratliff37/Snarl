from abc import ABC, abstractmethod

#
# Represents a Observer 
#
class ObserverClient(ABC):
       
    @abstractmethod
    def update(self, update):
        pass

    @abstractmethod
    def render(self):
        pass

    

    