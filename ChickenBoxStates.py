from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt
from enum import Enum
import sys

import toml

with open('config.toml', 'r') as f:
    config = toml.load(f)

mqttserver = config['chickenbox']['mqttserver']

class DoorIds(Enum):
    FRONT = 1
    EXIT = 2

def open_door(door_id : DoorIds):
    #TODO: implement code
    pass

def close_door(door_id : DoorIds):
    #TODO: implement code
    pass

def start_experiment():
    #TODO: implement call to experiment
    pass

class ChickenBoxManager():
    def __init__(self):
        self.state = StartState(self)

        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message = self.on_message

        self.mqtt_client.connect(mqttserver['url'], 1883, 60)
        self.mqtt_client.loop_forever()

    def on_message(self, client, userdata, message):
        print("Message received: " + message.payload.decode())

        #TODO: implement actual message handling
        if message.payload.decode() == "chicken_detected_in_box":
            self.chicken_detected_in_box()
            
        if message.payload.decode() == "chicken_exited_box":
            self.chicken_exited_box()

    def chicken_detected_in_box(self):
        self.state.chicken_detected_in_box()
    
    def chicken_exited_box(self):
        self.state.chicken_exited_box()

    def experiment_finished(self):
        self.state.experiment_finished()

class ChickenBoxState(ABC):
    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    def chicken_detected_in_box(self):
        pass
    
    @abstractmethod
    def chicken_exited_box(self):
        pass
    
    @abstractmethod
    def experiment_finished(self):
        pass

class StartState(ChickenBoxState):
    def __init__(self, manager):
        super().__init__(manager)

    def chicken_detected_in_box(self):
        close_door(DoorIds.FRONT)
        self.manager.state = ExperimentState(self.manager)

    def chicken_exited_box(self):
        pass

    def experiment_finished(self):
        pass

class ExperimentState(ChickenBoxState):
    def __init__(self, manager):
        super().__init__(manager)
        start_experiment()

    def chicken_detected_in_box(self):
        pass
    
    def chicken_exited_box(self):
        pass

    def experiment_finished(self):
        open_door(DoorIds.EXIT)
        self.manager.state = ResetState(self.manager)

class ResetState(ChickenBoxState):
    def __init__(self, manager):
        super().__init__(manager)

    def chicken_detected_in_box(self):
        pass
    
    def chicken_exited_box(self):
        close_door(DoorIds.EXIT)
        open_door(DoorIds.FRONT)
        self.manager.state = StartState(self.manager)

    def experiment_finished(self):
        pass



if __name__ == '__main__':
    ChickenBoxManager()
    sys.exit(main())