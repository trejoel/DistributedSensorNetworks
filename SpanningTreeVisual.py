import random
import sys
sys.path.insert(1, '.')
from source import DawnSimVis

SOURCE = 35


###########################################################
class Node(DawnSimVis.BaseNode):

    ###################
    def init(self):
        self.parent=self.id
        self.distance=0
        self.children=[]
        
    ###################
    def run(self):
        if self.id == SOURCE:
            self.change_color(1, 0, 0)
            pck = (self,0)
            self.cb_flood_send(pck)


    ###################
    def on_receive(self, pck):
        sender=pck[0].id
        distance=pck[1]
        if self.id==sender:# this is an ack
            self.log("MESSAGE ACKNOWLEDGE FROM "+str(sender)+" at distance "+str(distance))
            self.children.append(sender)
            print("children of:",str(self.id))
            print(self.children)
        else:
            if (self.parent==self.id and self.id!=SOURCE):
                self.log("MESSAGE RECEIVED FROM "+str(sender)+" at distance "+str(distance))
                self.change_color(0, 0, 1)
                self.parent=sender
                print("parent of "+str(self.id)+" is "+str(self.parent))
                pck=(pck[0],distance)#acknowledge message
                self.send(sender, pck)
                self.distance=distance+1
                pck=(self,self.distance)
                #self.set_timer(1, self.cb_flood_send, pck)
                self.cb_flood_send(pck)


    ###################
    def cb_flood_send(self, pck):
        self.send(DawnSimVis.BROADCAST_ADDR, pck)


###########################################################
def create_network():
    # place nodes over 100x100 grids
    for x in range(10):
        for y in range(10):
            px = 50 + x*60 + random.uniform(-20,20)
            py = 50 + y*60 + random.uniform(-20,20)
            sim.add_node(Node, pos=(px,py), tx_range=75)


# setting the simulation
sim = DawnSimVis.Simulator(
    duration=10,
    timescale=3,
    visual=True,
    terrain_size=(650, 650),
    title='Flooding')

# creating network
create_network()

# start the simulation
sim.run()
