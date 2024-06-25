#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 00:27:56 2024

@author: jtrejo
"""

import random
import sys
sys.path.insert(1, '.')
from source import DawnSimVis

SOURCE = 0
N=8


###########################################################
class Node(DawnSimVis.BaseNode):

    ###################
    def init(self):
        self.parent=self.id
        self.distance=0
        self.children=[]
        
    ###################
    def run(self):
        pck=(self,0)
        neighbor=(self.id+1) % N
        self.send(neighbor, pck)


    ###################
    def on_receive(self, pck):
        candidate=pck[0]
        distance=pck[1]
        if self.id==candidate.id:
            self.leader=True
            self.change_color(1, 0, 0)
            self.log(str(self.id)+" is the leader ")
        elif self.id>candidate.id:
            self.change_color(0, 0, 1)
            self.log("Message received from "+str(candidate)) 
            neighbor=(self.id+1) % N
            pck=(candidate,distance+1)
            self.send(neighbor, pck)


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
    duration=2,
    timescale=1,
    visual=True,
    terrain_size=(650, 650),
    title='Leader Election')

# creating network
#create_network()
# adding nodes
sim.add_node(Node, (50,50), 50)
sim.add_node(Node, (100,50), 50)
sim.add_node(Node, (150,50), 50)
sim.add_node(Node, (200,50), 50)
sim.add_node(Node, (200, 100),50)
sim.add_node(Node, (150, 100),50)
sim.add_node(Node, (100, 100),50)
sim.add_node(Node, (50, 100),50)


# start the simulation
sim.run()
