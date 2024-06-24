#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 10:49:02 2024

@author: jtrejo
"""

import random
import sys
sys.path.insert(1, '.')
from source import DawnSim

SOURCE = 0


###########################################################
class Node(DawnSim.BaseNode):

    ###################
    def init(self):
        self.parent=self.id
        self.children=[]

    ###################
    def run(self):
        if self.id == SOURCE:
            pck = self
            self.cb_flood_send(pck)
            self.flood_received = True
            Neighbors=self.neighbor_distance_list
            #for neigh in Neighbors:
            #    print("Neighbor:",neigh[1].id)
            

    ###################
    def on_receive(self, pck):
        #print("MESSAGE RECEIVED")
        sender=pck.id
        if self.id==SOURCE:
            self.log("MESSAGE ACKNOWLEDGE FROM "+str(sender))
        else:
            self.log("MESSAGE RECEIVED FROM "+str(sender))
            pck=self
            self.send(sender, pck)
        #self.log(sender)


    ###################
    def cb_flood_send(self, pck):
        self.send(DawnSim.BROADCAST_ADDR, pck)
        self.log('Flood msg is sent.')
        

# setting the simulation
sim = DawnSim.Simulator(
    duration=10,
    timescale=0.5)

# adding nodes
sim.add_node(Node, (50,50), 75)
sim.add_node(Node, (50,100), 75)
sim.add_node(Node, (0,150), 75)
sim.add_node(Node, (100,150), 75)
sim.add_node(Node, (50, 200),75)

# start the simulation
sim.run()
