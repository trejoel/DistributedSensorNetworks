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
        self.distance=0
        self.children=[]

    ###################
    def run(self):
        if self.id == SOURCE:
            pck = (self,0)
            self.cb_flood_send(pck)
            #self.flood_received = True
            #for neigh in Neighbors:
            #    print("Neighbor:",neigh[1].id)
            

    ###################
    def on_receive(self, pck):
        #print("MESSAGE RECEIVED")
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
                self.parent=sender
                print("parent of "+str(self.id)+" is "+str(self.parent))
                pck=(pck[0],distance)#acknowledge message
                self.send(sender, pck)
                self.distance=distance+1
                pck=(self,self.distance)
                self.cb_flood_send(pck)
        #self.log(sender)


    ###################
    def cb_flood_send(self, pck):
        self.send(DawnSim.BROADCAST_ADDR, pck)
        #self.log('Flood msg is sent.')
        

# setting the simulation
sim = DawnSim.Simulator(
    duration=3,
    timescale=0.5)

# adding nodes
sim.add_node(Node, (50,50), 75)
sim.add_node(Node, (50,100), 75)
sim.add_node(Node, (0,150), 75)
sim.add_node(Node, (100,150), 75)
sim.add_node(Node, (50, 200),75)

# start the simulation
sim.run()
